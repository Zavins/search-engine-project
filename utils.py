import json
from os import walk, stat
import re
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from posting import Posting
import linecache

class FileHelper:
    @staticmethod
    def load_json(path):
        #Params: path of the website .json file
        #Reture: json data
        with open(path, mode="r") as f:
            data = json.load(f)
        return data
    
    @staticmethod
    def iterate_json_files(path):
        #Params: the path of the folder containing .json files
        #Return: doc_id, url, content, encoding
        for dirpath, dirnames, filenames in walk(path):
            for f in filenames:
                file_path = f"{dirpath}/{str(f).lower()}"
                if file_path.endswith((".json")):
                    data = FileHelper.load_json(file_path)
                    url: str = data["url"]
                    encoding: str = data["encoding"]
                    content: str = data["content"]
                    yield f, url, content, encoding

    @staticmethod
    def get_file_size(path):
        #Return: file size of file in path
        return stat(path).st_size/1024

    @staticmethod
    def save_json(path, content):
        #Params: path to write to, file content
        #Return: file size in kb
        with open(path, mode='w') as f:
            f.write(json.dumps(content, indent=4, default=lambda x: x.__dict__))
        return FileHelper.get_file_size(path)

    @staticmethod
    def get_obj_by_line_num(path, num):
        with open(path, mode='r') as f:
            data = linecache.getline(path, num)
        return eval(data)

class TokenHelper:
    @staticmethod
    def tokenize(text: str):
        porter = PorterStemmer()
        word = word_tokenize(text)
        temp = [i.lower() for i in word if i.isalnum() and re.match(r'^[a-zA-Z0-9]+$', i)]
        return [porter.stem(w) for w in temp]
