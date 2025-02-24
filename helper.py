import re
import feedparser
import requests
from bs4 import BeautifulSoup
import random
import time
from tqdm import tqdm
import dspy
import os

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from lm import naikshriyans, shriyansnaik, adityapatil, akshatsharma, glacias, jbeans, somaiya, splitit, shriyansresearch


LMS = [naikshriyans, shriyansnaik, adityapatil, akshatsharma,
       glacias, jbeans, somaiya, splitit, shriyansresearch]


def linkParser(link):
    match = re.search(r"url=([^&]+)", link)
    if not match:
        return ""
    if "youtube" in match.group(1):
        return ""
    return match.group(1)


def fetchGoogleAlert(google_alert_link):
    feed = feedparser.parse(google_alert_link)

    alert_results = [{"title": entry.title, "link": linkParser(
        entry.link)} for entry in feed.entries if linkParser(entry.link)]
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

    title = soup.find('h1').get_text(
        strip=True) if soup.find('h1') else 'No Title Found'

    text = ' '.join([p.get_text(strip=True) for p in soup.find_all('p')])

    return {
        'title': title,
        'text': text
    }


class ExtractSummary(dspy.Signature):
    """Extract summary from text."""

    text: str = dspy.InputField()
    summary: str = dspy.OutputField(
        desc="A short 50 word summary. It should just give a gist of what the article is about.")


dspy.configure(lm=LMS[-1])
summarizer = dspy.Predict(ExtractSummary)


def summarizeContent(parsed_contents):
    for i, content in tqdm(enumerate(parsed_contents), total=len(parsed_contents)):
        lm_to_use = i % len(LMS)
        dspy.configure(lm=LMS[lm_to_use])

        text = content['content']['text']
        summary = summarizer(text=text).summary
        content['summary'] = summary

    return parsed_contents

def format_newsletter_content(alerts):
    
    html_content = """
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h2 { color: #2a9d8f; }
            p { font-size: 16px; line-height: 1.5; color: #333; }
            .content-block { border-bottom: 1px solid #ddd; padding-bottom: 15px; margin-bottom: 20px; }
            a { text-decoration: none; color: #0077cc; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <h1>📰 AI Agents Alert Digest</h1>
        <p>Here's a summary of the latest articles related to AI agents.</p>
    """
    
    for alert in alerts:
        html_content += f"""
        <div class="content-block">
            <h2><a href="{alert['link']}" target="_blank">{alert['content']['title']}</a></h2>
            <p>{alert['summary']}</p>
        </div>
        """
    
    return html_content

def send_email(to_email, subject, body, smtp_server='smtp.gmail.com', smtp_port=587):
    from_email = os.environ['SENDER_EMAIL']
    password = os.environ['SENDER_EMAIL_PASSWORD']  

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))
    
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls() 
        server.login(from_email, password)

        server.sendmail(from_email, to_email, msg.as_string())
        print(f"Email sent successfully to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        server.quit()