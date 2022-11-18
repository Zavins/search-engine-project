from utils import FileHelper, TokenHelper
from posting import Posting


url_dict = dict()
index_dict = dict()

def get_all_postings(word):
    line_num = index_dict.get(word, None)
    if line_num:
        return FileHelper.get_obj_by_line_num("result.txt", line_num)
    else:
        return []

def intersect_doc_list(list1, list2):
    i = 0
    j = 0
    result = []
    while i < len(list1) and j < len(list2):
        if list1[i].doc_id == list2[j].doc_id:
            result.append(Posting(list1[i].doc_id, list1[i].tfs *list2[j].tfs ))
            i += 1
            j += 1
        elif list1[i].doc_id < list2[j].doc_id:
            i += 1
        elif list1[i].doc_id > list2[j].doc_id:
            j += 1
    return result


def get_input():
    while True:
        query = input("Enter query: ").lower()
        if query == "quit":
            break
        result = []
        tokens = TokenHelper.tokenize(query)
        print(tokens)
        for i in range(len(tokens)):
            if i == 0:
                result = get_all_postings(tokens[i])
            else:
                result = intersect_doc_list(result, get_all_postings(tokens[i]))
        
        result.sort(key=lambda x: x.tfs, reverse=True)
        for r in result:
            print(url_dict[str(r.doc_id)])
            
            

if __name__ == '__main__':
    url_dict = FileHelper.load_json("doc_id.json")
    index_dict = FileHelper.load_json("indexes.json")
    get_input()
