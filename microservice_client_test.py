import json
import zmq
from NasaRandomImage import get_random_nasa_photos

try:
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.setsockopt(zmq.IMMEDIATE, True)  # make send() blocking by default (known issue)
    socket.connect("tcp://localhost:8989")

    keywords = ['apollo', 'moon']
    request = {
        'image_size': 'large',
        'keywords': keywords,
        'number_requested': 10,
        'user_id': 1
    }
    socket.send_string(json.dumps(request))
    response = socket.recv()
    response = json.loads(response)
    print(response)
finally:
    context.destroy()

keywords = ['jupiter']
for image in get_random_nasa_photos(keywords, 'orig', 5):
    print(image)
