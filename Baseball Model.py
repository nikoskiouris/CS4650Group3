import pandas as pd
from textblob import TextBlob
from nltk.corpus import stopwords
import re

# Function to clean text data
def clean_text(text):
    """Remove punctuation, stopwords, and return lowercase text."""
    stopwords_set = set(stopwords.words('english'))
    text = re.sub(r'[^\w\s]', '', text.lower())
    text = ' '.join([word for word in text.split() if word not in stopwords_set])
    return text

# Function to analyze sentiment
def analyze_sentiment(text):
    """Return a polarity score for the text."""
    blob = TextBlob(clean_text(text))
    return blob.sentiment.polarity

# Load your dataset
def load_data(file_path, file_type='csv'):
    """Load baseball data from a file."""
    if file_type == 'csv':
        return pd.read_csv(file_path)
    elif file_type == 'excel':
        return pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file type provided. Use 'csv' or 'excel'.")

# Calculate team performance score as average runs
def calculate_performance_score(df, runs_column='r'):
    """Calculate the average runs per game as the performance score."""
    df[runs_column] = pd.to_numeric(df[runs_column], errors='coerce')  # Ensure the runs column is numeric
    return df[runs_column].mean()

# Function to compute performance scores from articles
def compute_performance_scores(df, article_column, base_performance_score):
    """Add/subtract scores based on sentiment analysis of articles."""
    df['ArticleSentiment'] = df[article_column].apply(analyze_sentiment)
    df['AdjustedPerformanceScore'] = base_performance_score + df['ArticleSentiment'] * 100  # Scale factor adjustment
    return df

# Example usage:
# Load the team data
team_data_2010 = load_data('Data\Atlanta Falcons Batting Data 2010.xlsx', 'excel')
team_data_2020 = load_data('Data\Atlanta Falcons Batting Data 2020.xlsx', 'excel')

# Calculate initial and final performance scores
initial_score_2010 = calculate_performance_score(team_data_2010, 'r')
final_score_2020 = calculate_performance_score(team_data_2020, 'r')

# Load article data and adjust performance score based on sentiment
#article_data = load_data('path_to_articles.csv', 'csv')
#adjusted_df = compute_performance_scores(article_data, 'Article', initial_score_2010)

# Now you can compare initial_score_2010, final_score_2020, and adjusted performance scores
print("Initial Score 2010:", initial_score_2010)
print("Final Score 2020:", final_score_2020)
#print("Adjusted Performance Scores:")
#print(adjusted_df[['ArticleSentiment', 'AdjustedPerformanceScore']])
