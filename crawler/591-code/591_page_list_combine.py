
import json


with open('searched_json_url/taipeicity_house_url_list.json') as f:
    json_str_taipei_1 = f.read()

with open('searched_json_url/taipeicity_house_url_list_1.json') as f:
    json_str_taipei_2 = f.read()

with open('searched_json_url/newtaipeicity_house_url_list_1.json') as f:
    json_str_newtaipei_1 = f.read()

with open('searched_json_url/newtaipeicity_house_url_list.json') as f:
    json_str_newtaipei_2 = f.read()

with open('searched_json_url/newtaipeicity_restart_house_url_list_2.json') as f:
    json_str_newtaipei_3 = f.read()



taipei_list_1 = json.loads(json_str_taipei_1)
taipei_list_2 = json.loads(json_str_taipei_2)
newtaipei_list_1 = json.loads(json_str_newtaipei_1)
newtaipei_list_2 = json.loads(json_str_newtaipei_2)
newtaipei_list_3 = json.loads(json_str_newtaipei_3)

taipei_591_all_list = set(taipei_list_1 + taipei_list_2)
newtaipei_591_all_list = set(newtaipei_list_1 + newtaipei_list_2 + newtaipei_list_3)

with open('searched_json_url/taipei_591_all_list.json', 'w') as f:
    f.write(json.dumps(list(taipei_591_all_list)))

with open('searched_json_url/newtaipei_591_all_list.json', 'w') as f:
    f.write(json.dumps(list(newtaipei_591_all_list)))







