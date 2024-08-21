from promptflow.core import tool

@tool
def cache_article(article_text: str) -> str:
    """
    Caches the given article text into a temporary Python file.

    Args:
        article_text (str): The text of the article to be cached.

    Returns:
        str: The same article text that was provided as input.

    Example:
        >>> cache_article("This is a sample article text.")
        "This is a sample article text."
    """
    # Define filename
    filename = "temp_cached_article.py"

    # Content to be written to the .py file
    py_content = f'article_text = """{article_text}"""\n'

    # Write the content to the .py file
    with open(filename, 'w') as file:
        file.write(py_content)

    return article_text