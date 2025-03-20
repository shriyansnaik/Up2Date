import dspy
import os
from bs4 import BeautifulSoup
import re

from packages.helper import clean_html

jbeans = dspy.LM("openai/gemini-2.0-flash",
                 api_key=os.environ['GEMINI_API_KEY_JBEANS'],
                 base_url=os.environ['GEMINI_BASE_API']
                 )

dspy.configure(lm=jbeans)


class ExtractClassesFromHTML(dspy.Signature):
    """From the given HTML text, extracts the HTML tag and class 
    for articles, title, link, description and date. If not found, keep empty.
    The classes need to be extracted completely"""
    html_text: str = dspy.InputField()
    article: tuple[str, str] = dspy.OutputField(
        desc="HTML tag and its corresponding class containing the each article")
    title: tuple[str, str] = dspy.OutputField(
        desc="HTML tag and its corresponding class containing the title")
    link: tuple[str, str] = dspy.OutputField(
        desc="HTML tag and its corresponding class containing the link")
    description: tuple[str, str] = dspy.OutputField(
        desc="HTML tag and its corresponding class containing the description")
    date: tuple[str, str] = dspy.OutputField(
        desc="HTML tag and its corresponding class containing the date")


html_extractor = dspy.ChainOfThought(ExtractClassesFromHTML)


###################################################################

class IdentifyListOfContent(dspy.Signature):
    """From the given text, extract titles of content. It will 
    usually be something like publications, articles, blogs etc. 
    These things will usually be accompanied by author name, date, 
    description or something else. If not found, leave empty"""
    text: str = dspy.InputField()
    content_list_titles: list[str] = dspy.OutputField()


class GetContentList(dspy.Signature):
    """Based on the titles of the content list provided, extract 
    HTML tags and the corresponding class of that tag from the html
    for the list item. The classes need to be extracted completely"""

    html: str = dspy.InputField()
    content_list_titles: list[str] = dspy.InputField()
    list_item: list[tuple[str, str]] = dspy.OutputField(
        desc="HTML tag and its corresponding class containing the list item. If there are more than one type of list item, add all")


class ExtractItemDetails(dspy.Signature):
    """Given a few sample items, extracts the HTML tag and its class for 
    the title, the link, the description and the date 
    for a given item. If any detail is not found, 
    leave empty. The classes need to be extracted completely"""

    list_items: list[str] = dspy.InputField()
    title: tuple[str, str] = dspy.OutputField(
        desc="HTML tag and its corresponding class containing the title")
    link: tuple[str, str] = dspy.OutputField(
        desc="HTML tag and its corresponding class containing the link")
    description: tuple[str, str] = dspy.OutputField(
        desc="HTML tag and its corresponding class containing the description")
    date: tuple[str, str] = dspy.OutputField(
        desc="HTML tag and its corresponding class containing the date")


class FeedParserForHTML(dspy.Module):

    def __init__(self):
        self.title_identifier = dspy.ChainOfThought(IdentifyListOfContent)
        self.list_item_extractor = dspy.ChainOfThought(GetContentList)
        self.details_extractor = dspy.ChainOfThought(ExtractItemDetails)

    def process_html(self, original_html):
        html = clean_html(original_html)
        soup = BeautifulSoup(original_html, 'html.parser')
        text = re.sub(r'\n+', '\n', soup.text)

        return html, soup, text

    def forward(self, original_html):
        html, soup, text = self.process_html(original_html)

        content_list_titles = self.title_identifier(
            text=text).content_list_titles
        list_item = self.list_item_extractor(
            html=html, content_list_titles=content_list_titles).list_item

        parsed_data = []
        for item in list_item:
            item_tag, item_class = item
            sample_items = soup.find_all(item_tag, item_class)[:2]
            extracted = self.details_extractor(list_items=sample_items)
            details = (
                extracted.title,
                extracted.link,
                extracted.description,
                extracted.date,
            )
            parsed_data.append([item, details])

        return dspy.Prediction(parsed_data=parsed_data)
