from sqlalchemy import Column, ForeignKey, Integer, String  
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import relationship  
from sqlalchemy import create_engine  
from config import URL_DATABASE_CONNECT


Base = declarative_base()  
class Article(Base):  
    __tablename__ = 'article'
    id = Column(Integer, primary_key=True)  
    title = Column(String(250), nullable=False)  
    author = Column(String(250), nullable=False)  
    text = Column(String(3000))


engine = create_engine(URL_DATABASE_CONNECT)  
Base.metadata.create_all(engine)
