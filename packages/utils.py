import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import urllib.parse

# email imports
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from packages.templates import newsletter_template, article_template, last_article_template

HEADERS = {
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

def link_parser(link):
    match = re.search(r"url=([^&]+)", link)
    if not match:
        return ""
    
    decoded_url = urllib.parse.unquote(match.group(1))

    if "youtube" in decoded_url:
        return ""
    
    return decoded_url

def remove_extra_spaces_and_linebreaks(text):
    cleaned_text = re.sub(r'\n+', '\n', text)
    cleaned_text = re.sub(r' +', ' ', cleaned_text)
    return cleaned_text

def fetch_page_content(link):
    try:
        res = requests.get(url=link, headers=HEADERS)
        if res.status_code != 200:
            return None
        soup = BeautifulSoup(res.text, 'html.parser')
        body = soup.find('body')
        page_content = remove_extra_spaces_and_linebreaks(body.text)

        return page_content
    except:
        return ""


def format_newsletter(newsletter_name, newsletter_title, articles):
    
    formatted_articles = []
    for i, article in enumerate(articles):
        title = article['title']
        link = article['link']
        summary = article['summary']
        
        if i == len(articles) - 1:
            formatted_article = last_article_template.format(title=title, link=link, summary=summary)
        else:
            formatted_article = article_template.format(title=title, link=link, summary=summary)
        
        formatted_articles.append(formatted_article)
    
    newsletter = newsletter_template.format(
        newsletter_name=newsletter_name,
        newsletter_title=newsletter_title,
        formatted_date=datetime.now().strftime("%A, %B %d, %Y"),
        articles="".join(formatted_articles)
    )
    
    return newsletter


def send_email(subscriber_email, newsletter_title, newsletter):
    smtp_server='smtp.gmail.com'
    smtp_port=587
    
    from_email = os.environ['SENDER_EMAIL']
    password = os.environ['SENDER_EMAIL_PASSWORD']  

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = subscriber_email
    msg['Subject'] = newsletter_title

    msg.attach(MIMEText(newsletter, 'html'))
    
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls() 
        server.login(from_email, password)

        server.sendmail(from_email, subscriber_email, msg.as_string())
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        server.quit()
