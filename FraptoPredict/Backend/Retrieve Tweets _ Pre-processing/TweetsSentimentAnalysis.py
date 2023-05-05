import pandas as pd
import nltk
nltk.download('opinion_lexicon')
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
nltk.download('punkt')

nltk.download('stopwords')

df = pd.read_csv('TweetsDataset.csv')

def get_sentiment_score(text):
    positive_words = set(nltk.corpus.opinion_lexicon.positive())
    negative_words = set(nltk.corpus.opinion_lexicon.negative())
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(text.lower())
    filtered_words = [word for word in word_tokens if word not in stop_words]
    positive_score = len(positive_words.intersection(filtered_words))
    negative_score = len(negative_words.intersection(filtered_words))
    sentiment_score = positive_score - negative_score
    return sentiment_score

df['sentiment_score'] = df['tweet'].apply(get_sentiment_score)

df['sentiment'] = df['sentiment_score'].apply(lambda x: 'positive' if x >= 0 else 'negative')

df.to_csv('sentiment_analysis.csv', index=False)
