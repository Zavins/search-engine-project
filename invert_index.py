from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from simhash import Simhash, SimhashIndex
from collections import defaultdict
from utils import FileHelper, TokenHelper
from posting import Posting
import os

simhash_index = SimhashIndex([], k=3)
inverted_index_dict = defaultdict(list)
index_table = defaultdict(list) #token: [("filename", lineNumber), ("filename", lineNumber)]
doc_id_dict = defaultdict(str)
url_count = 0
THREADSHOLD = 100000
PARTIAL_DIR = "./partial/"
PARTIAL_INDEX_NAME = "partial"
MERGED_INDEX_NAME="merged"
file_count = 1


def process_content(content):
    soup = BeautifulSoup(content, "html.parser")
    content = soup.get_text()
    tokens: list[str] = TokenHelper.tokenize(content)
    important_content = soup.find_all(['h1', 'h2', 'h3', 'b', 'a', 'title'], text=True)
    # add weights for important contents.
    for c in important_content:
        tokens.extend(TokenHelper.tokenize(c.string))
    return tokens


def cal_tf(result):
    try:
        tfidf_vec = TfidfVectorizer()
        tfidf_vec.fit_transform(result)
        return tfidf_vec.vocabulary_
    except Exception as e:
        return dict()


def add_to_dict(tf_dict, id):
    global file_count
    if len(tf_dict) == 0:
        return
    for key, val in tf_dict.items():
        inverted_index_dict[key].append(Posting(id, val))
    if len(inverted_index_dict.keys()) >= THREADSHOLD:
        write_indexes(f'{PARTIAL_DIR}{PARTIAL_INDEX_NAME}{file_count}.txt')
        file_count += 1
    

def create_indexes(folder_path):
    global url_count
    f_iter = FileHelper.iterate_json_files(folder_path)
    for filename, url, content, encoding in f_iter:
        doc_id: str = filename.rstrip(".json")
        tokens = process_content(content)
        # if there is similar document exist
        hash = Simhash(value=tokens, f=64)
        if len(simhash_index.get_near_dups(hash)) < 1:
            print(url_count, url)
            simhash_index.add(doc_id, hash)
            tf_idf = cal_tf(tokens)
            url_count += 1
            doc_id_dict[url_count] = url
            add_to_dict(tf_idf, url_count)


def write_indexes(file_path):
    i = 0
    for k, v in inverted_index_dict.items():
        with open(file_path, "a") as f:
            length = FileHelper.write_obj(f, v)
        index_table[k].append([file_path, i, length])
        i += length
    inverted_index_dict.clear()


def merge_partial_indexes():
    i = 0
    with open(f"./{MERGED_INDEX_NAME}.txt", "a") as mf:
        for token, location in index_table.items():
            posts = []
            for filename, position, length in location:
                with open(f"{filename}") as f:
                    posts.extend(FileHelper.get_obj_by_position(f, position, length))
            posts.sort(key=lambda x: x.doc_id)
            length = FileHelper.write_obj(mf, posts)
            index_table[token] = [MERGED_INDEX_NAME, i, length]
            i += length

def generate_output():
    print("Token number:", len(index_table.keys()))
    print(f"Total inverted url: {url_count}")


def initialize():
    if os.path.exists(PARTIAL_DIR):
        for file in os.scandir(PARTIAL_DIR):
            os.remove(file)
    else:
        os.mkdir("./partial/")

    if os.path.exists(f"./{MERGED_INDEX_NAME}.txt"):
        os.remove(f"./{MERGED_INDEX_NAME}.txt")

if __name__ == '__main__':
    initialize()
    create_indexes("./developer/DEV")
    write_indexes(f'{PARTIAL_DIR}{PARTIAL_INDEX_NAME}{file_count}.txt')
    merge_partial_indexes()
    FileHelper.save_json("./index_table.json", index_table)
    FileHelper.save_json("./doc_id.json", doc_id_dict)
    generate_output()
