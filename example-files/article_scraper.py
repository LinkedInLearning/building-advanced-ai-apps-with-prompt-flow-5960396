import requests
from bs4 import BeautifulSoup
import json
from promptflow.core import tool

@tool
def article_scraper(url: str) -> str:
    """
    Scrapes the given URL to extract the title, publishing date, and main text of the article.

    Args:
        url (str): The URL of the article to be scraped.

    Returns:
        str: A JSON-formatted string containing the article's title, publishing date, and main text.
        If the page fails to load, an error message is returned instead.

    Example:
        >>> article_scraper('https://example.com/article')
        {
            "title": "Example Article Title",
            "publishing_date": "2024-08-14",
            "main_text": "This is the main content of the article..."
        }
    """
    # Set the headers to mimic a request from a browser to avoid being blocked
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # Send a GET request to the specified URL
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code != 200:
        return json.dumps({"error": f"Failed to retrieve the page, Status Code: {response.status_code}"})

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the title of the article
    title = soup.find('title').get_text() if soup.find('title') else 'No title found'

    # Attempt to extract the publishing date using common HTML tags and attributes
    date = None
    for date_tag in ['meta[name="pubdate"]', 'meta[property="article:published_time"]', 'time', 'meta[name="date"]']:
        date_element = soup.select_one(date_tag)
        if date_element and date_element.has_attr('content'):
            date = date_element['content']
            break
        elif date_element:
            date = date_element.get_text().strip()
            break

    date = date if date else 'No publishing date found'

    # Extract the main text of the article by joining all paragraph tags
    paragraphs = soup.find_all('p')
    main_text = ' '.join([p.get_text() for p in paragraphs])

    # Compile the extracted information into a dictionary
    article_data = {
        "title": title,
        "publishing_date": date,
        "main_text": main_text
    }

    # Return the article data as a JSON-formatted string
    return json.dumps(article_data, indent=4)