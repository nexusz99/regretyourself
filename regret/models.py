from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from regret.database import Base


class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    author = Column(String(50))
    msg = Column(String(10240))
    create_at = Column(DateTime(timezone='Asia/Seoul'))
    session_id = Column(String(64))

    thumbsup = relationship("ThumbsUp", backref='thumbs')


class ThumbsUp(Base):
    __tablename__ = 'thumbs'
    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey(Article.id))
    session_id = Column(String(64))
    create_at = Column(DateTime(timezone='Asia/Seoul'))
