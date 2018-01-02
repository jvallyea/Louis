import base64
import requests
import json
import os
import facebook
import urllib

token = 'EAACEdEose0cBAJZAog8QdugsN5yeUO4q1bOZBx4rCWheCZAgbzvJrZB1nFnkHJpSwSfKLNQEQQnJcq06ITRKP5SPvBBF1hWNi7JpCaD7Ee2OkSaSKqo9ZBoZBPgb4QsgGZAxqrVJoJ7OsH944BUpwkKtZCATH6qhQPqJ2wXBPiW2RnvVBEZCbDO7QUZB2rIHoBSEQeJYNIZB6yMZBgZDZD'

graph = facebook.GraphAPI(token)
profile = graph.get_object("me")

id_array = []
photos = graph.get_connections(id="me", connection_name="photos")
for item in photos['data']:
    id_array.append(item['id'])

#print id_array

for item in id_array:
    photo = (graph.get_object(str(item), fields="images, name_tags"))
    photo_url = str(photo['images'][0]['source'])
    #print photo_url['images'][0]['source']
    photo_id = photo['id']
    name = graph.get_object(id=photo_id, fields='name')

name = str(graph.get_object(str(item), fields='from')['from']['name'])
name = name.split(' ')[0]
# print photo_url


urllib.urlretrieve(photo_url, 'download.jpg')





with open("download.jpg", 'rb') as image_file:
    filename = str(base64.b64encode(image_file.read()).decode('UTF-8'))

with open("test.json", 'r') as f:
    data2 = json.load(f)
    #print filename
    data2['requests'][0]['image']['content'] = filename

os.remove('test.json')
with open('test.json', 'w') as f:
    json.dump(data2, f, indent=4)
#
data = open('test.json', 'rb').read()
response = requests.post(url='https://vision.googleapis.com/v1/images:annotate?key=AIzaSyAKePVj6YTI4eQlc-3So8ux_VomfYXjy3Y',data=data,headers={'Content-Type': 'application/json'})

print response.text

if 'joyLikelihood": "VERY_LIKELY' in response.text:
    emotion = 'joy'
elif 'sorrowLikelihood": "VERY_LIKELY' in response.text:
    emotion = 'sad'
elif 'angerLikelihood": "VERY_LIKELY' in response.text:
    emotion = 'anger'
elif 'surpriseLikelihood": "VERY_LIKELY' in response.text:
    emotion = 'surprise'
else:
    emotion = 'none'

print name + ' ' + emotion
