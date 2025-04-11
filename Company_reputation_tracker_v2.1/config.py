import os
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "YOUR_NEWSAPI_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY")
DB_URL = "sqlite:///company_tracker.db"
SENTIMENT_APPROACH = "textblob"
