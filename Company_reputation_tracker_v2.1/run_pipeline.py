from database.db_utils import get_db_session
from database.schema import Company, Mention
from agents.mention_fetcher import MentionFetcher
from agents.sentiment_agent import SentimentAgent

def run_pipeline():
    session = get_db_session()
    fetcher = MentionFetcher()
    sentiment_agent = SentimentAgent()

    companies = session.query(Company).all()
    for company in companies:
        print(f"Processing: {company.name}")
        mentions_data = fetcher.fetch_mentions(company.aliases, days_back=7)
        for data in mentions_data:
            existing = session.query(Mention).filter_by(company_id=company.id, title=data["title"], url=data["url"]).first()
            if not existing:
                sentiment = sentiment_agent.get_sentiment(data["content"])
                mention = Mention(company_id=company.id, title=data["title"], content=data["content"], sentiment=sentiment,
                                  url=data["url"], source=data["source"], published_at=data["published_at"])
                session.add(mention)
        session.commit()
    session.close()

if __name__ == "__main__":
    run_pipeline()
