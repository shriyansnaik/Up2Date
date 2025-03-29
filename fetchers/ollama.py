# https://ollama.com/blog

import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

def ollama():
    url="https://ollama.com/blog"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    html = response.text

    # Parse the HTML
    soup = BeautifulSoup(html, 'html.parser')

    list_element = soup.select_one("body > main > section")

    articles = list_element.find_all("a", recursive=False)

    results = []
    for article in articles:
        title = article.find('h2').text.strip()
        link = article['href']
        if not link.startswith('http'):
            parsed_url = urlparse(url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            link = base_url + link
        description = article.find('p').text.strip()

        results.append({
            'title': title,
            'link': link,
            'description': description
        })

    return results