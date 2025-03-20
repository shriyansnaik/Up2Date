import hashlib
import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
import feedgenerator
from pydantic import BaseModel
from bs4 import BeautifulSoup

from packages.dspy_utils import FeedParserForHTML
from packages.helper import get_list, get_text, get_link

app = FastAPI(title="RSS Feed Generator API")

# In-memory storage for URL mappings
url_mappings = {}
# Dictionary to map original URLs to their hash values for quick lookup
original_url_to_hash = {}

class UrlRequest(BaseModel):
    url: str

feed_parser_html = FeedParserForHTML()


def get_rss_data(soup, parsed_data, original_url, feed):
    for parsed_item in parsed_data:
        list_data, details_data = parsed_item
        title_data, link_data, description_data, date_data = details_data

        item_list = get_list(soup, list_data)
        
        for item in item_list:
            title = get_text(item, title_data)
            link = get_link(item, link_data, original_url)
            description = get_text(item, description_data)
            date = get_text(item, date_data)

            feed.add_item(
                title=title,
                link=link,
                description=description if description else date
            )

@app.get("/")
def read_root():
    return {"message": "Welcome to RSS Feed Generator API"}


@app.post("/generate-rss-url")
def generate_rss_url(request: UrlRequest):
    try:
        # Check if this URL has already been processed
        if request.url in original_url_to_hash:
            url_hash = original_url_to_hash[request.url]
            # Return the existing RSS feed URL
            return {
                "rss_feed_url": f"https://rss-feed-generator.onrender.com/feed/{url_hash}.xml",
                "message": "URL already exists in the system"
            }

        # Fetch the URL
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(request.url, headers=headers)
        html = response.text

        if response.status_code != 200:
            raise HTTPException(
                status_code=400, detail="Failed to fetch the URL")
        
        parsed_data = feed_parser_html(original_html=html).parsed_data
        if not parsed_data:
            raise HTTPException(
            status_code=422, detail=f"Cannot generate RSS for: {request.url}")
        # Generate a hash from the URL
        url_hash = hashlib.md5(request.url.encode()).hexdigest()[:10]

        # Store the mapping
        url_mappings[url_hash] = {
            "original_url": request.url,
            "parsed_data": parsed_data
        }
        
        # Store the reverse mapping
        original_url_to_hash[request.url] = url_hash

        # Generate the RSS feed URL with .xml extension
        rss_feed_url = f"https://rss-feed-generator.onrender.com/feed/{url_hash}.xml"

        return {"rss_feed_url": rss_feed_url}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating RSS URL: {str(e)}")


@app.post("/remove-url")
def remove_url(request: UrlRequest):
    try:
        # Check if URL exists in our system
        if request.url not in original_url_to_hash:
            raise HTTPException(
                status_code=404, detail="URL not found in the system")
        
        # Get the hash for this URL
        url_hash = original_url_to_hash[request.url]
        
        # Remove from both dictionaries
        del url_mappings[url_hash]
        del original_url_to_hash[request.url]
        
        return {
            "message": f"URL {request.url} has been removed successfully",
            "removed_url": request.url
        }
    
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error removing URL: {str(e)}")


@app.get("/feed/{url_hash}.xml")
def get_rss_feed(url_hash: str):
    # Remove .xml from url_hash if it's there
    url_hash = url_hash.replace(".xml", "")

    if url_hash not in url_mappings:
        raise HTTPException(status_code=404, detail="RSS feed not found")

    # Get the original URL and extraction info
    mapping = url_mappings[url_hash]
    original_url = mapping["original_url"]

    parsed_data = mapping["parsed_data"]

    # Fetch the URL content
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(original_url, headers=headers)

    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    if response.status_code != 200:
        raise HTTPException(
            status_code=400, detail="Failed to fetch the original URL")

    # Generate RSS feed
    feed = feedgenerator.Rss201rev2Feed(
        title=f"RSS Feed for {original_url}",
        link=original_url,
        description=f"Auto-generated RSS feed for {original_url}",
        language="en"
    )

    get_rss_data(soup, parsed_data, original_url, feed)

    # Generate the XML content
    xml_content = feed.writeString('utf-8')

    # Return properly formatted XML with correct content type
    return Response(
        content=xml_content,
        media_type="application/xml"
    )


@app.get("/list-feeds")
def list_feeds():
    # Create a list of all mappings
    feeds = []
    for url_hash, mapping in url_mappings.items():
        feeds.append({
            "original_url": mapping["original_url"],
            "rss_feed_url": f"https://rss-feed-generator.onrender.com/feed/{url_hash}.xml"
        })

    return {
        "total_feeds": len(feeds),
        "feeds": feeds
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)