import os
from promptflow.core import tool
from promptflow.connections import CustomConnection
from mistralai import Mistral

@tool
def mistral_connection(
    connection: CustomConnection,
    prompt: list,
    model_name: str,
    temperature: float = None,
    max_tokens: int = None,
    top_p: float = None
) -> str:
    """
    Connects to the Mistral API using the provided custom connection and sends a chat completion request.

    Args:
        connection (CustomConnection): The custom connection object containing the API key.
        prompt (list): A list of messages to be sent to the model. Each message should be a dictionary with 'role' and 'content' keys.
        model_name (str): The name of the model to be used for the completion request.
        temperature (float, optional): Sampling temperature to use. Higher values mean the model will take more risks.
        max_tokens (int, optional): The maximum number of tokens to generate in the completion.
        top_p (float, optional): Nucleus sampling probability. The model considers the results of the tokens with top_p probability mass.

    Returns:
        str: The content of the first message in the response from the Mistral API.

    Example:
        >>> connection = CustomConnection(secrets={'api_key': 'your_api_key'})
        >>> prompt = [{"role": "user", "content": "What is the capital of France?"}]
        >>> mistral_connection(connection, prompt, "model_name")
        'The capital of France is Paris.'
    """
    messages = [
        {
            "role": "system",
            "content": "If the query includes a URL, return 'url_query'. Otherwise return 'question_query'"
        },
        {
            "role": "user",
            "content": prompt,
        },
    ]

    # Authenticate the Mistral API through the custom Mistral connection
    client = Mistral(api_key=connection.secrets['api_key'])

    # Send standard completion request to the API
    response = client.chat.complete(
        messages=messages,
        model=model_name,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p
    )

    return response.choices[0].message.content