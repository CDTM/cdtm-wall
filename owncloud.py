import os
import requests
from requests.auth import HTTPBasicAuth


def get_photos():
    res = requests.get('https://home.cdtm.de/index.php/apps/gallery/api/thumbnails',
                 auth=HTTPBasicAuth(os.environ['CDTM_USER'], os.environ['CDTM_PASSWORD']))
    data = res.json()
    return data
