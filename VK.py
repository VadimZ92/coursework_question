import copy
import os
import requests
import time
import json
from pprint import pprint
from tqdm import tqdm
import time
from tqdm import tqdm

# access_token = 'vk1.a.xz2om2riQKMC5a3MgPz792dnFjJkNcVdqhtNBBxDnovy' \
#                '4Sa7blXMmlrFXvIZaDeOLBD_4qMTRn_9PKFkHX3-cQzVCXAlA6' \
#                'mm355Qj7_FhecBAHt3bRDmzsJAaA5He9mkMa0ADZHyERnWIvg6' \
#                '-ZrU1fW2_bkYJnZ6PRAQReTmQrE6JU4ygpVsbC7e4adpfnCT'

# user_id = input('Введите ID пользователя ВК: \n')
# TokenYandexPoligon = input('Введите токен полигона ЯндексДиска: \n')

class VK:
    # user_id = input('Введите ID пользователя ВК: \n')
    # TokenYandexPoligon = input('Введите токен полигона ЯндексДиска: \n')
    print("Начало работы программы по выгрузке фотографий из "
          "профиля пользователя ВК и загрузке на Яндекс диск")
    time.sleep(3)

    def __init__(self, access_token, user_id, version='5.131'):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}
        # self.Token = TokenYandexPoligon

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

