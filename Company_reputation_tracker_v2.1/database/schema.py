from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func
from sqlalchemy.orm import relationship

Base = declarative_base()

class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    aliases = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    mentions = relationship("Mention", back_populates="company")

class Mention(Base):
    __tablename__ = "mentions"
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=True)
    sentiment = Column(String, nullable=True)
    url = Column(String, nullable=True)
    source = Column(String, nullable=True)
    published_at = Column(DateTime, nullable=True)
    company = relationship("Company", back_populates="mentions")
