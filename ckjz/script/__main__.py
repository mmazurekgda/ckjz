import requests
import random
import time
import json
from ckjz.constants import TOILET_TYPE

TARGET_IP_ADDRESS = 'localhost'
TARGET_PORT = 3000

def update(name: TOILET_TYPE, status: bool):
    url = f'http://{TARGET_IP_ADDRESS}:{TARGET_PORT}/toilets/{name.value}'
    response = requests.post(
        url,
        params={'status': status},
        headers={"accept": "application/json"},
    )
    return response.json()


if __name__ == '__main__':
    while True:
        for name in TOILET_TYPE:
            time.sleep(1)
            update(name, random.choice([True, False]))

