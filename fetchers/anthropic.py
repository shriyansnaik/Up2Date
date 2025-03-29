# https://alignment.anthropic.com/
import requests
from bs4 import BeautifulSoup
import re

def anthropic(url="https://alignment.anthropic.com/"):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    html = response.text
    
    # Parse the HTML
    soup = BeautifulSoup(html, 'html.parser')

    list_element = soup.select_one("body > div > div.toc")

    articles = list_element.find_all("a")

    results = []
    for article in articles:
        title = article.find('h3').text.strip()
        link = article['href']
        if not link.startswith('http'):
            link = url + link
        description = article.find('div', 'description').text.strip()
        description = re.sub(r'\s+', ' ', description)

        results.append({
            'title': title,
            'link': link,
            'description': description
        })

    return results