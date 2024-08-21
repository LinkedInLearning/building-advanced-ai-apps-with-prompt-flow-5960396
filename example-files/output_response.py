from promptflow.core import tool

@tool
def output_response(cached_article: dict = {"chat_status": False, "text": None}, chat: str = None) -> str:
    """
    Determines the appropriate response based on the cached article status and chat input.

    Args:
        cached_article (dict): A dictionary containing the status and text of the cached article.
            - "chat_status" (bool): Indicates whether the chat is active.
            - "text" (str or None): The cached article text.
        chat (str, optional): The chat input provided by the user.

    Returns:
        str: The appropriate response based on the input conditions.

    Example:
        >>> output_response({"chat_status": False, "text": "Cached article text"}, None)
        'Cached article text'
        >>> output_response({"chat_status": False, "text": None}, None)
        'Please paste in the link to the article you want to talk about!'
        >>> output_response({"chat_status": True, "text": "Cached article text"}, "User chat message")
        'User chat message'
        >>> output_response({"chat_status": True, "text": "Cached article text"}, None)
        'Invalid input.'
    """
    # If cached_article.chat_status is False and cached_article.text is not None
    if not cached_article.get("chat_status") and cached_article.get("text"):
        return cached_article.get("text", "")
    
    # If cached_article.chat_status is False and cached_article.text is None
    if not cached_article.get("chat_status") and not cached_article.get("text"):
        return "Please paste in the link to the article you want to talk about!"

    # If cached_article.chat_status is True and chat has data
    if cached_article.get("chat_status") and chat:
        return chat

    # Fallback in case the inputs don't match any condition
    return "Invalid input."