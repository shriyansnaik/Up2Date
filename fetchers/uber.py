# https://www.uber.com/en-IN/blog/engineering/ai/
# https://www.uber.com/en-IN/blog/engineering/data/

import requests
import re
from urllib.parse import urlparse

def uber_ai():
    url="https://www.uber.com/en-IN/blog/engineering/ai/"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0'
    }
    response = requests.get(url, headers=headers)
    html = response.text

    start_index = html.find("[{\\u0022id\\u0022:0")
    end_index = html[start_index:].find("\\u0022}}]")

    target_string = html[start_index:start_index+end_index] + "\\u0022}}]"
    cleaned_string = target_string.replace("\\u0022", "")

    pattern = r'props:{footer:([^,]+),.*?href:(\/[^,]+),.*?title:([^}]+)'

    matches = re.findall(pattern, cleaned_string)

    results = []
    for date, link, title in matches:
        if not link.startswith('http'):
            parsed_url = urlparse(url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            link = base_url + link
        results.append({
            'title': title,
            'link': link,
            'description': date
        })

    return results

def uber_data():
    url="https://www.uber.com/en-IN/blog/engineering/data/"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0'
    }
    response = requests.get(url, headers=headers)
    html = response.text

    start_index = html.find("[{\\u0022id\\u0022:0")
    end_index = html[start_index:].find("\\u0022}}]")

    target_string = html[start_index:start_index+end_index] + "\\u0022}}]"
    cleaned_string = target_string.replace("\\u0022", "")

    pattern = r'props:{footer:([^,]+),.*?href:(\/[^,]+),.*?title:([^}]+)'

    matches = re.findall(pattern, cleaned_string)

    results = []
    for date, link, title in matches:
        if not link.startswith('http'):
            parsed_url = urlparse(url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            link = base_url + link
        results.append({
            'title': title,
            'link': link,
            'description': date
        })

    return results
