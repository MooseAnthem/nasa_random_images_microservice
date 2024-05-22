# A. How to REQUEST data from the NASA Random Image Microservice

1. ZeroMQ is a required library. Ensure that it's installed in your virtual environment, using pip:

`pip install zmq`

2. Run an instance of the microservice on `localhost`. The NASA Random Image Microservice (NRIM) binds to `localhost:8989`.
```python
> python3 nasa_random_images_microservice.py
```


3. NRIM expects to receive a JSON string containing 4 fields:
   1. `keywords:` - an array of string keywords that will be used to retrieve related random photos.
   2. `image_size` - the size of the images sent back. Valid sizes are `orig`, `large`, `medium`, `small`, and `thumb`.
   3. `number_requested` - how many image hyperlinks the microservice should return.
   4. `user_id` - a unique user ID. This ensures that over multiple microservice calls, an ID will never receive the same hyperlink more than once.

For convenience, the wrapper function `get_random_nasa_photos(keywords, image_size, number_requested, user_id=0)` is provided to network connections to the microservice and JSON formatting needed for a request. 
Here's an example call:

```python
from NasaRandomImages import get_random_nasa_photos

keywords = ['mars', 'rover', 'water']
get_random_nasa_photos(keywords, 'large', 10)
```

# B. How to Programmatically RECIEVE data from the NASA Random Image Microservice

The wrapper function `get_random_nasa_photos` returns an array containing the url strings for the relevant photos on NASA's servers. Take care that the connection
is successful and handle if the microservice is unavailable:
```python
try:
   image_urls = get_random_nasa_photos(keywords, 'large', 10)
   for url in image_urls:
      print(url)
except ConnectionRefusedError, ConnectionError as e:
   # Handle
```

# C. UML Sequence Diagram

