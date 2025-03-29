# https://news.microsoft.com/source/topics/ai/feed
# https://news.microsoft.com/source/view-all/?_categories=ai

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def microsoft():
    url="https://news.microsoft.com/source/view-all/?_categories=ai"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    html = response.text

    # Parse the HTML
    soup = BeautifulSoup(html, 'html.parser')

    list_element = soup.select_one("#content > div:nth-child(2) > div:nth-child(1) > div > div")

    articles = list_element.find_all("div", recursive=False)

    results = []
    for article in articles:
        title = article.find("div", "fwpl-item el-fz703r h2").text.strip()
        description = article.find("div", "fwpl-item el-37vm0k7 kicker").text.strip()
        link = article.find("a")["href"]
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
