import hashlib
import json
import os
import requests
from bs4 import BeautifulSoup
import feedgenerator
from typing import Dict, List, Tuple, Any

# Assuming these are available in the same paths
from packages.dspy_utils import FeedParserForHTML
from packages.helper import get_list, get_text, get_link

# Path for the JSON storage file
JSON_STORAGE_FILE = "url_mappings.json"

# Initialize the FeedParser
feed_parser_html = FeedParserForHTML()

def load_mappings() -> Tuple[Dict[str, Dict[str, Any]], Dict[str, str]]:
    """Load URL mappings from JSON file"""
    if not os.path.exists(JSON_STORAGE_FILE):
        return {}, {}
    
    try:
        with open(JSON_STORAGE_FILE, 'r') as f:
            data = json.load(f)
            return data.get('url_mappings', {}), data.get('original_url_to_hash', {})
    except (json.JSONDecodeError, FileNotFoundError):
        return {}, {}

def save_mappings(url_mappings: Dict[str, Dict[str, Any]], original_url_to_hash: Dict[str, str]) -> None:
    """Save URL mappings to JSON file"""
    data = {
        'url_mappings': url_mappings,
        'original_url_to_hash': original_url_to_hash
    }
    
    with open(JSON_STORAGE_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_rss_data(soup: BeautifulSoup, parsed_data: List, original_url: str, feed) -> None:
    """Extract and add RSS data to the feed"""
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

def generate_rss(url: str) -> str:
    """Generate a hash for a given website URL and store its parsed data"""
    url_mappings, original_url_to_hash = load_mappings()
    
    try:
        # Check if this URL has already been processed
        if url in original_url_to_hash:
            url_hash = original_url_to_hash[url]
            return url_hash

        # Fetch the URL
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        html = response.text

        if response.status_code != 200:
            return "Failed to fetch the URL"
        
        parsed_data = feed_parser_html(original_html=html).parsed_data
        if not parsed_data:
            return f"Cannot generate RSS for: {url}"
            
        # Generate a hash from the URL
        url_hash = hashlib.md5(url.encode()).hexdigest()[:10]

        # Store the mapping
        url_mappings[url_hash] = {
            "original_url": url,
            "parsed_data": parsed_data
        }
        
        # Store the reverse mapping
        original_url_to_hash[url] = url_hash
        
        # Save to JSON file
        save_mappings(url_mappings, original_url_to_hash)

        return url_hash

    except Exception as e:
        return f"Error generating RSS: {str(e)}"

def remove_url(url: str) -> Dict[str, str]:
    """Remove a URL from the storage"""
    url_mappings, original_url_to_hash = load_mappings()
    
    try:
        # Check if URL exists in our system
        if url not in original_url_to_hash:
            return {"message": "URL not found in the system"}
        
        # Get the hash for this URL
        url_hash = original_url_to_hash[url]
        
        # Remove from both dictionaries
        del url_mappings[url_hash]
        del original_url_to_hash[url]
        
        # Save changes to JSON file
        save_mappings(url_mappings, original_url_to_hash)
        
        return {
            "message": f"URL {url} has been removed successfully",
            "removed_url": url
        }
    
    except Exception as e:
        return {"message": f"Error removing URL: {str(e)}"}

def get_rss_feed(url: str) -> str:
    """Generate and return the RSS feed XML for a given URL directly"""
    url_mappings, original_url_to_hash = load_mappings()
    
    # Check if URL exists in the system, if not, generate it
    if url not in original_url_to_hash:
        generate_rss(url)
        # Reload mappings to get the newly saved data
        url_mappings, original_url_to_hash = load_mappings()
        
        # If still not found after generation attempt, return error
        if url not in original_url_to_hash:
            return "Could not generate RSS feed for this URL"
    
    # Get the hash for this URL
    url_hash = original_url_to_hash[url]
    
    # Get the mapping data
    mapping = url_mappings[url_hash]
    original_url = mapping["original_url"]
    parsed_data = mapping["parsed_data"]

    # Fetch the latest URL content
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(original_url, headers=headers)

    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    if response.status_code != 200:
        return "Failed to fetch the URL content"

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

    # Return just the XML content
    return xml_content

def list_feeds() -> Dict:
    """List all the RSS feeds stored in the system"""
    url_mappings, _ = load_mappings()
    
    # Create a list of all mappings
    feeds = []
    for url_hash, mapping in url_mappings.items():
        feeds.append({
            "original_url": mapping["original_url"],
            "hash": url_hash
        })

    return {
        "total_feeds": len(feeds),
        "feeds": feeds
    }

def main():
    """Main function to demonstrate usage"""
    print("RSS Feed Generator (Simplified version)")
    print("Available functions:")
    print("1. get_rss_feed(url) - Get RSS feed XML for any URL")
    print("2. remove_url(url) - Remove a URL from storage")
    print("3. list_feeds() - List all stored feeds")
    
    # Example usage
    # url = "https://example.com"
    # xml = get_rss_feed(url)
    # print(xml)
    
if __name__ == "__main__":
    main()