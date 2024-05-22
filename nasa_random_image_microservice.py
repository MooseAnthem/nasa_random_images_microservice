import json
import zmq
import requests
import re

ENDPOINT = 'https://images-api.nasa.gov/search'
unique_session = {}
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://localhost:8993")


def convert_nasa_href(link):
    # remove the collections suffix:
    link = str.replace(link, '/collection.json', '')
    photo_number = re.search(r'[^/]*$', link).group(0)
    return '/'.join([link, photo_number])


while True:
    #  Wait for next request from client
    request = socket.recv()
    try:
        req = json.loads(request)
        keywords = ','.join(req['keywords'])
        images_requested = req['size']
        image_size = req['image_size']
        payload = {'links': []}

        r = requests.get(ENDPOINT, {'keywords': keywords, 'media_type': 'image'})
        nasa_images = json.loads(r.content)
        # create a dictionary to track what images have been sent back:
        if req['user_id'] not in unique_session:
            unique_session[req['user_id']] = []
        previous_images = unique_session[req['user_id']]
        images_added = 0
        for image in nasa_images['collection']['items']:
            if images_added == images_requested:
                break
            if image['data'][0]['nasa_id'] not in previous_images:
                previous_images.append(image['data'][0]['nasa_id'])
                # add to payload
                href = convert_nasa_href(image['href'])
                href = f'{href}~{image_size}.jpg'
                r = requests.get(href)
                if r.status_code == 200:
                    payload['links'].append(href)
                    images_added += 1

        socket.send_string(json.dumps(payload))

    except json.JSONDecodeError as e:
        response = {
            'error': "request JSON formatted incorrectly"
        }
        socket.send_string(json.dumps(response))
    finally:
        pass
