import pandas as pd
from textblob import TextBlob
from nltk.corpus import stopwords
import re
from transformers import pipeline
import os
import shutil

def clean_text(text):
    """Remove punctuation, stopwords, and return lowercase text."""
    stopwords_set = set(stopwords.words('english'))
    text = re.sub(r'[^\w\s]', '', text.lower())
    text = ' '.join([word for word in text.split() if word not in stopwords_set])
    return text

def paraphrase_text(text, article_index):
    """Paraphrase the given text using a pre-trained language model."""
    paraphraser = pipeline("text2text-generation", model="t5-base", tokenizer="t5-base", framework="pt")
    paraphrased_text = paraphraser(text, max_length=1000, do_sample=True, top_p=0.9, num_return_sequences=1)[0]['generated_text']
    
    # Save the paraphrased article to a file
    output_folder = "Articles Paraphrased"
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, f"article_{article_index}.txt")
    with open(output_file, "w") as file:
        file.write(paraphrased_text)
    
    return paraphrased_text

def analyze_sentiment(text, article_index):
    """Return a polarity score for the text."""
    paraphrased_text = paraphrase_text(text, article_index)
    blob = TextBlob(clean_text(paraphrased_text))
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
    
    # Clear the output folder
    output_folder = "Articles Paraphrased"
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    
    df['ArticleSentiment'] = df.apply(lambda row: analyze_sentiment(row[article_column], row.name), axis=1)
    df['AdjustedPerformanceScore'] = base_performance_score + df['ArticleSentiment'] * 100  # Scale factor adjustment
    return df