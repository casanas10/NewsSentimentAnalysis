import os
import glob
import re


def get_data(folder_path):
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


if __name__ == "__main__":
    folder_path = 'data/ReutersNews106521'
    dates, headlines, articles, urls = get_data(folder_path)
    print(dates[0])