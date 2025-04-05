# --- db/models.py (SQLAlchemy Models) ---

from sqlalchemy import Column, String, Text, DateTime, Numeric, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String
import uuid

Base = declarative_base()

class Company(Base):
    __tablename__ = 'companies'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(Text, nullable=False)
    aliases = Column(JSON, default=list)
    website = Column(Text)
    industry = Column(Text)
    preferences = Column(JSON, default=dict)
    schedule = Column(Text)

class Mention(Base):
    __tablename__ = 'mentions'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String, ForeignKey("companies.id"))
    content = Column(Text)
    url = Column(Text)
    channel = Column(Text)
    sentiment = Column(Text)
    topic = Column(Text)
    published_at = Column(DateTime)

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String, ForeignKey("companies.id"))
    platform = Column(Text)
    rating = Column(Numeric)
    review_text = Column(Text)
    published_at = Column(DateTime)

class Summary(Base):
    __tablename__ = 'summaries'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String, ForeignKey("companies.id"))
    timeframe = Column(Text)
    summary = Column(Text)
    sentiment_summary = Column(JSON)