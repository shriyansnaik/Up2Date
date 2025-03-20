from helper import fetchGoogleAlert, getLinkContent, parseLinkContent, summarizeContent, format_newsletter_content, send_email, format_kaveri_newsletter_content
import os

rss_feed_url = 'https://www.google.co.in/alerts/feeds/14281887962566473241/7938470061037680642'

google_alert_data = fetchGoogleAlert(rss_feed_url)

raw_contents = getLinkContent(google_alert_data)

parsed_contents = parseLinkContent(raw_contents)

summarised_contents = summarizeContent(parsed_contents)

html_formatted_newsletter = format_newsletter_content(summarised_contents)

mailing_list = os.getenv("AGENT_MAIL_LIST").split(",")

for email in mailing_list:
    send_email(email,
               "Daily AI Agents Digest",
               html_formatted_newsletter)

rss_feed_url = "https://www.google.co.in/alerts/feeds/14281887962566473241/5523182970888272628"

google_alert_data = fetchGoogleAlert(rss_feed_url)

raw_contents = getLinkContent(google_alert_data)

parsed_contents = parseLinkContent(raw_contents)

summarised_contents = summarizeContent(parsed_contents)

mailing_list = os.getenv("KAVERI").split(",")

html_formatted_newsletter = format_kaveri_newsletter_content(summarised_contents)

for email in mailing_list:
    send_email(email,
               "Indian Equity Market News",
               html_formatted_newsletter)