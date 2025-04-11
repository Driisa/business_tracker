import requests
import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
import torch

# Load environment variables
load_dotenv()

# API Keys
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

# Initialize sentiment analysis pipeline with caching to avoid loading the model multiple times
_sentiment_analyzer = None

def get_sentiment_analyzer():
    """Get or initialize the sentiment analysis pipeline."""
    global _sentiment_analyzer
    if _sentiment_analyzer is None:
        try:
            print("Loading Hugging Face sentiment analysis model...")
            
            # Option 1: Use the pipeline directly (simpler but loads the model from scratch)
            # _sentiment_analyzer = pipeline('sentiment-analysis', model="distilbert-base-uncased-finetuned-sst-2-english")
            
            # Option 2: Load model and tokenizer once (more efficient)
            model_name = "distilbert-base-uncased-finetuned-sst-2-english"
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForSequenceClassification.from_pretrained(model_name)
            
            # Create a custom function to use the loaded model and tokenizer
            def analyze_with_model(text):
                inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512, padding=True)
                with torch.no_grad():
                    outputs = model(**inputs)
                scores = torch.nn.functional.softmax(outputs.logits, dim=1)
                
                # This model gives "POSITIVE" or "NEGATIVE" only (no NEUTRAL)
                # We'll interpret scores close to 0.5 as NEUTRAL
                highest_score = scores[0].max().item()
                highest_index = scores[0].argmax().item()
                
                # The model uses 0 for NEGATIVE and 1 for POSITIVE
                if highest_index == 1:  # POSITIVE
                    label = "POSITIVE"
                    # Scale from [0.5, 1.0] to [0.0, 1.0]
                    normalized_score = (highest_score - 0.5) * 2 if highest_score > 0.5 else 0
                else:  # NEGATIVE
                    label = "NEGATIVE"
                    # Scale from [0.5, 1.0] to [-1.0, 0.0]
                    normalized_score = -(highest_score - 0.5) * 2 if highest_score > 0.5 else 0
                
                # Create NEUTRAL zone if confidence is low
                if 0.4 < highest_score < 0.6:
                    label = "NEUTRAL"
                    normalized_score = 0
                
                return {"label": label, "score": normalized_score}
            
            _sentiment_analyzer = analyze_with_model
            print("Hugging Face model loaded successfully!")
            
        except Exception as e:
            print(f"Error loading Hugging Face model: {e}")
            print("Falling back to basic sentiment analysis...")
            
            # Define a simple function that always returns neutral
            def fallback_analyzer(text):
                return {"label": "NEUTRAL", "score": 0.0}
            
            _sentiment_analyzer = fallback_analyzer
    
    return _sentiment_analyzer

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
    """Analyze sentiment using Hugging Face Transformers."""
    if not text:
        return {"label": "NEUTRAL", "score": 0.0}
    
    try:
        # Get or initialize the sentiment analyzer
        sentiment_analyzer = get_sentiment_analyzer()
        
        # Use a reasonable text length to avoid issues with very long texts
        truncated_text = text[:1000] if text else ""
        
        # Analyze sentiment
        result = sentiment_analyzer(truncated_text)
        
        return result
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        return {"label": "NEUTRAL", "score": 0.0}


def analyze_mentions(mentions):
    """Analyze sentiment for a list of mentions."""
    enriched_mentions = []
    
    # Load analyzer once for all mentions
    get_sentiment_analyzer()
    
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
        
        # Test batch sentiment analysis
        enriched_mentions = analyze_mentions(test_mentions[:2])
        print(f"Analyzed {len(enriched_mentions)} mentions")
        for mention in enriched_mentions:
            print(f"Title: {mention['title'][:50]}...")
            print(f"Sentiment: {mention['sentiment']}, Score: {mention['sentiment_score']}")
            print("---")