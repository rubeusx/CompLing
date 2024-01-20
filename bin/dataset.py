import pandas as pd
import pickle

f2 = open('tweets.csv', 'r')

df = pd.read_csv(f2).drop(['id'], axis=1)
df.head(10)

positive_df = df[df.label == "positive"].drop('label', axis = 1)
with open('positive.json', 'w', encoding='utf-8') as file:
    positive_df.to_json(file, force_ascii=False)
    positive_df.shape

negative_df = df[df.label == "negative"].drop('label', axis = 1)
with open('negative.json', 'w', encoding='utf-8') as file:
    negative_df.to_json(file, force_ascii=False)
    negative_df.shape

positive_list = list(positive_df.text)
with open('positive_list.pkl', 'wb') as file:
    pickle.dump(positive_list,file)

negative_list = list(negative_df.text)
with open('negative_list.pkl', 'wb') as file:
    pickle.dump(negative_list,file)
