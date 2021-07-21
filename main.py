import requests
import os

url = 'https://api.vk.com/method/'
TOKEN = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
YATOKEN = 'AQAAAAArlzIkAADLW5pM2qBTp002qhWAmg8rGaU'


class VK:
    def __init__(self, token):
        self.params = {
            'owner_id': '552934290',
            'access_token': token,
            'v': '5.77',
            'album_id': 'profile',
            'extended': '1',
            'photo_sizes': '1'
        }
        self.photos = []

    def create_request(self, METHOD):
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


vk = VK(TOKEN)
data = vk.create_request('photos.get')
photos = vk.create_photo_info(data)
os.mkdir('photos')


photo_names = []

for photo in photos:
    data = requests.get(photo['url'])
    if photo['name'] in photo_names:
        name = str(photo['date'])
    else:
        name = str(photo['name'])
        photo_names.append(photo['name'])
    with open('photos/' + name + '.jpg', 'wb') as file:
        for chunk in data.iter_content():
            file.write(chunk)


class YaUploader:
    def __init__(self, token):
        self.token = token
        self.headers = {'Accept': 'application/json', "Authorization": self.token}

    def upload(self, file_path):
        params = {'path': file_path}
        response = requests.get('https://cloud-api.yandex.net/v1/disk/resources/upload', params=params,
                                headers=self.headers)
        put_url = response.json().get('href')
        files = {'file': open(file_path, 'rb')}
        response = requests.put(put_url, files=files, headers=headers)
        print(response)

    def create_ya_folder(self):
        params = {'path': 'photos'}
        response = requests.get('https://cloud-api.yandex.net/v1/disk/resources', params=params, headers=self.headers)
        print(response.json())


if __name__ == '__main__':
    pass
    # uploader = YaUploader(YATOKEN)
    # file_path = 'Ivan.txt'
    # uploader.upload(file_path)
    # uploader.create_ya_folder()
