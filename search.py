from math import log

from utils import FileHelper, TokenHelper
from posting import Posting
from datetime import datetime
from functools import lru_cache

url_dict = dict()
index_dict = dict()
file_cache = dict()
total = 0


@lru_cache(maxsize=256)
def get_all_postings(word):
    file, pos, length = index_dict.get(word, (None, None, None))
    if file and pos and length:
        if file_cache.get(file, None) == None:
            file_cache[file] = open(f"{file}.txt")
        return FileHelper.get_obj_by_position(file_cache[file], pos, length)
    return []


def intersect_doc_list(list1, list2):
    i = 0
    j = 0
    result = []
    global total
    while i < len(list1) and j < len(list2):
        if list1[i].doc_id == list2[j].doc_id:
            idf1 = log(total/len(list1))
            idf2 = log(total/len(list2))
            result.append(Posting(list1[i].doc_id, list1[i].tfs*idf1+list2[j].tfs*idf2))
            i += 1
            j += 1
        elif list1[i].doc_id < list2[j].doc_id:
            i += 1
        elif list1[i].doc_id > list2[j].doc_id:
            j += 1
    return result


def get_result(query):
    try:
        start = datetime.now()
        result = []
        tokens = TokenHelper.tokenize(query)
        for i, token in enumerate(tokens):
            if i == 0:
                result = get_all_postings(token)
            else:
                if len(result) == 0:
                    break
                result = intersect_doc_list(result, get_all_postings(token))
        urls = [url_dict[str(r.doc_id)] for r in sorted(result, key=lambda x: x.tfs, reverse=True)]
        time = str(datetime.now() - start)
        print("Time Used: ", time)
        return urls[:60], time
    except Exception as e:
        print(e)
        return (["Error occurred when querying the result"], 0)

def load():
    global url_dict, index_dict, total
    url_dict = FileHelper.load_json("doc_id.json")
    index_dict = FileHelper.load_json("index_table.json")
    total = len(url_dict.keys())

def unload():
    for v in file_cache.values():
        v.close()


def get_input():
    global file_cache
    while True:
        query = input("Enter query: ").lower()
        if query == "quit":
            break
        for r in get_result(query):
            print(r)
    unload()


if __name__ == '__main__':
    load()
    get_input()
