import requests
import re
import os
import numpy as np
from bs4 import BeautifulSoup
import openai


    
prompt_library = {
    "SYS_answering": "You are no longer a chatbot, you are to give concise answers based on the question articles given, if there are no articles, respond with 'I don't think I remember it'",
    "SYS_summarizing": "You are no longer a chatbot, you are to summarize the articles with as much key details included as possible. Make it shorter than the original text",
    "COMMAND_answering": "{}, answer the question using only the articles and tell me which article url was it from",
    "COMMAND_summarizing": "Summarize the article below in fewer words: {}"
}

def load_chat_template(SYS_key: str, COMMAND_key: str, COMMAND_arg: str) -> list:
    """
    Create a list of conversation prompts based on the given keys and argument.

    Parameters:
    - SYS_key (str): the key to the system prompt in the prompt_library dictionary.
    - COMMAND_key (str): the key to the user prompt in the prompt_library dictionary.
    - COMMAND_arg (str): the argument to insert into the COMMAND_key prompt.

    Returns:
    - A list of dictionaries representing the conversation prompts.
    """
    return [
        {"role": "system", "content": prompt_library[SYS_key]},
        {"role": "user", "content": prompt_library[COMMAND_key].format(COMMAND_arg)}
    ]

def chatgpt_query(message: list) -> str:
    """
    Send a list of messages to the GPT-3 Chat model and return the generated response.

    Parameters:
    - message (list): a list of dictionaries representing the conversation prompts.

    Returns:
    - The generated response from the GPT-3 Chat model.
    """
    if os.path.isfile('api_key.txt'):
        with open('api_key.txt') as f:
            openai.api_key = f.readline()

    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message,
    ).choices[0].message.content

def embedding_query(text: str) -> list:
    """
    Generate an embedding for the given text using the OpenAI Text Embedding model.

    Parameters:
    - text (str): the text to generate the embedding for.

    Returns:
    - A list of floats representing the embedding.
    """
    if os.path.isfile('api_key.txt'):
        with open('api_key.txt') as f:
            openai.api_key = f.readline()
    return openai.Embedding.create(
        model='text-embedding-ada-002', 
        input=text[:30000])["data"][0]["embedding"]

def recursive_summarize(text):
    '''
    Recursively summarize a long text by dividing it into smaller segments and summarizing each of them.

    Parameters:
    text (str): The text to be summarized.

    Returns:
    str: The summarized text.
    '''
    if len(text) < 12000:
        return text
    else:
        # Divide the text into segments of roughly equal length
        segment_length = len(text) // ((len(text) // 20000) + 1)
        segments = [text[i:i+segment_length] for i in range(0, len(text), segment_length)]

        # Summarize each segment recursively
        summarized_segments = []
        for segment in segments:
            message = load_chat_template("SYS_summarizing", "COMMAND_summarizing", (segment))
            summarized_segment = chatgpt_query(message)
            summarized_segments.append(summarized_segment)
        # Combine the summarized segments and return the result
        return recursive_summarize(''.join(summarized_segments))


def get_website_text(url):
    '''
    Extract the text content from a website by making an HTTP GET request.

    Parameters:
    url (str): The URL of the website.

    Returns:
    str: The text content of the website.
    '''
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    main_content = soup.find('body')
    text = ' '.join([p.get_text() for p in main_content.find_all('p')])
    return text


def get_topk(query_embedding, all_embeddings, k):
    '''
    Given a query embedding and a list of all embeddings, return
    the top k embeddings that are most similar to the query
    embedding, using dot product as the similarity metric.

    Parameters:
    query_embedding (list): The embedding of the query.
    all_embeddings (list): The list of all embeddings.
    k (int): The number of top embeddings to return.

    Returns:
    list: The indices of the top k embeddings.
    '''
    # Compute the dot product between the query embedding and all embeddings
    dot_products = [np.dot(query_embedding, np.array(e, dtype=float)) for e in all_embeddings]

    # Sort the dot products in descending order and return the top k indices
    topk_indices = np.argsort(dot_products)[::-1][:k]

    return topk_indices
