import requests
import os

url = 'https://api.vk.com/method/'
TOKEN = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'


class VK:
    def __init__(self, token, id):
        self.params = {
            'owner_id': id,
            'access_token': token,
            'v': '5.77',
            'album_id': 'profile',
            'extended': '1',
            'photo_sizes': '1'
        }
        self.photos = []

    def create_request(self, METHOD):
        print('Получаем файлы из VK...')
        result = requests.get(url + METHOD, params=self.params)
        return result.json()

    def create_photo_info(self, data):
        for items in data['response']['items']:
            for index, item in enumerate(items['sizes']):
                if index == len(items['sizes']) - 1:
                    self.photos.append(
                        {'url': item['url'], 'name': items['likes']['count'], 'size': item['type'],
                         'date': items['date']})
        return self.photos


input_id = input('Введите id пользователя: ')
input_yatoken = input('Введите яндекс токен: ')
vk = VK(TOKEN, input_id)
data = vk.create_request('photos.get')
photos = vk.create_photo_info(data)

photo_names = []

for photo in photos:
    print(f'Создаем файл... {str(photo["name"]) + ".jpg"}')
    data = requests.get(photo['url'])
    if str(photo['name']) + '.jpg' in photo_names:
        name = str(photo['date']) + '.jpg'
        photo_names.append(str(photo['date']) + '.jpg')
    else:
        name = str(photo['name']) + '.jpg'
        photo_names.append(str(photo['name']) + '.jpg')
    with open(name, 'wb') as file:
        for chunk in data.iter_content():
            file.write(chunk)


class YaUploader:
    def __init__(self, token):
        self.token = token
        self.headers = {'Accept': 'application/json', "Authorization": self.token}
        self.folder = ''

    def upload(self, names):
        for name in names:
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


if __name__ == '__main__':
    uploader = YaUploader(input_yatoken)
    uploader.create_ya_folder()
    uploader.upload(photo_names)
