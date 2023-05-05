import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import TweetTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

# Load the dataset
df = pd.read_csv('/users/w1761877/Downloads/Tweets/TweetDataset1.csv')

# define columns to preprocess
columns = ['description', 'text', 'hashtags']

# define preprocessing function
def preprocess(text):
    if not text:
        return ""
    # Remove URLs, usernames, and hashtags
    text = re.sub(r"http\S+|www\S+|https\S+|t\.co\S+|\@[a-zA-Z0-9_]+|\#[a-zA-Z0-9_]+", "", text)
    
    # Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))
    
    # Tokenize the text
    tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)
    tokens = tokenizer.tokenize(text)
    
    # Remove stop words and stem the words
    stemmer = PorterStemmer()
    words = [stemmer.stem(word) for word in tokens if word not in stopwords.words('english')]
    
    # Join the words back into a sentence
    processed_text = ' '.join(words)
    
    return processed_text

# preprocess columns and combine into one list
processed_tweets = []
for column in columns:
    tweets = df[column].tolist()
    processed_tweets += [preprocess(tweet) for tweet in tweets]

# print out preprocessed tweets to check for empty strings
for tweet in processed_tweets:
    print(tweet)

# remove empty documents
processed_tweets = [tweet for tweet in processed_tweets if tweet]

if not processed_tweets:
    raise ValueError("All documents are empty after preprocessing")

# Vectorize the text data
vectorizer = TfidfVectorizer(max_features=1000, min_df=5, max_df=0.7)
X = vectorizer.fit_transform(processed_tweets).toarray()

# Save the preprocessed data to a CSV file
df_processed = pd.DataFrame(X, columns=vectorizer.get_feature_names())
df_processed.to_csv('/users/w1761877/Downloads/processed_tweets.csv', index=False)
print ("{Preprocessing Successful")
