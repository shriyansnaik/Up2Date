import dspy
import random

from packages.llms import naikshriyans, shriyansnaik, adityapatil, akshatsharma, glacias, jbeans, somaiya, splitit, shriyansresearch

LMS = [naikshriyans, shriyansnaik, adityapatil, akshatsharma,
       glacias, jbeans, somaiya, splitit, shriyansresearch]

class ExtractSummary(dspy.Signature):
    """Extract a catch title and a short summary from page content of the given article."""

    page_content: str = dspy.InputField()
    title: str = dspy.OutputField(desc="catchy title")
    short_summary: str = dspy.OutputField(
        desc="A short 50 word summary. It should just give a gist of what the article is about.")
    
dspy.configure(lm=LMS[-1])
summarizer = dspy.Predict(ExtractSummary)
    
def summarise_page_content(page_content):
    dspy.configure(lm=random.choice(LMS))
    out = summarizer(page_content=page_content)
    return out.title, out.short_summary

class GenerateTitleForNewsletter(dspy.Signature):
    """Generates a comprehensive title for the newsletter
    from the titles of articles in the newsletter"""

    all_titles: list[str] = dspy.InputField()
    newsletter_title: str = dspy.OutputField(desc="A comprehensive title that captures the top spicy news in one simple line with simple and catchy language")

title_generator = dspy.Predict(GenerateTitleForNewsletter)

def generate_news_letter_title(all_titles):
    dspy.configure(lm=random.choice(LMS))
    out = title_generator(all_titles=all_titles)
    return out.newsletter_title