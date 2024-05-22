import json
import zmq

try:
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.setsockopt(zmq.IMMEDIATE, True)  # make send() blocking by default (known issue)
    socket.connect("tcp://localhost:8989")

    keywords = ['apollo', 'moon']
    request = {
        'image_size': 'large',
        'keywords': keywords,
        'size': 10,
        'user_id': 1
    }
    print(f'Sending payload to NASA Image Search Microservice...')
    socket.send_string(json.dumps(request))
    response = socket.recv()
    response = json.loads(response)
    print(response)
finally:
    context.destroy()