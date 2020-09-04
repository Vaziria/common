import gevent
from pprint import pprint
import json
from requests import Session
import os
import csv


cek = not os.path.exists('hasil_resi.csv')

csvfile = open('hasil_resi.csv', 'a+', newline='')
fieldnames = ['resi', 'status', 'tanggal']
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

if cek:
	writer.writeheader()


class Worker:
	session = None

	def __init__(self):
		self.session = Session()

	def get_home():
		
		url = 'https://www.cekpengiriman.com/'

		headers = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
			"Origin": "https://www.cekpengiriman.com",


		}

		req = self.session.get(url, headers = headers)

		return req.status_code == 200



def req_resi(resi):

	url = 'https://www.cekpengiriman.com/wp-content/themes/resiongkir/data/data.php'

	headers = {
		"X-Requested-With": "XMLHttpRequest",
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
		"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
		"Origin": "https://www.cekpengiriman.com",
		"Sec-Fetch-Site": "same-origin",
		"Sec-Fetch-Mode": "cors",
		"Sec-Fetch-Dest": "empty",
		"Referer": "https://www.cekpengiriman.com/",


	}

	payload = {
		"nomor": resi,
		"kurir": "ninja",
		"type": "waybill"
	}

	req = _session.post(url, headers = headers, data = payload)

	if req.status_code == 200:
		return json.loads(req.text)

	print(req.status_code)

	return False




def get_data(path):

	with open(path, 'r') as out:
		hasil = out.read()

	hasil = hasil.split('\n')

	hasil = list(map(lambda x: x.strip(), hasil))

	return hasil

def parse_data(data):

	result = data['rajaongkir']['result']
	last = result['manifest'][-1]
	return {
		'tanggal': result['delivery_status']['pod_date'],
		'status': result['delivery_status']['status']
	}
	
	


def write_csv(data):
	
	writer.writerow(data)


def run():
	get_home()

	for resi in get_data('resi.txt'):
		print('print checking {}'.format(resi))
		try:
			data = req_resi(resi)
			data = parse_data(data)
		except Exception as e:
			print(e)
			continue

		data['resi'] = resi

		write_csv(data)






if __name__ == '__main__':
	from pprint import pprint

	run()