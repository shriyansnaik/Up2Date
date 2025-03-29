# https://writingmate.ai/blog

import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

def writingmate():
    url="https://writingmate.ai/blog"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    html = response.text

    # Parse the HTML
    soup = BeautifulSoup(html, 'html.parser')

    # get the first article separately from the hero section
    article_1 = soup.find('a', "framer-RsvLW framer-71KHQ framer-IMWXn framer-1g3gwbn framer-v-oxyta5 framer-11vkiv1")
    title_1 = article_1.find('h2').text.strip()
    link_1 = article_1['href']
    if not link_1.startswith('http'):
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        link_1 = base_url + link_1
    description_1 = article_1.find('p').text.strip()
    article_1 = {
        'title': title_1,
        'link': link_1,
        'description': description_1
    }

    list_element = soup.select_one("#blog > div.framer-1ksll40 > div")

    articles = list_element.find_all("div", "ssr-variant hidden-1xrsf3z", recursive=False)

    results = [article_1]
    for article in articles:
        title = article.find('h1').text.strip()
        link = article.find('a')['href']
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