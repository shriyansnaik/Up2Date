# https://bytes.swiggy.com/tagged/swiggy-data-science

import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

def swiggy():
    url="https://bytes.swiggy.com/tagged/swiggy-data-science"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    html = response.text

    # Parse the HTML
    soup = BeautifulSoup(html, 'html.parser')

    list_element = soup.find("div", "js-tagStream")

    articles = list_element.find_all("div", recursive=False)

    results = []
    for article in articles:
        title = article.find('h3').text.strip()
        link = article.find('a', 'link link--darken')['href']
        if not link.startswith('http'):
            parsed_url = urlparse(url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            link = base_url + link
        description = article.find('time').text.strip()

        results.append({
            'title': title,
            'link': link,
            'description': description
        })

    return results
