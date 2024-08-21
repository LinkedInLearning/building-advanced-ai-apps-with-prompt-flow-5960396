import os
from promptflow.core import tool

@tool
def retrieve_cached_article(classifier: str, article_text: str = None) -> dict:
    """
    Retrieves the cached article text or processes a new article text based on the input parameters.

    Args:
        classifier (str): A classifier string to categorize the article.
        article_text (str, optional): The text of the new article to be processed. Defaults to None.

    Returns:
        dict: A dictionary containing the classifier, chat status, and article text.
            - "classifier" (str): The classifier string provided as input.
            - "chat_status" (bool): Indicates whether the chat is active.
            - "text" (str or None): The article text, either new or cached.

    Example:
        >>> retrieve_cached_article("news", "This is a new article.")
        {'classifier': 'news', 'chat_status': False, 'text': 'This is a new article.'}
        >>> retrieve_cached_article("news")
        {'classifier': 'news', 'chat_status': True, 'text': 'Cached article text'}
        >>> retrieve_cached_article("news")
        {'classifier': 'news', 'chat_status': False, 'text': None}
    """
    # Check if the article_text provided is not empty
    if article_text and article_text != "None":
        # This is a new article. Bypass chat and return the article.
        return {"classifier": classifier, "chat_status": False, "text": article_text}
    else:
        # Check if the temp_cached_article.py file exists
        if os.path.exists("temp_cached_article.py"):
            # Use a dictionary to capture the local variables after exec
            local_vars = {}
            exec(open("temp_cached_article.py").read(), {}, local_vars)
            cached_article_text = local_vars.get("article_text", None)
            # This is a question about a cached article. Send it to chat.
            return {"classifier": classifier, "chat_status": True, "text": cached_article_text}
        else:
            # There is no new article and no cached article. Request an article.
            return {"classifier": classifier, "chat_status": False, "text": None}