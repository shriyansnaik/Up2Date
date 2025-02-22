import re
import feedparser
import requests
from bs4 import BeautifulSoup
import random
import time
from tqdm import tqdm
import dspy

def linkParser(link):
    match = re.search(r"url=([^&]+)", link)
    if not match:
        return ""
    if "youtube" in match.group(1):
        return ""
    return match.group(1)
    
    
def fetchGoogleAlert(google_alert_link):
    feed = feedparser.parse(google_alert_link)

    alert_results = [{"title": entry.title, "link": linkParser(entry.link)} for entry in feed.entries if linkParser(entry.link)]
    return alert_results

def getLinkContent(google_alert_data):
    raw_contents = []
    for alert in tqdm(google_alert_data):
        content, status_code = fetchArticleHTML(alert['link'])

        if not status_code or status_code != 200:
            continue
        
        raw_contents.append({"content": content, "link": alert['link']})

    return raw_contents

def fetchArticleHTML(article_link, min_delay=2, max_delay=5):
    try:
        # Introduce random delay between requests
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
        
        response = requests.get(article_link, timeout=5)
        if response.status_code != 200:
            return "", response.status_code
        
        return response.text, response.status_code
    
    except requests.exceptions.Timeout:
        return "", "timeout"
    
    except requests.exceptions.RequestException as e:
        return "", "something else"

def parseLinkContent(raw_contents):
    for raw_content in tqdm(raw_contents):
        parsed_content = parseLinkContentHelper(raw_content['content'])
        raw_content['content'] = parsed_content
    
    return raw_contents

def parseLinkContentHelper(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')

    title = soup.find('h1').get_text(strip=True) if soup.find('h1') else 'No Title Found'

    text = ' '.join([p.get_text(strip=True) for p in soup.find_all('p')])

    return {
        'title': title,
        'text': text
    }

lm = dspy.LM('llama-3.3-70b-versatile',
             api_key='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',
             api_base='https://api.groq.com/openai/v1')
dspy.configure(lm=lm)

class ExtractSummary(dspy.Signature):
    """Extract summary from text."""

    text: str = dspy.InputField()
    summary: str = dspy.OutputField(desc="a short 50 word summary covering all the essential information")

summarizer = dspy.Predict(ExtractSummary)

def summarizeContent(parsed_contents):
    for content in parsed_contents:
        text = content['content']['text']
        summary = summarizer(text=text)
        content['summary'] = summary

    return parsed_contents