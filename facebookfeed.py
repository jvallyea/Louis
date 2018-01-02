import facebook
import urllib

token = 'EAACEdEose0cBADYoGkJwJZCZC5xSdUEabQ1wrLFjo6rpQ8AdY0zfaa9lXhw0KC2IsCx0vsQvqkKvWuWb927Wg6ZCVvTKiWtVDpYXz9OrpeMvt2ZCN7SWnCbE1TXwvltLDQNNMI5Nm6RZAjM19iZBPXnEp0azkA5ZBl5CTMGzZCDpqRxvHYdQupEE69mZCZCWgYUSc1KylikkZB3lwZDZD'

graph = facebook.GraphAPI(token)
profile = graph.get_object("me")

id_array = []
photos = graph.get_connections(id="me", connection_name="photos")
for item in photos['data']:
    id_array.append(item['id'])

#print id_array

for item in id_array:
    photo = (graph.get_object(str(item), fields="images"))
    photo_url = str(photo['images'][0]['source'])
    #print photo_url['images'][0]['source']

# photo1 = graph.get_object("1562105493870784", fields='images')
# print photo1

print photo_url

urllib.urlretrieve(photo_url, 'test.jpg')
