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
count = 0
path = []


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


# 储存到dict  {word:[Post(id,tf_s)]}
def save_data(tf_dict, id):
    if len(tf_dict) == 0:
        return
    global count
    count += 1
    for key, val in tf_dict.items():
        f_result[key].append(Post(id, val))


def simhash_result(path_list):
    i = 0
    num = 1
    for paths in path_list:
        print(f" {num} sim: {paths}")
        num += 1
        text = get_json_result(paths)
        sim_value = Simhash(text)
        if len((index.get_near_dups(sim_value))) < 1:
            index.add(str(i), sim_value)
            path.append(paths)


def binary_convert(m):
    return round(m / 1024, 2)


if __name__ == '__main__':
    dic = "DEV/flamingo_ics_uci_edu"
    files = get_path(dic)
    simhash_result(files)
    for id, web in enumerate(path):
        # print(f" {i} main: {web}")
        content = get_json_result(web)
        tokens = word_token(content)
        tf_idf = cal_tf(tokens)
        save_data(tf_idf, id)
    print("Token number:", len(f_result.keys()))
    print(f"Total inverted url: {count}")
    m = getsizeof(f_result)
    print("the total size of index: ", binary_convert(m))
    with open("test.json", mode='w') as f:
        f.write(json.dumps(f_result, indent=4))
