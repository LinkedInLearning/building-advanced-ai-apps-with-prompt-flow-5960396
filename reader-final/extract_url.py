import re
from promptflow.core import tool

@tool
def extract_url(text: str) -> str:
    """
    Extracts the first URL found in the given text.

    Args:
        text (str): The input text from which to extract the URL.

    Returns:
        str: The first URL found in the text. If no URL is found, returns None.

    Example:
        >>> extract_url("Check out this link: https://example.com and let me know what you think.")
        'https://example.com'
    """
    # Regular expression pattern for matching URLs
    url_pattern = r'(https?://[^\s]+)'

    # Search for the first match in the input text
    match = re.search(url_pattern, text)

    # Return the matched URL or None if no URL is found
    return match.group(0) if match else None