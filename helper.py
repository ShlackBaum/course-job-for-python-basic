import time
import requests
import json
from pprint import pprint

def splitter_of_strings (string):
    string = string.split(" ")
    string = "-".join(string)
    string = string.split(":")
    string = "-".join(string)
    string = string.split(".")
    string = "-".join(string)
    return string

def json_report(folder_name, yd):
    print(f"Этап 5 из 5: Создаем JSON-отчёт")
    time.sleep(1)
    value_for_OAuth = 'OAuth ' + yd.token
    h = {'Authorization': value_for_OAuth}
    p = {'path': folder_name}
    response = requests.get(yd.create_folder_or_upload_url, params=p, headers=h)
    file_list=response.json()['_embedded']['items']
    list_of_dicts_for_json = []
    dict_for_json = {}
    for file in file_list:
        for key, value in file.items():
            if key == 'size':
                dict_for_json[key]=value
            if key == 'name':
                dict_for_json[key]=value
                dict_for_json_copied=dict_for_json.copy()
                list_of_dicts_for_json.append(dict_for_json_copied)
                dict_for_json.clear
    json_dict_bl = json.dumps(list_of_dicts_for_json)
    json_dict = json.loads(json_dict_bl)
    pprint(f""" Итоговый JSON-файл:
    {json_dict}""")
    with open('course_json.json', 'w') as outfile:
        json.dump(json_dict, outfile)
    return (json_dict)