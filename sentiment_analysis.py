import requests
import config
from datetime import datetime, timedelta
from textblob import TextBlob

def fetch_news_articles(pair):
    if not config.ENABLE_SENTIMENT_ANALYSIS:
        return []

    base_currency = pair[:3]
    quote_currency = pair[3:]
    query = f"{base_currency} OR {quote_currency}"

    url = (
        f"https://newsapi.org/v2/everything?q={query}"
        f"&from={(datetime.now() - timedelta(days=config.SENTIMENT_LOOKBACK_DAYS)).strftime('%Y-%m-%d')}"
        f"&sortBy={config.SENTIMENT_SORT_BY}&language={config.SENTIMENT_LANGUAGE}"
        f"&apiKey={config.NEWSAPI_KEY}"
    )

    try:
        response = requests.get(url, timeout=config.SENTIMENT_REQUEST_TIMEOUT)
        data = response.json()
        if config.LOG_SENTIMENT:
            print(f"[Sentiment] Fetched {len(data.get('articles', []))} articles for {pair}")
        return data.get("articles", [])
    except Exception as e:
        if config.LOG_ERRORS:
            print(f"[Error] Failed to fetch news for {pair}: {e}")
        return []

def analyze_article_sentiment(article):
    """
    Analyzes sentiment of a single article using TextBlob.
    Returns polarity score from -1.0 to 1.0
    """
    content = article.get("title", "") + ". " + article.get("description", "")
    blob = TextBlob(content)
    return blob.sentiment.polarity

def compute_overall_sentiment(pair):
    articles = fetch_news_articles(pair)
    if not articles:
        return 0.0

    polarity_scores = [analyze_article_sentiment(article) for article in articles if article.get("title")]
    if not polarity_scores:
        return 0.0

    average_score = sum(polarity_scores) / len(polarity_scores)

    if config.LOG_SENTIMENT:
        print(f"[Sentiment] Average polarity for {pair}: {average_score:.2f}")

    return average_score

def determine_sentiment_bias(score):
    """
    Returns 'bullish', 'bearish' or 'neutral' based on polarity score and config thresholds.
    """
    if score >= config.SENTIMENT_BULLISH_THRESHOLD:
        return "bullish"
    elif score <= config.SENTIMENT_BEARISH_THRESHOLD:
        return "bearish"
    else:
        return "neutral"
