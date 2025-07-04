import os
from flask import Flask, render_template, request
from flask_apscheduler import APScheduler
from dotenv import load_dotenv
from api.models import db
from api.repositories.article_repository import ArticleRepository
from run_scraper import scraper

load_dotenv()

class Config:
    SCHEDULER_API_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

scheduler = APScheduler()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    scheduler.init_app(app)
    scheduler.start()

    with app.app_context():
        db.create_all()
        # scrape_and_store_news()

    register_routes(app)
    return app

@scheduler.task('interval', id='scrape_news_task', hours=24, misfire_grace_time=3600)
def scrape_and_store_news():
    from api.models import Article
    articles = scraper()
    repo = ArticleRepository(db.session)
    print(f"Got {len(articles)} from the scraper")

    for item in articles:
        if not item['title'] or not item['url']:
            continue
        try:
            repo.create_article(
                title=item['title'],
                url=item['url'],
                image_url=item.get('image_url'),
                source=item.get('source')
            )
        except Exception as e:
            print(f"[ERROR] Could not insert article: {e}")

def register_routes(app):
    @app.route("/")
    def home():
        repo = ArticleRepository(db.session)
        articles = repo.get_articles(page=1, per_page=6)["articles"]
        sources = ["BBC","CNN","The Guardian","SKY News"]
        return render_template("index.html", articles=articles, sources=sources)

    @app.route("/load_news")
    def load_news():
        page = int(request.args.get("page", 1))
        source = request.args.get("source")
        repo = ArticleRepository(db.session)
        articles = repo.get_articles(page=page, per_page=6, source=source)["articles"]
        return "".join(
            render_template("components/news_card.html", article=article)
            for article in articles
        )

if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0",debug=False)
