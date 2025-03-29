# https://www.amazon.science/blog?q=&f0=0000016e-2ff0-da81-a5ef-3ff057f10000&s=1&expandedFilters=Research%2520area%2CTag%2CTag%2CTag%2CTag%2CTag%2CTag%2CTag%2CTag%2CTag%2CTag%2CTag%2CTag%2CTag%2CTag%2CTag%2CTag%2CTag%2CTag%2CTag%2CTag%2CTag%2CTag%2CConference%2CConference%2CConference%2CConference%2CConference%2CConference%2CConference%2CConference%2CConference%2CConference%2CConference%2CConference%2CConference%2CAuthor%2CAuthor%2CAuthor%2CAuthor%2CAuthor%2CAuthor%2CAuthor%2CAuthor%2CAuthor%2CAuthor%2CAuthor%2CAuthor%2CAuthor%2CAuthor%2CAuthor%2CAuthor%2CAuthor%2CAuthor%2CAuthor%2CAuthor%2CAuthor%2CAuthor%2CDate%2C
import requests
from bs4 import BeautifulSoup

def amazon(url="https://www.amazon.science/blog?q=&f0=0000016e-2ff0-da81-a5ef-3ff057f10000&s=1&expandedFilters=Research%2520area%2CTag%2CTag%2CTag%2CTag%2CTag%2CTag%2CTag%2CTag%2CTag%2CTag%2CTag%2CTag%2CTag%2CTag%2CTag%2CTag%2CTag%2CTag%2CTag%2CTag%2CTag%2CTag%2CConference%2CConference%2CConference%2CConference%2CConference%2CConference%2CConference%2CConference%2CConference%2CConference%2CConference%2CConference%2CConference%2CAuthor%2CAuthor%2CAuthor%2CAuthor%2CAuthor%2CAuthor%2CAuthor%2CAuthor%2CAuthor%2CAuthor%2CAuthor%2CAuthor%2CAuthor%2CAuthor%2CAuthor%2CAuthor%2CAuthor%2CAuthor%2CAuthor%2CAuthor%2CAuthor%2CAuthor%2CDate%2C"):
    """
    Extracts search results from the given URL.
    
    Args:
        url (str): The URL to fetch and parse
        
    Returns:
        list: A list of dictionaries containing title, link, date, and description
    """
    # Fetch the HTML content
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    html = response.text
    
    # Parse the HTML
    soup = BeautifulSoup(html, 'html.parser')
    
    # Use the CSS selector to get the <ul> element
    ul_element = soup.select_one("body > div:nth-child(4) > main > ps-search-results-module > form > div > ps-search-filters > div > main > ul")
    
    results = []
    
    # Check if the <ul> element was found
    if ul_element:
        # Find all <li> elements inside the <ul>
        li_elements = ul_element.find_all('li')
        
        # Iterate over the <li> elements
        for item in li_elements:
            # Extract title and link
            title_element = item.select_one("div > div.PromoF-title > a")
            title = title_element.text.strip() if title_element else "No title found"
            link = title_element['href'] if title_element and 'href' in title_element.attrs else "No link found"
            
            # Extract date
            date_element = item.select_one("div > div.PromoF-details > div.PromoF-date")
            date = date_element.text.strip() if date_element else "No date found"
            
            # Extract description
            description_element = item.select_one("div > div.PromoF-content > div.PromoF-body > div.PromoF-description")
            description = description_element.text.strip() if description_element else "No description found"
            
            # Add the extracted information to results
            results.append({
                "title": title,
                "link": link,
                "date": date,
                "description": description
            })
    
    return results