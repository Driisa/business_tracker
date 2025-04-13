import requests
import json
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import google.generativeai as genai
from logger import get_logger, log_function_call, log_info, log_error, log_warning
from bs4 import BeautifulSoup
import time
import random

# Get logger
logger = get_logger()

# Load environment variables
load_dotenv()

# API Keys
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize sentiment analysis with caching to avoid initializing multiple times
_sentiment_analyzer = None

@log_function_call
def get_sentiment_analyzer():
    """Get or initialize the Gemini AI sentiment analysis."""
    global _sentiment_analyzer
    if _sentiment_analyzer is None:
        try:
            log_info("Initializing Gemini AI for sentiment analysis...")
            
            # Configure the Gemini API
            if not GEMINI_API_KEY:
                raise ValueError("GEMINI_API_KEY is not set in .env file")
                
            genai.configure(api_key=GEMINI_API_KEY)
            
            # Initialize the Gemini model
            model = genai.GenerativeModel('gemini-pro')
            
            # Create a function to analyze sentiment using Gemini
            def analyze_with_gemini(text):
                if not text or len(text.strip()) == 0:
                    return {"label": "NEUTRAL", "score": 0.0}
                
                # Prompt for sentiment analysis
                prompt = f"""Analyze the sentiment of the following text and respond with ONLY a JSON object containing:
                1. 'label': either 'POSITIVE', 'NEGATIVE', or 'NEUTRAL'
                2. 'score': a number between -1.0 (very negative) and 1.0 (very positive), with 0.0 being neutral
                
                Text to analyze: "{text}"
                
                JSON response:"""
                
                try:
                    response = model.generate_content(prompt)
                    response_text = response.text
                    
                    # Extract JSON from response
                    try:
                        # Find JSON in the response
                        json_start = response_text.find('{')
                        json_end = response_text.rfind('}')
                        
                        if json_start >= 0 and json_end >= 0:
                            json_str = response_text[json_start:json_end+1]
                            result = json.loads(json_str)
                            
                            # Validate the result format
                            if 'label' in result and 'score' in result:
                                # Ensure label is one of the expected values
                                if result['label'] not in ['POSITIVE', 'NEGATIVE', 'NEUTRAL']:
                                    result['label'] = 'NEUTRAL'
                                    
                                # Ensure score is within expected range
                                score = float(result['score'])
                                result['score'] = max(min(score, 1.0), -1.0)
                                
                                return result
                    except Exception as json_error:
                        log_error(f"Error parsing Gemini response: {json_error}", exc_info=True)
                    
                    # If we couldn't parse the JSON or it didn't have the expected format,
                    # try to determine sentiment from the raw response
                    if 'positive' in response_text.lower():
                        return {"label": "POSITIVE", "score": 0.7}
                    elif 'negative' in response_text.lower():
                        return {"label": "NEGATIVE", "score": -0.7}
                    else:
                        return {"label": "NEUTRAL", "score": 0.0}
                        
                except Exception as e:
                    log_error(f"Error calling Gemini API: {e}", exc_info=True)
                    return {"label": "NEUTRAL", "score": 0.0}
            
            _sentiment_analyzer = analyze_with_gemini
            log_info("Gemini AI initialized successfully!")
            
        except Exception as e:
            log_error(f"Error initializing Gemini AI: {e}", exc_info=True)
            log_warning("Falling back to basic sentiment analysis...")
            
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
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    @log_function_call
    def fetch_article_content(self, url):
        """Fetch and extract the main content from an article URL using BeautifulSoup."""
        if not url:
            return ""
            
        try:
            # Add a small delay to avoid overwhelming the server
            time.sleep(random.uniform(0.5, 1.5))
            
            # Make the request to the article URL
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
                
            # Get the text content
            text = soup.get_text(separator=' ', strip=True)
            
            # Clean up the text (remove extra whitespace)
            text = ' '.join(text.split())
                
            log_info(f"Successfully extracted content from {url} ({len(text)} chars)")
            return text
            
        except Exception as e:
            log_error(f"Error extracting content from {url}: {e}", exc_info=True)
            return ""
    
    @log_function_call
    def fetch_mentions(self, company_name, aliases, days=7):
        """Fetch mentions of a company from NewsAPI."""
        if not self.api_key:
            log_error("NewsAPI key is not set")
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
                log_error(f"Error from NewsAPI: {data.get('message', 'Unknown error')}")
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
                
                # Get the article URL
                url = article.get('url', '')
                
                # Extract the full content using BeautifulSoup
                scraped_content = ""
                
                scraped_content = self.fetch_article_content(url)
            
                
                mention = {
                    'title': article.get('title', 'No title'),
                    'content': scraped_content,
                    'url': url,
                    'source': article.get('source', {}).get('name', 'Unknown'),
                    'published_at': published_at
                }
                mentions.append(mention)
            
            log_info(f"Found {len(mentions)} mentions for {company_name}")
            return mentions
            
        except requests.exceptions.RequestException as e:
            log_error(f"Error fetching mentions: {e}", exc_info=True)
            return []


@log_function_call
def analyze_sentiment(text):
    """Analyze sentiment using Hugging Face Transformers."""
    if not text:
        log_info("Empty text provided for sentiment analysis, returning NEUTRAL")
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
        log_error(f"Error analyzing sentiment: {e}", exc_info=True)
        return {"label": "NEUTRAL", "score": 0.0}


@log_function_call
def analyze_mentions(mentions):
    """Analyze sentiment for a list of mentions."""
    log_info(f"Analyzing sentiment for {len(mentions)} mentions")
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
    # Initialize logging
    from logger import log_startup, log_shutdown
    log_startup()
    
    # Test NewsAPI client
    news_client = NewsClient()
    test_mentions = news_client.fetch_mentions("Tesla", ["TSLA", "Tesla Inc."], days=3)
    log_info(f"Found {len(test_mentions)} mentions")
    
    if test_mentions:
        # Test sentiment analysis
        sentiment_result = analyze_sentiment(test_mentions[0]["title"])
        log_info(f"Sentiment: {sentiment_result['label']}, Score: {sentiment_result['score']}")
        
        # Test batch sentiment analysis
        enriched_mentions = analyze_mentions(test_mentions[:2])
        log_info(f"Analyzed {len(enriched_mentions)} mentions")
        for mention in enriched_mentions:
            log_info(f"Title: {mention['title'][:50]}...")
            log_info(f"Sentiment: {mention['sentiment']}, Score: {mention['sentiment_score']}")
            log_info("---")
    
    # Log shutdown
    log_shutdown()