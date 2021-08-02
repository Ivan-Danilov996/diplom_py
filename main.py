import requests
from datetime import datetime
import json

id = '552934290'
token = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'


def get_date(date):
    ts = int(date)
    return datetime.utcfromtimestamp(ts).strftime('%d-%m-%Y %H-%M-%S')


class VK:
    def __init__(self):
        self.params = {
            'owner_id': input('Введите id пользователя: '),
            'access_token': input('Введите токен вк: '),
            'v': '5.77',
            'album_id': 'profile',
            'extended': '1',
            'photo_sizes': '1',
            'count': input('Введите количество фотографий: ')
        }
        self.url = 'https://api.vk.com/method/'
        self.photos = []
        self.photo_names = []
        self.info_files = []
        self.create_request('photos.get')

    def create_request(self, METHOD):
        print('Получаем файлы из VK...')
        result = requests.get(self.url + METHOD, params=self.params)
        self.create_photo_info(result.json())

    def create_photo_info(self, data):
        for items in data['response']['items']:
            for index, item in enumerate(items['sizes']):
                if index == len(items['sizes']) - 1:
                    self.photos.append(
                        {'url': item['url'], 'name': items['likes']['count'], 'size': item['type'],
                         'date': items['date']})
        self.create_files(self.photos)

    def create_files(self, photos):
        for photo in photos:
            print(f'Создаем файл... {str(photo["name"]) + ".jpg"}')
            data = requests.get(photo['url'])
            if str(photo['name']) + '.jpg' in self.photo_names:
                name = str(get_date(photo['date'])) + '.jpg'
                self.photo_names.append(str(get_date(photo['date'])) + '.jpg')
                self.info_files.append({'name': str(get_date(photo['date'])), 'size': photo['size']})
            else:
                name = str(photo['name']) + '.jpg'
                self.photo_names.append(str(photo['name']) + '.jpg')
                self.info_files.append({'name': str(photo['name']), 'size': photo['size']})
            with open(name, 'wb') as file:
                for chunk in data.iter_content():
                    file.write(chunk)
        self.create_data_file(self.info_files)

    def create_data_file(self, items):
        with open('data.json', "w") as write_file:
            json.dump(items, write_file)

    def get_photo_names(self):
        return self.photo_names


class YaUploader:
    def __init__(self, names):
        self.token = input('Введите яндекс токен: ')
        self.headers = {'Accept': 'application/json', "Authorization": self.token}
        self.folder = ''
        self.names = names
        self.create_ya_folder()

    def upload(self):
        for name in self.names:
            print(f'Загрузка {name} на сервер')
            params = {'path': 'photos/' + name}
            response = requests.get('https://cloud-api.yandex.net/v1/disk/resources/upload', params=params,
                                    headers=self.headers)
            put_url = response.json().get('href')
            files = {'file': open(name, 'rb')}
            response = requests.put(put_url, files=files, headers=self.headers)
            if response.status_code == 201:
                print('Загрузка файла завершена')
        print('Готово')

    def create_ya_folder(self):
        print('Создаем папку на Яндекс диске')
        params = {'path': 'photos'}
        response = requests.put('https://cloud-api.yandex.net/v1/disk/resources', params=params, headers=self.headers)
        self.folder = response.json().get('href')
        self.upload()


if __name__ == '__main__':
    vk = VK()
    disc = YaUploader(vk.get_photo_names())
