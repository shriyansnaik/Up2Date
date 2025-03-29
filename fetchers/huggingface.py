# https://huggingface.co/blog/feed.xml
import feedparser
from typing import List, Dict

def huggingface():
    url = "https://huggingface.co/blog/feed.xml"
    feed = feedparser.parse(url)
    
    articles = []
    for entry in feed.entries:
        article = {
            'title': entry.title,
            'link': entry.guid,
            'description': entry.published  # Using published date as description
        }
        articles.append(article)
    
    return articles