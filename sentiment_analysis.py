import pandas as pd
from textblob import TextBlob
from nltk.corpus import stopwords
import re

def clean_text(text):
    """Remove punctuation, stopwords, and return lowercase text."""
    stopwords_set = set(stopwords.words('english'))
    text = re.sub(r'[^\w\s]', '', text.lower())
    text = ' '.join([word for word in text.split() if word not in stopwords_set])
    return text

def analyze_sentiment(text):
    """Return a polarity score for the text."""
    blob = TextBlob(clean_text(text))
    return blob.sentiment.polarity

def load_data(file_path, file_type='csv'):
    """Load baseball data from a file."""
    if file_type == 'csv':
        return pd.read_csv(file_path)
    elif file_type == 'excel':
        return pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file type provided. Use 'csv' or 'excel'.")

def calculate_performance_score(df, runs_column='r'):
    """Calculate the average runs per game as the performance score."""
    df[runs_column] = pd.to_numeric(df[runs_column], errors='coerce')  # Ensure the runs column is numeric
    return df[runs_column].mean()

def compute_performance_scores(df, article_column, base_performance_score):
    """Add/subtract scores based on sentiment analysis of articles."""
    df['ArticleSentiment'] = df[article_column].apply(analyze_sentiment)
    df['AdjustedPerformanceScore'] = base_performance_score + df['ArticleSentiment'] * 100  # Scale factor adjustment
    return df