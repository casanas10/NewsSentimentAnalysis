import os
import glob
import re
import numpy as np
import pandas as pd

import spacy
nlp = spacy.load('en_core_web_sm')

def get_news_data(folder_path):
    # Load the dataset
    dates = []
    headlines = []
    articles = []

    urls = []

    for folder_name in glob.glob(os.path.join(folder_path, '*')):
        for filename in glob.glob(os.path.join(folder_name, '*')):

            try:
                with open(filename, 'r') as f:

                    text = f.read()
                    lines = re.split(r'[\n\r]+', text)
                    article = ''
                    for i in range(4,len(lines)):
                        article += lines[i].rstrip()

                    dates.append(re.sub("-- ", "", lines[2]))
                    headlines.append(re.sub("-- ", "", lines[0]))
                    urls.append(re.sub("-- ", "", lines[3]))
                    articles.append(article)
            except:
                pass

    return dates, headlines, articles, urls

def get_apple_news_data(data_df):

    if not os.path.exists('data/apple_news.pkl'):
        apple_news_df = pd.DataFrame(columns=['date', 'headline', 'text', 'url'])

        for i, row in enumerate(data_df.values):
            doc = nlp(row[2])
            # set_of_orgs = set()
            for X in doc.ents:
                if X.label_ == 'ORG':
                    if X.text == 'Apple' or X.text == "APPL":
                        # set_of_orgs.add(X.text)
                        print(X.text, X.label_)
                        print(row[0])
                        apple_news_df.loc[i] = row
                        break

        return apple_news_df

def cleanup_date_format(x):
    print(x)


if __name__ == "__main__":

    if not os.path.exists('data/newspickle.pkl'):
        folder_path = 'data/ReutersNews106521'
        dates, headlines, articles, urls = get_news_data(folder_path)

        date_array = np.array(dates)
        headline_array = np.array(headlines)
        text_array = np.array(articles)
        urls_array = np.array(urls)

        print(date_array.shape)
        print(headline_array.shape)
        print(text_array.shape)
        print(urls_array.shape)

        all_data_df = pd.DataFrame({
            'date': date_array,
            'headline': headline_array,
            'text': text_array,
            'url': urls_array
        })

        all_data_df.to_pickle("./data/newspickle.pkl")


    all_data_df = pd.read_pickle("./data/newspickle.pkl")

    apple_news_df = pd.read_pickle("./data/apple_news.pkl")

    apple_news = apple_news_df['Date'].apply(lambda x: cleanup_date_format(x))
            # for line in headlines[0:5]:
    #     print(line)
        # doc = nlp('European authorities fined Google a record $5.1 billion on Wednesday for abusing its power in the mobile phone market and ordered the company to alter its practices')
        # print([(X.text, X.label_) for X in doc.ents])

