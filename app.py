from flask import Flask, render_template, request, redirect, url_for
from src.api import *

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'secret_key'
API_KEY_FILE = 'api_key.txt'

@app.route('/', methods=['GET', 'POST'])
def home() -> str:
    '''
    Renders the home page of the web application.

    Returns:
    str: The HTML content of the home page.
    '''
    if request.method == 'POST':
        api_key = request.form['api_key']
        
        # Write the API key to the text file
        with open(API_KEY_FILE, 'w') as f:
            f.write(api_key)
        return redirect(url_for('index'))
    
    # Read the API key from the text file, if it exists
    if os.path.exists(API_KEY_FILE):
        with open(API_KEY_FILE, 'r') as f:
            api_key = f.read().strip()
    else:
        api_key = None
    
    return render_template('home.html', api_key=api_key)

@app.route('/urls')
def get_urls() -> str:
    '''
    Renders the page displaying the stored URLs.

    Returns:
    str: The HTML content of the page displaying the stored URLs.
    '''
    if os.path.isfile('store.json'):
        with open('store.json', 'r') as f:
            data = json.load(f)
        # extract the URLs
        urls = data['url']
    else:
        urls = []
    return render_template('urls.html', urls=urls)

@app.route('/index', methods=['GET', 'POST'])
def index() -> str:
    '''
    Renders the main page of the web application and handles form submissions.

    Returns:
    str: The HTML content of the main page of the web application.
    '''
    if request.method == 'POST':
        if 'url' in request.form:
            url = request.form['url']
            success = store_article(url)
            if success:
                message = 'Article stored successfully!'
            else:
                message = 'Failed to store article. Article already exists or cannot be indexed'
        elif 'query' in request.form:
            query = request.form['query']
            message = generate_answer(query)
        return render_template('index.html', message=message)

    if os.path.isfile('store.json'):
        with open('store.json', 'r') as f:
            data = json.load(f)
        # extract the URLs
        urls = data['url']
    else:
        urls = []
    return render_template('index.html', urls=urls)

@app.route('/go-to-index')
def go_to_index() -> str:
    '''
    Redirects to the main page of the web application.

    Returns:
    str: A redirect response to the main page of the web application.
    '''
    return redirect(url_for('index'))

@app.route('/go-to-urls')
def go_to_urls() -> str:
    '''
    Redirects to the page displaying the stored URLs.

    Returns:
    str: A redirect response to the page displaying the stored URLs.
    '''
    return redirect(url_for('get_urls'))

if __name__ == '__main__':
     app.run(debug=True)
