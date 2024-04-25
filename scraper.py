import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_article(url):
    """Scrape an article from a given URL."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract the article title
    title = soup.find('h1').text.strip()
    
    # Extract the article text
    article_text = ''
    for paragraph in soup.find_all('p'):
        article_text += paragraph.text.strip() + '\n'
    
    return title, article_text

def load_articles(urls):
    """Load articles from a list of URLs."""
    articles = []
    for url in urls:
        title, text = scrape_article(url)
        articles.append({'Title': title, 'Article': text})
    
    return pd.DataFrame(articles)