import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from gensim import corpora, models
import pandas as pd
from collections import Counter
# nltk.download('punkt')
# nltk.download('stopwords')

def preprocess_titles(titles):
    # Tokenize, convert to lowercase, and remove stopwords
    stop_words = set(stopwords.words('english'))
    customize = set(["mobile","edge","computing","mec"])
    customized_stop_words = stop_words.union(customize)
    preprocessed_titles = [word_tokenize(title.lower()) for title in titles]
    preprocessed_titles = [[word for word in title if word.isalnum() and word not in customized_stop_words] for title in preprocessed_titles]

    return preprocessed_titles

def create_corpus(preprocessed_titles):
    # Create a dictionary and bag-of-words corpus
    dictionary = corpora.Dictionary(preprocessed_titles)
    corpus = [dictionary.doc2bow(title) for title in preprocessed_titles]

    return dictionary, corpus

def run_lda(corpus, dictionary, num_topics):
    lda_model = models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=20)
    topics = lda_model.print_topics(num_topics=num_topics)

    return topics

def extract_hot_topics(topics):
    for topic in topics:
        print(topic)

# Example usage
df = pd.read_csv(r'./test.csv')
titles = df["title"].to_list()

preprocessed_titles = preprocess_titles(titles)
dictionary, corpus = create_corpus(preprocessed_titles)
topics = run_lda(corpus, dictionary, num_topics=10)
extract_hot_topics(topics)