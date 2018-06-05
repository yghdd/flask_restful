# coding: utf-8
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Article(Base):
    __tablename__ = 'article'

    id = Column(Integer, primary_key=True)
    title = Column(String(50), unique=True)
    content = Column(Text)
    origin = Column(String(50))
    cate_id = Column(ForeignKey('news_category.id'), index=True)
    pict = Column(String(100))

    cate = relationship('NewsCategory', primaryjoin='Article.cate_id == NewsCategory.id', backref='articles')


class Image(Base):
    __tablename__ = 'image'

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    url = Column(String(200))


class Music(Base):
    __tablename__ = 'music'

    name = Column(String(30), nullable=False)
    singer = Column(String(30))
    url = Column(String(200), nullable=False)
    id = Column(Integer, primary_key=True)


class NewsCategory(Base):
    __tablename__ = 'news_category'

    id = Column(Integer, primary_key=True)
    title = Column(String(20), nullable=False, unique=True)
    ord_no = Column(Integer)
    origin_url = Column(String(20))


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    @property
    def json(self):
        return {'id':self.id,'name':self.name}
