import sys
import RPi.GPIO as gpio
import time
import httplib, urllib, base64, json, requests
# import picamera

global gpio

def stepper1(direction, steps):
    try:
        steps = int(float(steps))
    except:
        steps = 0

    gpio.setmode(gpio.BCM)
    gpio.setup(23, gpio.OUT) #Direction
    gpio.setup(24, gpio.OUT) #Step
    print("You told me to turn %s %s steps") % (direction, steps)

    if direction == 'left':
        gpio.output(23, True)
    elif direction == 'right':
        gpio.output(23, False)

    StepCounter = 0
    WaitTime = 0.002

    while StepCounter < steps:
        gpio.output(24, True)
        gpio.output(24, False)
        StepCounter += 1
        time.sleep(WaitTime)

    time.sleep(1)

    gpio.cleanup()

def stepper2(direction, steps):
    try:
        steps = int(float(steps))
    except:
        steps = 0

    print ("You told me to turn %s %s steps") % (direction, steps)

    gpio.setmode(gpio.BCM)
    gpio.setup(20, gpio.OUT) #Direction
    gpio.setup(21, gpio.OUT) #Step

    if direction == 'backward':
        gpio.output(20, True)
    elif direcetion == "forward":
        gpio.output(20, False)

    StepCounter = 0
    WaitTime = 0.002

    while StepCounter < steps:
        gpio.output(21, True)
        gpio.output(21, False)
        StepCounter += 1
        time.sleep(WaitTime)

    time.sleep(1)

    gpio.cleanup()






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

# camera = picamera.PiCamera()
# camera.capture('image.jpg')

subscription_key = '11df03355d354a4290e13ef06312983b'
uri_base = 'westcentralus.api.cognitive.microsoft.com'
#
headers = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': subscription_key,
}
#
params = urllib.urlencode({
    'visualFeatures': 'Categories,Description,Color',
    'language': 'en',
})
#
try:
    body = open('Stop.JPG', 'rb').read()
    conn = httplib.HTTPSConnection(uri_base)
    conn.request("POST", "/vision/v1.0/analyze?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()
    parsed = json.loads(data)
    print ("Response:")
    result = (json.dumps(parsed, sort_keys=True, indent=2))
    print parsed
    caption = parsed["description"]["captions"][0]["text"]
    print caption
    print caption
    conn.close()
except Exception as e:
    print('Error: ')
    print(e)

##caption = "alex zhuk"
text_array = []

saved_positions = json.load(open("positions.txt"))
positions = {}

for char in caption:
    text_array.append(d[char])

print text_array

if len(text_array) < 13:
    diff = 13 - len(text_array)
    k = 0
    while k < diff:
        text_array.append([[0,0,0],[0,0,0]])
        k += 1
print text_array

j = 0
for i in range(len(text_array)):
    if j >= 13:
        break
    for item in face_array:
        if text_array[i][0] == faces[item]:
            current_pos = saved_positions[str(j)][0]
            desired_pos = item
            difference = desired_pos - current_pos
            if difference >= 0:
                steps = 25 * difference
                stepper1("left", steps)
                face_1 = item
                print "Moved to position %s from position %s" % (desired_pos, current_pos)
                stepper2("forward", 125)
            elif difference < 0:
                difference = abs(difference)
                steps = 25 * difference
                stepper1("right", steps)
                face_1 = item
                print "Moved to position %s from position %s" % (desired_pos, current_pos)
                stepper2("forward", 125)

    for item in face_array:
        if text_array[i][1] == faces[item]:
            current_pos = saved_positions[str(j)][1]
            desired_pos = item
            difference = desired_pos - current_pos
            if difference >= 0:
                steps = 25 * difference
                stepper1("left", steps)
                face_2 = item
                print "Moved to position %s from position %s" % (desired_pos, current_pos)
                j += 1
                if j >=13:
                    stepper2("backward", 3250)
                elif j < 13:
                    stepper2("forward", 125)
            elif difference < 0:
                difference = abs(difference)
                steps = 25 * difference
                stepper1("right", steps)
                face_2 = item
                print "Moved to position %s from position %s" % (desired_pos, current_pos)
                j += 1
                if j >= 13:
                    stepper2("backward", 3250)
                elif j < 13:
                    stepper2("forward", 125)

    positions[i] = [face_1, face_2]

with open('positions.txt', 'w') as file:
    file.write(json.dumps(positions))
