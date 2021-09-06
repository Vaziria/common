import requests
from lxml import etree
import random
import string
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder
from requests_toolbelt.utils import dump
import time
import base64

class CekPengiriman:
    def get_options(self, fname):
        url = 'https://www.cekpengiriman.com/cek-resi'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
        }

        req = requests.get(url, headers=headers)

        if req.status_code != 200:
            print('gagal --- '.format(req.text))
            return False

        hasil = etree.HTML(req.text)
        options = hasil.xpath('//select[@name="kurir"]/option')
        hasil = {}
        for option in options:
            key = option.attrib.get('value')

            if key == '':
                continue

            hasil[key] = option.text

        with open(fname, 'w+') as out:
            json.dump(hasil, out, indent=4, sort_keys=True)

        return hasil

    def cekresi(self, kurirtipe, resi):
        session = requests.Session()
        tsession = int(time.time() * 1000)
        url = 'https://www.cekpengiriman.com/wp-content/themes/cp/data/awb/{}.php'.format(kurirtipe)

        payload = {
            "nomor": resi,
            "kurir": kurirtipe,
            "type": "awb",
            "uuid": self.create_token(tsession)
        }
        boundary = '----WebKitFormBoundary' \
           + ''.join(random.sample(string.ascii_letters + string.digits, 16))
        mp_encoder = MultipartEncoder(
            fields=payload,
            boundary=boundary
        )

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
            'Referer': 'https://www.cekpengiriman.com/cek-resi?resi={}&kurir={}'.format(resi, kurirtipe),
            'Content-Type': mp_encoder.content_type,
            'Origin': 'https://www.cekpengiriman.com',
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty"

        }

        cookies = {
            "time_session": str(tsession)
        }

        req = session.post(url, headers=headers, data=mp_encoder.to_string(), cookies=cookies)

        if req.status_code != 200:
            print(req.text)
            return False

        return req.json()

    def create_token(self, data):
        data = str(data).encode('utf8')
        data = base64.b64encode(data)
        data = base64.b64encode(data)
        
        hasil = ''
        for car in data.decode('utf8'):
            car = ord(car)
            index = 48 ^ car
            hasil += chr(index)

        hasil = base64.b64encode(hasil.encode('utf8'))

        return hasil


if __name__ == '__main__':
    from pprint import pprint
    cek = CekPengiriman()
    # hasil = cek.get_options('list.txt')
    hasil = cek.cekresi('jnt', 'JP0796360242')
    # hasil = cek.create_token("1630940474114")

    pprint(hasil)