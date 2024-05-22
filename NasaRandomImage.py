import json
import zmq


def get_random_nasa_photos(keywords, image_size, number_requested, user_id=0):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.setsockopt(zmq.IMMEDIATE, True)  # make send() blocking by default (known issue)
    socket.connect("tcp://localhost:8989")

    request = {
        'image_size': image_size,
        'keywords': keywords,
        'number_requested': number_requested,
        'user_id': user_id
    }
    print(f'Sending payload to NASA Image Search Microservice...')
    socket.send_string(json.dumps(request))
    print(f'Waiting for response...')
    response = socket.recv()
    print(f'Images received from NASA Image Search Microservice')
    context.destroy()
    response = json.loads(response)

    return response['links']
