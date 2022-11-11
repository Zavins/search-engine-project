import json
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize, WordPunctTokenizer
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
import os
from simhash import Simhash, SimhashIndex
from collections import defaultdict
from sys import getsizeof
from Post import Post


index = SimhashIndex([], k=3)
f_result = defaultdict(list)
id_result = {}
count=0
path=[]


def get_json_result(path):
    with open(path, mode="r") as f:
        data = json.load(f)
        soup = BeautifulSoup(data["content"], "html.parser")
        file_content = soup.get_text()

        result = " ".join(file_content.split())
        important_content = soup.find_all(['h1', 'h2', 'h3', 'b', 'a'], text=True)
        important_content = ' '.join([e.string for e in important_content])
        # print("This is the result",result)
        return result + " " + important_content


def word_token(text):
    porter = PorterStemmer()
    word = word_tokenize(text)
    temp = [i.lower() for i in word if i.isalnum()]
    return [porter.stem(w) for w in temp]


# 计算td-idf
def cal_tf(result):
    try:
        tfidf_vec = TfidfVectorizer()
        tfidf_vec.fit_transform(result)
        return tfidf_vec.vocabulary_
    except Exception as e:
        return dict()



# 得到所有path
def get_path(domain):
    path_result = []
    for root, dirs, files in os.walk(domain):
        for file in files:
            if os.path.splitext(file)[1] == '.json':
                path_result.append(os.path.join(root, file))
    return path_result
