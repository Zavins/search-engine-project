import json
from os import walk, stat
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer

class FileHelper:
    @staticmethod
    def load_json(path):
        #Params: path of the website .json file
        #Reture: website url, website raw_content, website encoding
        with open(path, mode="r") as f:
            data = json.load(f)
            url:str = data["url"]
            encoding:str = data["encoding"]
            content:str = data["content"]
        return url, content, encoding
    
    @staticmethod
    def iterate_json_files(path):
        #Params: the path of the folder containing .json files
        #Return: doc_id, url, content, encoding
        for dirpath, dirnames, filenames in walk(path):
            for f in filenames:
                file_path = f"{dirpath}/{str(f).lower()}"
                if file_path.endswith((".json")):
                    yield (f, ) + FileHelper.load_json(file_path)

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

class TokenHelper:
    @staticmethod
    def tokenize(text: str):
        porter = PorterStemmer()
        word = word_tokenize(text)
        temp = [i.lower() for i in word if i.isalnum()]
        return [porter.stem(w) for w in temp]

    @staticmethod
    def computeWordFrequencies(tokens):
        token_freq = dict()
        #Convert list to dict.
        for token in tokens:
            token_freq[token] = token_freq[token] + 1 if token in token_freq else 1
        return token_freq

    @staticmethod
    def printFrequencies(frequencies) -> None:
        frequencies = dict(sorted(frequencies.items(), key=lambda item: -item[1]))
        for token, freq in frequencies.items():
            print(f"{token} - {freq}")