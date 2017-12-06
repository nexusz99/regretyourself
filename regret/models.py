from sqlalchemy import Column, Integer, String

from regret.database import Base


class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)

