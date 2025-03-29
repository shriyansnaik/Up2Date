# https://deepmind.google/discover/blog/
# https://deepmind.google/research/breakthroughs/

import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

def deepmind_blog(url="https://deepmind.google/discover/blog"):
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    html = response.text

    # Parse the HTML
    soup = BeautifulSoup(html, 'html.parser')

    list_element = soup.select_one("#content > div > gdm-filter > gdm-pagination > ul")

    articles = list_element.find_all("a")

    results = []
    for article in articles:
        title = article.find('p', 'glue-headline glue-headline--headline-5').text.strip()
        link = article['href']
        if not link.startswith('http'):
            parsed_url = urlparse(url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            link = base_url + link
        description = article.find('p', 'glue-card__description').text.strip()

        results.append({
            'title': title,
            'link': link,
            'description': description
        })

    return results

def deepmind_research(url="https://deepmind.google/research/breakthroughs/"):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    html = response.text

    # Parse the HTML
    soup = BeautifulSoup(html, 'html.parser')

    list_element = soup.select_one("#content > div > ul")

    articles = list_element.find_all("a")

    results = []
    for article in articles:
        title = article.find('p', 'glue-headline glue-headline--headline-5').text.strip()
        link = article['href']
        if not link.startswith('http'):
            parsed_url = urlparse(url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            link = base_url + link
        description = article.find('p', 'glue-card__description').text.strip()

        results.append({
            'title': title,
            'link': link,
            'description': description
        })

    return results