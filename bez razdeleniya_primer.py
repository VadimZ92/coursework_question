import copy
import os
import requests
import time
import json
from pprint import pprint
from tqdm import tqdm
import time
from tqdm import tqdm

access_token = 'vk1.a.xz2om2riQKMC5a3MgPz792dnFjJkNcVdqhtNBBxDnovy' \
               '4Sa7blXMmlrFXvIZaDeOLBD_4qMTRn_9PKFkHX3-cQzVCXAlA6' \
               'mm355Qj7_FhecBAHt3bRDmzsJAaA5He9mkMa0ADZHyERnWIvg6' \
               '-ZrU1fW2_bkYJnZ6PRAQReTmQrE6JU4ygpVsbC7e4adpfnCT'

user_id = input('Введите ID пользователя ВК: \n')
TokenYandexPoligon = input('Введите токен полигона ЯндексДиска: \n')

class VK:
    print("Начало работы программы по выгрузке фотографий из "
          "профиля пользователя ВК и загрузке на Яндекс диск")
    time.sleep(3)

    def __init__(self, access_token, user_id, version='5.131', ):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}
        self.Token = TokenYandexPoligon

    def creation_json_photoList(self):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.id,
                  'album_id': 'profile',
                  'extended': 1,
                  'photo_sizes': 1,
                  'count': 5
                  }
        response = requests.get(url, params={**self.params, **params}).json()
        if list(response)[0] != 'response':
            print("Введен не верный ID. Программа завершена")
            os._exit(1)
        response_status = \
            requests.get(url, params={**self.params, **params}).status_code
        if response_status == 200:
            print("Успешная выгрузка фотографий из профиля ВК")
            time.sleep(2)
        elif response_status >= 400:
            print(f'Ошибка{response_status}')
        response = response['response']['items']
        # Список для создания файла json
        json_list = []
        # Список имен фото, нужен для проверки повтора имени фото
        Name_list = []
        # Результирующий список со ссылками на фото
        self.list_photo = []
        json_dict = {}  # Словарь для создания файла json
        # копия словаря (другой объект) для записи в список
        copy_json_dict = {}
        for dict_response in response:
            name = dict_response['likes']['count']
            photo = dict_response['sizes'][-1]['url']
            if name not in Name_list:
                json_dict["file_name"] = f"{name}.jpg"
                json_dict['size'] = dict_response['sizes'][-1]['type']
            else:
                json_dict["file_name"] = \
                    f"{name}.jpg, 'date':{dict_response['date']}"
                json_dict['size'] = dict_response['sizes'][-1]['type']
            Name_list.append(name)
            copy_json_dict = copy.deepcopy(json_dict)
            json_list.append(copy_json_dict)
            with open('data.json', 'w') as write_file:
                json.dump(json_list, write_file)
            self.list_photo.append(photo)
        print("Создан json - файл")
        time.sleep(2)
        return json_list

    with open('data.json', 'rb') as file:
        json_file = file.read()

    # ЗАПИСЬ НА ЯНДЕКС ДИСК

class YD:


    def __init__(self, Token):
        self.Token = TokenYandexPoligon

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'OAuth {}'.format(self.Token)
        }

    def disk_file_path(self, path):  # Создаем папку на яндекс диске
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        headers = self.get_headers()
        requests.put(f"{url}?path={path}", headers=headers)
        print("Создана папка 'Photo_VK' на Яндекс диске")
        time.sleep(2)
        return f"{url}?path={path}"

    def upload_to_yandexDisk(self, disk_file_path):
        print('Загрузка Фотографий на Яндекс Диск ')
        time.sleep(0.5)
        upload_url = \
            "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        with open('data.json') as file_object:
            # Список имен фотографий для записи на яндекс диск
            list_name_photo = json.load(file_object)
        for dikt_name_photo, url_photo in\
                tqdm(zip(list_name_photo, vk.list_photo)):
            time.sleep(0.5)
            name = dikt_name_photo['file_name']
            # проверка на максимально возможное ограничение
            # по длине названия файла в Яндекс диске
            if len(name) > 12:
                name = name[:14]
            params = {"path": f'Photo_VK/{name}',
                      'url': url_photo}
            response = \
                requests.post(upload_url, headers=headers, params=params)
            time.sleep(1)  # время, чтобы успевал отработать алгоритм
        if 200 <= response.status_code < 400:
            print('Успешная загрузка Фотографий на Яндекс Диск ')
        elif response.status_code >= 400:
            print(f'Ошибка{response.status_code}')


if __name__ == '__main__':
    vk = VK(access_token, user_id)
    ya = YD(TokenYandexPoligon)
    vk.creation_json_photoList()
    ya.disk_file_path('Photo_VK')
    ya.upload_to_yandexDisk(disk_file_path='Photo_VK')
