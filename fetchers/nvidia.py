# https://blogs.nvidia.com/blog/category/generative-ai/feed/
# https://blogs.nvidia.com/blog/tag/healthcare-life-sciences/feed/

import feedparser
from typing import List, Dict

def nvidia():
    url = "https://blogs.nvidia.com/blog/category/generative-ai/feed/"
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