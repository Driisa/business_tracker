import datetime
from newsapi import NewsApiClient
from config import NEWSAPI_KEY

class MentionFetcher:
    def __init__(self, api_key=NEWSAPI_KEY):
        self.client = NewsApiClient(api_key=api_key)

    def fetch_mentions(self, aliases, days_back=7):
        from_date = (datetime.datetime.now() - datetime.timedelta(days=days_back)).strftime("%Y-%m-%d")
        query = " OR ".join([f'"{alias.strip()}"' for alias in aliases.split(",")])
        response = self.client.get_everything(
            q=query,
            from_param=from_date,
            language="en",
            sort_by="relevancy",
            page_size=20
        )
        mentions = []
        for article in response.get("articles", []):
            mentions.append({
                "title": article["title"] or "No Title",
                "content": article["description"] or "",
                "url": article["url"],
                "source": article["source"]["name"],
                "published_at": article["publishedAt"]
            })
        return mentions
