import hashlib
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text,nullable=False)
    source = db.Column(db.String(128), nullable=False)
    scraped_at = db.Column(db.DateTime, default=datetime.utcnow)

    title_hash = db.Column(db.String(64), nullable=False, unique=True)
    url_hash = db.Column(db.String(64), nullable=False, unique=True)

    def __init__(self, title, url, image_url=None, source=None):
        self.title = title
        self.url = url
        self.image_url = image_url
        self.source = source
        self.title_hash = hashlib.sha256(title.encode('utf-8')).hexdigest()
        self.url_hash = hashlib.sha256(url.encode('utf-8')).hexdigest()
