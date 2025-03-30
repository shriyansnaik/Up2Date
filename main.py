from tqdm import tqdm
import time
import random

from packages.firebase_helper import fetch_and_delete_firestore_links
from packages.subscribers_details import subscriber_details
from packages.utils import link_parser, fetch_page_content, format_newsletter, send_email
from packages.ai import summarise_page_content, generate_news_letter_title

print("Execution started...")
alert_links = fetch_and_delete_firestore_links()
print("Alerts data fetched from firestore...")

for alert_keyword, links in alert_links.items():
    details = subscriber_details.get(alert_keyword, None)
    if not details:
        print(f"Skipping '{alert_keyword}'\nAdd subscriber details in packages/subscriber_details.py")
        continue

    newsletter_name, mailing_list = details['name'], details['subscribers']
    publish = details.get("publish", False)

    print(f"Generating newletter for {newsletter_name}")
    articles = []
    links = list(set(links))
    for link in tqdm(links):
        article = {}
        link = link_parser(link)
        if not link:
            continue

        page_content = fetch_page_content(link)
        if not page_content:
            continue

        title, summary = summarise_page_content(page_content)

        article['title'] = title
        article['summary'] = summary
        article['link'] = link

        articles.append(article)

        # to avoid rate limit from fetching
        time.sleep(random.uniform(2, 5))


    list_of_titles = [article['title'] for article in articles]
    newsletter_title = generate_news_letter_title(list_of_titles)

    newsletter = format_newsletter(newsletter_name=newsletter_name,
                                   newsletter_title=newsletter_title,
                                   articles=articles)

    print("Sending emails to subscribers")
    for subscriber_email in mailing_list:
        send_email(subscriber_email=subscriber_email,
                   newsletter_title=newsletter_title,
                   newsletter=newsletter)
    

    # if publish is true, upload to firebase from 
    # where shriyansnaik.vercel.app will pull it and display