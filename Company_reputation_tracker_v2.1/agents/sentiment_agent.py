from config import SENTIMENT_APPROACH, OPENAI_API_KEY
import openai
from textblob import TextBlob

class SentimentAgent:
    def __init__(self):
        self.approach = SENTIMENT_APPROACH
        if self.approach == "openai":
            openai.api_key = OPENAI_API_KEY

    def get_sentiment(self, text):
        if self.approach == "openai":
            return self._openai_sentiment(text)
        else:
            return self._textblob_sentiment(text)

    def _openai_sentiment(self, text):
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=f"""Classify the sentiment of this text as Positive, Negative, or Neutral

Text: {text}""",
                max_tokens=1,
                temperature=0
            )
            sentiment_str = response.choices[0].text.strip()
            return sentiment_str.upper()
        except Exception:
            return "NEUTRAL"

    def _textblob_sentiment(self, text):
        analysis = TextBlob(text)
        polarity = analysis.sentiment.polarity
        if polarity > 0.1:
            return "POSITIVE"
        elif polarity < -0.1:
            return "NEGATIVE"
        else:
            return "NEUTRAL"
