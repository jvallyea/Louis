import httplib, urllib, base64, json, requests

d = {}
d['a']  = [[1,0,0],[0,0,0]]
d['b'] = [[1,1,0],[0,0,0]]
d['c'] = [[1,0,0],[1,0,0]]
d['d'] = [[1,0,0],[1,1,0]]
d['e'] = [[1,0,0],[0,1,0]]
d['f'] = [[1,1,0],[1,0,0]]
d['g'] = [[1,1,0],[1,1,0]]
d['h'] = [[1,1,0],[0,1,0]]
d['i'] = [[0,1,0],[1,0,0]]
d['j'] = [[0,1,0],[1,1,0]]
d['k'] = [[1,0,1],[0,0,0]]
d['l'] = [[1,1,1],[0,0,0]]
d['m'] = [[1,0,1],[1,0,0]]
d['n'] = [[1,0,1],[1,1,0]]
d['o'] = [[1,0,1],[0,1,0]]
d['p'] = [[1,1,1],[1,0,0]]
d['q'] = [[1,1,1],[1,1,0]]
d['r'] = [[1,1,1],[0,1,0]]
d['s'] = [[0,1,1],[1,0,0]]
d['t'] = [[0,1,1],[1,1,0]]
d['u'] = [[1,0,1],[0,0,1]]
d['v'] = [[1,1,1],[0,0,1]]
d['w'] = [[0,1,0],[1,1,1]]
d['x'] = [[1,0,1],[1,0,1]]
d['y'] = [[1,0,1],[1,1,1]]
d['z'] = [[1,0,1],[0,1,1]]
d[' '] = [[0,0,0],[0,0,0]]

faces = {}
faces[1] = [0,0,0]
faces[2] = [1,0,0]
faces[3] = [0,1,0]
faces[4] = [0,0,1]
faces[5] = [1,1,0]
faces[6] = [1,0,1]
faces[7] = [0,1,1]
faces[8] = [1,1,1]

face_array = [1,2,3,4,5,6,7,8]

subscription_key = '72a7588f3eb84e9a88d922600c26cee4'
uri_base = 'westcentralus.api.cognitive.microsoft.com'

headers = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': subscription_key,
}

params = urllib.urlencode({
    'visualFeatures': 'Categories,Description,Color',
    'language': 'en',
})

try:
    body = open('STOP.jpg', 'rb').read()
    conn = httplib.HTTPSConnection(uri_base)
    conn.request("POST", "/vision/v1.0/analyze?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()
    parsed = json.loads(data)
    print ("Response:")
    print (json.dumps(parsed, sort_keys=True, indent=2))
    conn.close()
except Exception as e:
    print('Error: ')
    print(e)

text = 'a woman holding a baby'
text_array = []
positions = {}


for char in text:
    text_array.append(d[char])

print text_array
j = 0
for i in range(len(text_array)):
    if j > 26:
        break
    for item in face_array:
        if text_array[i][0] == faces[item]:
            j += 1
            print "face " + str(item)
            face_1 = item
    for item in face_array:
        if text_array[i][1] == faces[item]:
            j += 1
            print "face " + str(item)
            face_2 = item
    print "---"
    positions[i] = [face_1, face_2]

print positions

with open('positions.txt', 'w') as file:
    file.write(json.dumps(positions))

saved_positions = json.load(open("positions.txt"))

j = str(5)
for item in saved_positions:
    print saved_positions[item]
