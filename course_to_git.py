import requests
from pprint import pprint
import datetime
import time
from tqdm import tqdm
import json

#Вставьте имя папки на создание для Яндекс.Диска
folder_name = ''

#Вставьте ID профиля с ВК для резервирования его фотографий
vk_id = ''

#Вставьте токен ВК
vk_token = ''

#Вставьте токен Яндекс.Диска
yd_token = ''

vk_api_v= '5.131'
vk_url_auth ='?v=' + vk_api_v + '&access_token=' + vk_token
base_vk_url='https://api.vk.com/method/'
base_yd_url='https://cloud-api.yandex.net/'

def get_photos(user_id):
    url_salt='photos.get'
    url=base_vk_url+url_salt+vk_url_auth
    owner_id = user_id
    print(f"Этап 1 из 5: Запрашиваем фотографии из профиля в ВК")
    p = {'owner_id': owner_id, 'album_id': 'profile', 'extended': '1', 'photo_sizes': '0'}
    response = requests.get(url, params=p)
    list_of_dictphotos= response.json()['response']['items']
    dict_id_object = {}
    dict_url_likes = {}
    print(f"Этап 2 из 5: Собираем фото из профиля в словарь")
    for photo_dict in tqdm(list_of_dictphotos):
        time.sleep(0.3)
        for key, value in photo_dict.items():
            if key == 'id':
                photo_id = value
                dict_id_object[photo_id] = ''
            if key == 'sizes':
                list_of_resolutions = photo_dict['sizes']
                dict_with_maximum_resolution = list_of_resolutions[-1]
                url_of_maximum_resolution_photo = dict_with_maximum_resolution['url']
            if key == 'likes':
                likes_amount = value['count']
                dict_url_likes[url_of_maximum_resolution_photo] = likes_amount
                dict_url_likes_copied = {}
                dict_url_likes_copied = dict_url_likes.copy()
                dict_id_object[photo_id] = dict_url_likes_copied
                dict_url_likes.clear()
    return dict_id_object

def create_folder(folder_name, yd_token):
    print(f"Этап 3 из 5: Создаем папку на диске")
    time.sleep(1)
    url_salt="v1/disk/resources"
    url = base_yd_url+url_salt
    value_for_OAuth = 'OAuth ' + yd_token
    h = {'Authorization': value_for_OAuth}
    p = {'path': folder_name}
    response=requests.put(url, params=p, headers=h)
    if response.status_code == 201:
        print(f"Папка {folder_name} успешно создана")
        return folder_name
    elif response.status_code == 409:
        print(f"Папка {folder_name} уже есть. В создании не нуждается")
        return folder_name
    else:
        print(f"Что-то пошло не так. Отклик - {response.status_code}")
        return

def reserve_photos(dict_with_photos, folder_name):
    url=base_yd_url+'v1/disk/resources/upload'
    likes_list = []
    print(f"Этап 4 из 5: загружаем фотографии на диск")
    for photo_id, dicts_with_url_and_values in tqdm(dict_with_photos.items()):
        time.sleep(0.3)

        for dict_url, dict_likes in dicts_with_url_and_values.items():
            value_for_OAuth = 'OAuth ' + yd_token
            dtt = datetime.datetime.now()
            date_time_str = str(dtt)
            path=folder_name+'/'+ str(dict_likes) +'.jpg'
            if dict_likes in likes_list:
                date_time_str = date_time_str.split(" ")
                date_time_str = "-".join(date_time_str)
                date_time_str = date_time_str.split(":")
                date_time_str = "-".join(date_time_str)
                date_time_str = date_time_str.split(".")
                date_time_str = "-".join(date_time_str)
                path=folder_name+'/'+ str(dict_likes) + '-' + date_time_str + '.jpg'
            likes_list.append(dict_likes)
            h = {'Authorization': value_for_OAuth}
            p = {'path': path, 'url': dict_url}
            requests.post(url, headers=h, params=p)

def json_report(folder, token):
    print(f"Этап 5 из 5: Создаем отчет как JSON")
    time.sleep(1)
    url_salt = "v1/disk/resources"
    url = base_yd_url + url_salt
    value_for_OAuth = 'OAuth ' + yd_token
    h = {'Authorization': value_for_OAuth}
    p = {'path': folder}
    response = requests.get(url, params=p, headers=h)
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
    json_dict = json.dumps(list_of_dicts_for_json)
    pprint(f""" Итоговый JSON-файл: 
{json_dict}""")
    return (json_dict)

dict_id_object=get_photos(vk_id)
create_folder(folder_name, yd_token)
reserve_photos(dict_id_object, folder_name)
json_report(folder_name, yd_token)
