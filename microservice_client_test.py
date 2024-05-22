import json
import zmq

try:
    context = zmq.Context()
    sender = context.socket(zmq.REQ)
    sender.setsockopt(zmq.IMMEDIATE, True)  # make send() blocking by default (known issue)
    sender.connect("tcp://localhost:8993")

    keywords = ['challenger', 'explosion']
    request = {
        'image_size': 'large',
        'keywords': keywords,
        'size': 10,
        'user_id': 1
    }
    print(f'Sending payload to NASA Image Search Microservice...')
    sender.send_string(json.dumps(request))
    response = sender.recv()
    response = json.loads(response)
    print(response)
finally:
    context.destroy()