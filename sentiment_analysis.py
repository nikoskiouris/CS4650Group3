import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification
import torch
from nltk.corpus import stopwords
import re
import os
import shutil
import nltk
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

def preprocess_text(text):
    """Preprocess the text by removing stopwords, punctuation, and lemmatizing words."""
    stopwords_set = set(stopwords.words('english'))
    text = re.sub(r'http\S+', '', text)  # Remove URLs
    text = re.sub(r'[^\w\s]', '', text.lower())  # Remove punctuation and lowercase
    words = nltk.word_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words if word not in stopwords_set]
    return ' '.join(words)

def paraphrase_text(text, article_index):
    """Paraphrase the given text using a pre-trained language model."""
    from transformers import pipeline
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
    """Return a polarity score for the text using BERT."""
    paraphrased_text = paraphrase_text(text, article_index)
    
    # Load the pre-trained BERT model and tokenizer
    model_name = 'bert-base-uncased'
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertForSequenceClassification.from_pretrained(model_name, num_labels=2)
    
    # Tokenize the input text
    inputs = tokenizer(preprocess_text(paraphrased_text), padding=True, truncation=True, return_tensors='pt')
    
    # Perform sentiment analysis
    with torch.no_grad():
        outputs = model(**inputs)
        probabilities = torch.softmax(outputs.logits, dim=1)
        positive_prob = probabilities[0][1].item()
    
    polarity = positive_prob * 2 - 1  # Convert probability to polarity score in the range [-1, 1]
    return polarity

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