from sqlalchemy import create_engine, Column, Integer, String, Text, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from datetime import datetime
from datetime import timedelta

# Create SQLAlchemy Base
Base = declarative_base()

# Database URL
DATABASE_URL = "sqlite:///company_tracker.db"

# Create engine and session
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = scoped_session(SessionLocal)

class Company(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    aliases = Column(Text, nullable=True)  # Stored as comma-separated values
    created_at = Column(DateTime, default=datetime.now)
    
    mentions = relationship("Mention", back_populates="company", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Company(id={self.id}, name='{self.name}')>"

class Mention(Base):
    __tablename__ = "mentions"
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=True)
    sentiment = Column(String(20), nullable=True)  # POSITIVE, NEGATIVE, NEUTRAL
    sentiment_score = Column(Float, nullable=True)
    url = Column(String(255), nullable=False)
    source = Column(String(100), nullable=True)
    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    
    company = relationship("Company", back_populates="mentions")
    
    def __repr__(self):
        return f"<Mention(id={self.id}, title='{self.title[:20]}...', sentiment='{self.sentiment}')>"

def init_db():
    """Initialize the database, creating all tables."""
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully.")

def get_db():
    """Get a database session."""
    db = db_session()
    try:
        return db
    finally:
        db.close()

# Database utility functions
def add_company(name, aliases):
    """Add a new company to the database."""
    db = get_db()
    try:
        # Check if company already exists
        existing = db.query(Company).filter(Company.name == name).first()
        if existing:
            return existing
        
        # Format aliases as comma-separated string
        aliases_str = ','.join(aliases) if aliases else ''
        
        # Create new company
        company = Company(name=name, aliases=aliases_str)
        db.add(company)
        db.commit()
        return company
    except Exception as e:
        db.rollback()
        print(f"Error adding company: {e}")
        return None

def get_companies():
    """Get all companies."""
    db = get_db()
    return db.query(Company).all()

def get_company(company_id):
    """Get a company by ID."""
    db = get_db()
    return db.query(Company).filter(Company.id == company_id).first()

def get_company_aliases(company_id):
    """Get aliases for a company."""
    db = get_db()
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company or not company.aliases:
        return []
    return [alias.strip() for alias in company.aliases.split(',') if alias.strip()]

def add_mentions(company_id, mentions):
    """Add mentions for a company."""
    db = get_db()
    count = 0
    try:
        # Check if company exists
        company = db.query(Company).filter(Company.id == company_id).first()
        if not company:
            return 0
        
        for mention in mentions:
            # Check for duplicate by URL
            existing = db.query(Mention).filter(
                Mention.company_id == company_id,
                Mention.url == mention.get('url', '')
            ).first()
            
            if existing:
                # Update existing mention
                existing.title = mention.get('title', existing.title)
                existing.content = mention.get('content', existing.content)
                existing.sentiment = mention.get('sentiment', existing.sentiment)
                existing.sentiment_score = mention.get('sentiment_score', existing.sentiment_score)
                existing.source = mention.get('source', existing.source)
                if 'published_at' in mention and mention['published_at']:
                    existing.published_at = mention['published_at']
            else:
                # Create new mention
                new_mention = Mention(
                    company_id=company_id,
                    title=mention.get('title', 'No title'),
                    content=mention.get('content', ''),
                    sentiment=mention.get('sentiment', 'NEUTRAL'),
                    sentiment_score=mention.get('sentiment_score', 0.0),
                    url=mention.get('url', ''),
                    source=mention.get('source', 'Unknown'),
                    published_at=mention.get('published_at')
                )
                db.add(new_mention)
                count += 1
        
        db.commit()
        return count
    except Exception as e:
        db.rollback()
        print(f"Error adding mentions: {e}")
        return 0

def get_mentions(company_id, sentiment=None):
    """Get mentions for a company."""
    db = get_db()
    query = db.query(Mention).filter(Mention.company_id == company_id)
    
    if sentiment:
        query = query.filter(Mention.sentiment == sentiment.upper())
    
    # Order by published date (newest first)
    query = query.order_by(Mention.published_at.desc())
    
    return query.all()

def get_sentiment_stats(company_id):
    """Get sentiment statistics for a company."""
    db = get_db()
    mentions = db.query(Mention).filter(Mention.company_id == company_id).all()
    
    stats = {
        "POSITIVE": 0,
        "NEGATIVE": 0,
        "NEUTRAL": 0,
        "TOTAL": len(mentions),
        "AVG_SCORE": 0.0
    }
    
    total_score = 0.0
    score_count = 0
    
    for mention in mentions:
        if mention.sentiment in stats:
            stats[mention.sentiment] += 1
        else:
            stats["NEUTRAL"] += 1
            
        # Track score for average calculation
        if mention.sentiment_score is not None:
            total_score += mention.sentiment_score
            score_count += 1
    
    # Calculate average sentiment score
    if score_count > 0:
        stats["AVG_SCORE"] = total_score / score_count
    
    return stats

def get_sentiment_timeline_data(company_id, days=None):
    """Get sentiment data over time for a company.
    
    Args:
        company_id: The company ID
        days: Optional number of days to limit results
        
    Returns:
        List of mentions with date and sentiment information
    """
    db = get_db()
    query = db.query(Mention).filter(Mention.company_id == company_id)
    
    if days:
        cutoff_date = datetime.now() - timedelta(days=days)
        query = query.filter(Mention.published_at >= cutoff_date)
    
    # Order by published date
    mentions = query.order_by(Mention.published_at).all()
    
    return mentions

if __name__ == "__main__":
    # Initialize database when run directly
    init_db()