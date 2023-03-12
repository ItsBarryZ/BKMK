from src.util import (
    get_website_text,
    chatgpt_query,
    embedding_query,
    get_topk,
    recursive_summarize,
    load_chat_template
)
import json
import os

STORE= 'store.json'


def store_article(url: str, store: str = STORE) -> bool:
    '''
    Given a URL, generates the embedding and appends it to a JSON file.

    Args:
    url (str): The URL of the article to store.
    store (str): The path to the store file. Defaults to 'store.json'.

    Returns:
    bool: True if the article is successfully stored, False otherwise.
    '''
    if os.path.isfile(store):
        print(f"{store} exists!")
    else:
        with open(store, 'w') as f:
            json.dump({"url": [], "embedding": []}, f)

    text = get_website_text(url)
    embedding = embedding_query(text)

    # Load existing data from file, if any
    with open(store, 'r') as f:
        embedding_url_dict = json.load(f)
        urls = embedding_url_dict['url']
        embeddings = embedding_url_dict['embedding']

    if url not in urls:
        # Store the embedding-URL pair in the dictionary
        urls.append(url)
        embeddings.append(embedding)
        embedding_url_dict = {"url": urls, "embedding": embeddings}

        # Save the updated data to the file
        with open(store, 'w') as f:
            json.dump(embedding_url_dict, f)
            
        return True

    return False



def retrieve_article(query: str, store: str = STORE, topk: int = 1) -> list:
    '''
    Given a query, generates the embedding and calls a top-k function to get the top-k results. Uses the index to find
    them in the JSON file and get the URLs.

    Returns False if there are no articles.

    Args:
    query (str): The query to generate an answer for.
    store (str): The path to the store file containing the articles. Defaults to 'store.json'.
    topk (int): The number of most similar embeddings to retrieve.

    Returns:
    list: The list of top-k URLs for the most similar embeddings.
    '''
    if os.path.isfile(store):
        print(f"{store} exists!")
    else:
        return False

    # Generate the embedding for the given query
    embedding = embedding_query(query)

    # Load existing data from file
    with open(store, 'r') as f:
        embedding_url_dict = json.load(f)
        urls = embedding_url_dict['url']
        embeddings = embedding_url_dict['embedding']

    # Find the top-k embeddings that are most similar to the query embedding
    topk_indices = get_topk(embedding, embeddings, topk)

    # Retrieve the URLs for the top-k embeddings
    topk_urls = [urls[i] for i in topk_indices]

    # Return the list of top-k URLs
    return topk_urls


def generate_answer(query: str, store: str = STORE) -> str:
    '''
    Generates an answer to the given query using the articles stored in the provided store.

    Args:
    query (str): The query to generate an answer for.
    store (str): The path to the store file containing the articles. Defaults to 'store.json'.

    Returns:
    str: The generated answer for the query.
    '''
    urls = retrieve_article(query, store, 1)
    print(urls)

    all_text = ""
    for url in urls:
        text = get_website_text(url)
        text = recursive_summarize(text)
        all_text += "article url: {}\n".format(url)
        all_text += text

    message = load_chat_template(
        "SYS_answering",
        "COMMAND_answering",
        "question: {}, articles:{}".format(query, all_text)
    )

    return chatgpt_query(message)


if __name__ == "__main__":
    print(store_article('https://en.wikipedia.org/wiki/Claude_Cr%C3%A9peau'))
