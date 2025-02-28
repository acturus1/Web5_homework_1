import requests
import sys
from PIL import Image
from io import BytesIO

def get_map_params(place):
    params = {'apikey':'8013b162-6b42-4997-9691-77b7074026e0', "geocode": place, "format": "json"}
    map_api = "http://geocode-maps.yandex.ru/1.x/"
    
    response = requests.get(map_api, params=params)
    return response

def get_map_placec(place, text):
    map_params = {
        "apikey": 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3',
        "text": text,
        "lang": "ru_RU",
        "ll": f'{place[0]},{place[1]}',
        "spn": '1,1',
        "type": "biz"
    }
    
    search_api_server = "https://search-maps.yandex.ru/v1/"
    
    response = requests.get(search_api_server, params=map_params)
    return response

def get_map_photo(place, points):
    map_params = {
        "ll": ','.join(place),
        "apikey": "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13",
        "pt": '~'.join([f'{point[0]},{point[1]},pm2rdm' for point in points])
    }
    
    map_api_server = "https://static-maps.yandex.ru/v1"
    
    response = requests.get(map_api_server, params=map_params)
    return response

def main():
    adress = " ".join(sys.argv[1:])
    
    response = get_map_params(adress)
    print(response.url)
    json_response = response.json()
    toponym_coodrinates = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
    toponym_coodrinates = toponym_coodrinates.split(' ')
    
    text = 'аптека'
    response2 = get_map_placec(toponym_coodrinates, text)
    json_response2 = response2.json()
    
    points = []
    for feature in json_response2["features"]:
        point = feature['geometry']['coordinates']
        points.append([point[0], point[1]])
    
    response3 = get_map_photo(toponym_coodrinates, points)
    
    im = BytesIO(response3.content)
    opened_image = Image.open(im)
    opened_image.show()


main()

# python 1zadanie.py Москва, ул. Ак. Королева, 12
