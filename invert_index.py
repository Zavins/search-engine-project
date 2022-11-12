
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from simhash import Simhash, SimhashIndex
from collections import defaultdict
from utils import FileHelper, TokenHelper
from posting import Posting

simhash_index = SimhashIndex([], k=3)
inverted_index_dict = defaultdict(list)
doc_id_dict = defaultdict(str)
url_count = 0


def process_content(content):
    soup = BeautifulSoup(content, "html.parser")
    content = soup.get_text()
    tokens:list[str] = TokenHelper.tokenize(content)
    important_content = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'b', 'a'], text=True)
    #add weights for important contents.
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
    if len(tf_dict) == 0:
        return
    for key, val in tf_dict.items():
        inverted_index_dict[key].append(Posting(id, val))


def create_indexes(folder_path):
    global url_count
    f_iter = FileHelper.iterate_json_files(folder_path)
    for filename, url, content, encoding in f_iter:
        doc_id:str = filename.rstrip(".json")
        tokens = process_content(content)
        #if there is similar document exist
        hash = Simhash(value=tokens, f=64)
        if len(simhash_index.get_near_dups(hash)) < 1:
            print(url_count, url)
            simhash_index.add(doc_id, hash)
            tf_idf = cal_tf(tokens)

            url_count += 1
            doc_id_dict[url_count] = doc_id
            add_to_dict(tf_idf, url_count)


def generate_output(file_path):
    print("Token number:", len(inverted_index_dict.keys()))
    print(f"Total inverted url: {url_count}")
    print("the total size of index: ", FileHelper.save_json(file_path, inverted_index_dict))


if __name__ == '__main__':
    create_indexes("./developer/DEV")
    generate_output("./result.json")
    FileHelper.save_json("./doc_id.json", doc_id_dict)