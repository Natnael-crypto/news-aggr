from api.models import db, Article
from sqlalchemy.exc import IntegrityError

class ArticleRepository:
    def __init__(self, session):
        self.session = session

    def create_article(self, title: str, url: str, image_url: str, source: str):
        article = Article(title=title, url=url, image_url=image_url, source=source)
        self.session.add(article)
        try:
            self.session.commit()
            return article
        except IntegrityError:
            self.session.rollback()
            return None  # Duplicate article (based on unique constraints)

    def get_articles(self, page=1, per_page=10, source=None):
        query = self.session.query(Article).order_by(Article.scraped_at.desc())

        if source:
            query = query.filter_by(source=source)

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        return {
            "articles": [self.serialize(article) for article in pagination.items],
            "total": pagination.total,
            "pages": pagination.pages,
            "current_page": pagination.page
        }

    @staticmethod
    def serialize(article: Article):
        return {
            "id": article.id,
            "title": article.title,
            "url": article.url,
            "image_url": article.image_url,
            "source": article.source,
            "scraped_at": article.scraped_at.isoformat()
        }
