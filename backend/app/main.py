from fastapi import FastAPI
from pydantic import BaseModel
import re
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import string
import pandas as pd
from wordcloud import WordCloud
from heapq import nlargest
from fastapi.middleware.cors import CORSMiddleware

# Download necessary resources
nltk.download("stopwords")
nltk.download("punkt")

# Initialize FastAPI
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define stopwords and punctuation
stop_words = set(stopwords.words("english"))
punctuation = string.punctuation

# Define request model
class TextRequest(BaseModel):
    article: str

# Function to clean and preprocess text
def preprocess_article(article):
    article = article.lower()
    article = re.sub(r"<.*?>", "", article)  # Remove HTML
    article = re.sub(r"\S+@\S+", "", article)  # Remove emails
    article = re.sub(r"http\S+|www\S+|ftp\S+", "", article)  # Remove URLs
    article = "".join(char if char not in punctuation else " " for char in article)
    article = re.sub(r"\s+", " ", article).strip()  # Remove extra spaces
    words = word_tokenize(article)
    filtered_words = [word for word in words if word not in stop_words]
    return " ".join(filtered_words)

# Function to normalize the word frequency
def normalize(li_word):
    normalized_freq = []
    for dictionary in li_word:
        if dictionary:  # Avoid division by zero
            max_frequency = max(dictionary.values())
            for word in dictionary.keys():
                dictionary[word] /= max_frequency
        normalized_freq.append(dictionary)
    return normalized_freq

# Function to calculate the word frequency
def word_frequency(article_word):
    word_frequency_list = []
    for sentence in article_word:
        word_frequency = {}
        for word in word_tokenize(sentence):
            word_frequency[word] = word_frequency.get(word, 0) + 1
        word_frequency_list.append(word_frequency)
    return normalize(word_frequency_list)

# Function to score sentences
def sentence_score(sentence_list, normalized_freq):
    sentence_score_list = []
    for list_, dictionary in zip(sentence_list, normalized_freq):
        score_dict = {}
        for sent in list_:
            for word in word_tokenize(sent):
                if word in dictionary:
                    score_dict[sent] = score_dict.get(sent, 0) + dictionary[word]
        sentence_score_list.append(score_dict)
    return sentence_score_list

# Function to tokenize sentences
def sent_token(article_sent):
    sentence_list = []
    for sent in article_sent:
        tokens = sent_tokenize(sent)
        clean_tokens = [''.join(word for word in sentence if word not in punctuation) for sentence in tokens]
        clean_tokens = [re.sub(' +', ' ', sentence) for sentence in clean_tokens]
        sentence_list.append(clean_tokens)
    return sentence_list

# Function to generate the summary
def summary(sentence_scores):
    summary_list = []
    for scores in sentence_scores:
        if scores:
            select_length = max(1, int(len(scores) * 0.25))  # Ensure at least one sentence
            summary_ = nlargest(select_length, scores, key=scores.get)
            summary_list.append(" ".join(summary_))
        else:
            summary_list.append("")  # Handle empty input case
    return summary_list

# Function to summarize an article
def article_summarize(article):
    start_time = time.time()
    
    # Convert article to a Pandas Series
    article_series = pd.Series([article])
    preprocess_time = time.time()
    print(f"Preprocess time: {preprocess_time - start_time}s")

    # Preprocess the article
    preprocessed_articles = article_series.apply(preprocess_article)
    
    # Tokenize sentences
    tokenized_sentences = sent_token(preprocessed_articles)
    
    # Calculate word frequencies
    normalized_frequencies = word_frequency(preprocessed_articles)
    
    # Score sentences
    sentence_scores = sentence_score(tokenized_sentences, normalized_frequencies)
    
    # Generate summary
    summary_result = summary(sentence_scores)
    end_time = time.time()
    
    print(f"Total processing time: {end_time - start_time}s")
    
    return summary_result

# API route
@app.post("/summarize/")
async def summarize(request: TextRequest):
    summary = article_summarize(request.article)
    return {"summary": summary}
