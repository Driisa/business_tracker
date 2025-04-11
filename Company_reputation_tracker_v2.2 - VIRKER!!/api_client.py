import requests
import json
import os
from datetime import datetime, timedelta
from textblob import TextBlob
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

class NewsClient:
    """Client for fetching news from NewsAPI."""
    
    def __init__(self):
        self.api_key = NEWSAPI_KEY
        self.base_url = "https://newsapi.org/v2/everything"
    
    def fetch_mentions(self, company_name, aliases, days=7):
        """Fetch mentions of a company from NewsAPI."""
        if not self.api_key:
            raise ValueError("NewsAPI key is not set. Please set NEWSAPI_KEY in .env file.")
        
        # Combine company name and aliases for search
        search_terms = [company_name] + [alias.strip() for alias in aliases if alias.strip()]
        query = " OR ".join([f'"{term}"' for term in search_terms])
        
        # Calculate date range
        to_date = datetime.now().strftime('%Y-%m-%d')
        from_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        # Request parameters
        params = {
            'q': query,
            'from': from_date,
            'to': to_date,
            'language': 'en',
            'sortBy': 'publishedAt',
            'apiKey': self.api_key
        }
        
        try:
            # Make API request
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('status') != 'ok':
                print(f"Error from NewsAPI: {data.get('message', 'Unknown error')}")
                return []
            
            # Process and normalize results
            mentions = []
            for article in data.get('articles', []):
                published_at = None
                if article.get('publishedAt'):
                    try:
                        published_at = datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
                    except ValueError:
                        try:
                            published_at = datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%S.%fZ')
                        except ValueError:
                            published_at = None
                
                mention = {
                    'title': article.get('title', 'No title'),
                    'content': article.get('description', article.get('content', '')),
                    'url': article.get('url', ''),
                    'source': article.get('source', {}).get('name', 'Unknown'),
                    'published_at': published_at
                }
                mentions.append(mention)
            
            print(f"Found {len(mentions)} mentions for {company_name}")
            return mentions
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching mentions: {e}")
            return []


def analyze_sentiment(text):
    """Analyze sentiment using TextBlob."""
    if not text:
        return {"label": "NEUTRAL", "score": 0.0}
    
    try:
        # Use TextBlob for sentiment analysis
        analysis = TextBlob(text)
        
        # TextBlob polarity ranges from -1 (negative) to 1 (positive)
        score = analysis.sentiment.polarity
        
        # Determine sentiment label based on score
        if score > 0.1:
            label = "POSITIVE"
        elif score < -0.1:
            label = "NEGATIVE"
        else:
            label = "NEUTRAL"
        
        return {
            "label": label,
            "score": score
        }
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        return {"label": "NEUTRAL", "score": 0.0}


def analyze_mentions(mentions):
    """Analyze sentiment for a list of mentions."""
    enriched_mentions = []
    
    for mention in mentions:
        # Combine title and content for better analysis
        text = f"{mention.get('title', '')} {mention.get('content', '')}"
        
        # Get sentiment
        sentiment = analyze_sentiment(text)
        
        # Add sentiment to mention
        enriched_mention = mention.copy()
        enriched_mention['sentiment'] = sentiment["label"]
        enriched_mention['sentiment_score'] = sentiment["score"]
        
        enriched_mentions.append(enriched_mention)
    
    return enriched_mentions


# Test functionality when run directly
if __name__ == "__main__":
    # Test NewsAPI client
    news_client = NewsClient()
    test_mentions = news_client.fetch_mentions("Tesla", ["TSLA", "Tesla Inc."], days=3)
    print(f"Found {len(test_mentions)} mentions")
    
    if test_mentions:
        # Test sentiment analysis
        sentiment_result = analyze_sentiment(test_mentions[0]["title"])
        print(f"Sentiment: {sentiment_result['label']}, Score: {sentiment_result['score']}")