import requests
import json
from pprint import pprint

key = 'AIzaSyCKN-gIIELoSc3b98yoiG2UjiHGSiCX32I'
channelId = 'UCMCgOm8GZkHp8zJ6l7_hIuA'
main_link = 'https://www.googleapis.com/youtube/v3/search?&maxResults=1&part=snippet,id&order=date&maxResults=1'

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

params = {'key': key,
          'channelId': channelId}

response = requests.get(main_link, headers=headers,params=params)
data = json.loads(response.text)
add_data = data["items"][0]["snippet"]["publishedAt"]

print(f'Последнее видео на канале "{data["items"][0]["snippet"]["channelTitle"]}" - "{data["items"][0]["snippet"]["title"]}", добавлено {add_data[0:10]}')

#pprint(data)
#print(type(data["items"]))