import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests

def fetch_html(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return ""

    html = response.text
    return html

def clean_html(html_content):
    # Create BeautifulSoup object
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove unwanted tags
    unwanted_tags = ['header', 'footer', 'script', 'style', 'noscript', 'img', 
                     'picture', 'svg', 'canvas', 'video', 'audio', 'iframe',
                     'nav', 'aside', 'meta', 'link', 'head', 'form', 'button',
                     'input', 'select', 'option', 'textarea']
    
    for tag in unwanted_tags:
        for element in soup.find_all(tag):
            element.decompose()
    
    # Convert soup to string
    html_str = str(soup)
    
    # Clean up unnecessary whitespace
    # Remove multiple spaces
    html_str = re.sub(r'\s+', ' ', html_str)
    
    # Remove spaces between tags
    html_str = re.sub(r'>\s+<', '><', html_str)
    
    # Remove spaces at the beginning and end of tags
    html_str = re.sub(r'\s+>', '>', html_str)
    html_str = re.sub(r'<\s+', '<', html_str)
    
    return html_str

def get_text(soup, target):
    target_tag, target_class = target
    
    # find the target tag and class in the soup
    if target_class == '':
        target_element = soup.find(target_tag)
    else:
        target_element = soup.find(target_tag, target_class)

    # check if target element exists
    if target_element:
        return target_element.get_text().strip()

    # check if soup itself has the target tag and class
    if soup.name == target_tag and target_class in soup.get('class', []):
        return soup.get_text().strip()

def get_link(soup, target, original_url):
    target_tag, target_class = target
    
    parsed_url = urlparse(original_url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    # if class is '' so we have to do find all and then return the one with
    # class = ''
    if target_class:
        target_element = soup.find(target_tag, target_class)
    else:
        target_elements = soup.find_all(target_tag)
        target_element = None
        for element in target_elements:
            if element.get("class") == []:
                target_element = element
                break

    if target_element:
        link = target_element['href']
    elif soup.has_attr('href'):
        link = soup['href']
    
    if not link:
        return original_url
    
    if link.startswith('/'):
        link = base_url + link
    elif not link.startswith(('http://', 'https://')):
        link = base_url + '/' + link.lstrip('/')

    return link 

def get_list(soup, target):
    target_tag, target_class = target
    if target_class:
        return soup.find_all(target_tag, target_class)
    return soup.find_all(target_tag)