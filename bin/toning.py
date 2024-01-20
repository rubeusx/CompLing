from nltk.stem.wordnet import WordNetLemmatizer
from nltk import FreqDist, classify, NaiveBayesClassifier
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
import asyncio
import time

import re, string, random
import pymorphy2


async def get_tone(content):
    morph = pymorphy2.MorphAnalyzer()
    def remove_noise(tweet_tokens, stop_words=()):
        cleaned_tokens = []

        for token, tag in pos_tag(tweet_tokens):
            token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', token)
            token = re.sub("(@[A-Za-z0-9_]+)", "", token)

            pos = morph.parse(token)[0].tag.POS
            if pos:
                if pos.startswith("N"):
                    pos = 'n'
                elif pos.startswith('V'):
                    pos = 'v'
                else:
                    pos = 'a'

                lemmatizer = WordNetLemmatizer()
                token = lemmatizer.lemmatize(token, pos)

            if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
                cleaned_tokens.append(token.lower())

        return cleaned_tokens

    def get_all_words(cleaned_tokens_list):
        for tokens in cleaned_tokens_list:
            for token in tokens:
                yield token

    def get_tweets_for_model(cleaned_tokens_list):
        for tweet_tokens in cleaned_tokens_list:
            yield dict([token, True] for token in tweet_tokens)

    top_words = stopwords.words('russian')

    positive_tweet_tokens = ["позитивный", "текст", "пример"]
    negative_tweet_tokens = ["негативный", "текст", "пример"]

    positive_cleaned_tokens_list = [remove_noise(tokens, top_words) for tokens in [positive_tweet_tokens]]
    negative_cleaned_tokens_list = [remove_noise(tokens, top_words) for tokens in [negative_tweet_tokens]]

    all_pos_words = get_all_words(positive_cleaned_tokens_list)
    freq_dist_pos = FreqDist(all_pos_words)
    #print(freq_dist_pos.most_common(10))

    positive_tokens_for_model = get_tweets_for_model(positive_cleaned_tokens_list)
    negative_tokens_for_model = get_tweets_for_model(negative_cleaned_tokens_list)

    positive_dataset = [(tweet_dict, "Хорошая новость") for tweet_dict in positive_tokens_for_model]
    negative_dataset = [(tweet_dict, "Плохая новость") for tweet_dict in negative_tokens_for_model]

    dataset = positive_dataset + negative_dataset
    random.shuffle(dataset)

    train_data = dataset[:1]
    test_data = dataset[1:]

    classifier = NaiveBayesClassifier.train(train_data)

    #print("Accuracy is:", classify.accuracy(classifier, test_data))
    #print(classifier.show_most_informative_features(10))

    custom_tokens = remove_noise(word_tokenize(content), top_words)
    return classifier.classify(dict([token, True] for token in custom_tokens))

