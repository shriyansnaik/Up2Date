# https://netflixtechblog.medium.com/

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def netflix():
    url="https://netflixtechblog.medium.com/"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    html = response.text

    # Parse the HTML
    soup = BeautifulSoup(html, 'html.parser')

    list_element = soup.select_one("#root > div > div.l.c > div.ab > div.dl.l.dm > div > main > div > div.l.ae > div > div")

    articles = list_element.find_all("div", recursive=False)

    results = []
    # we skip the last article as it is always empty
    articles.pop()
    for article in articles:
        title = article.find("h2").text.strip()
        description = article.find("h3").text.strip()
        link = article.find("a", "ag ah ai aj ak al am an ao ap aq ar as at au")['href']
        if not link.startswith('http'):
            parsed_url = urlparse(url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            link = base_url + link

        results.append({
            'title': title,
            'link': link,
            'description': description
        })

    return results
