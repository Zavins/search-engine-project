from invert_index import process_content,cal_tf,add_to_dict,save_indexes
import json


#D:\Desktop\fall_2022\compsci121\Compsci-121-A3-Search-Engine-Group-3\analyst\www_informatics_uci_edu\1f35e2fbae793436bef9256c0104de291a0bd5751440a59a2c4958b093240f62.json
with open("./analyst/www_informatics_uci_edu/1f35e2fbae793436bef9256c0104de291a0bd5751440a59a2c4958b093240f62.json", "r") as f:
    a = json.load(f)

    b = process_content(a["content"])
    c = cal_tf(b)
    add_to_dict(c, 1)
    save_indexes("test.txt")
