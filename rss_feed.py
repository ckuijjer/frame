import feedparser

def fetch_rss_feed(rss_url: str) -> tuple[str, str]:
    """
    Retrieve the RSS feed and return the title and summary of the first article.
    
    Args:
        rss_url (str): URL of the RSS feed.
    
    Returns:
        tuple: (title, summary) of the first article.
    """
    feed = feedparser.parse(rss_url)
    first_article = feed.entries[0]
    title = first_article.title
    summary = first_article.summary
    return title, summary
