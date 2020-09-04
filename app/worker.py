import gevent
from pprint import pprint
import json
from requests import Session
import os
import csv

from vazutils.logger import Logger

logger = Logger(__name__)



class Worker:
	session = None
	idnya = None

	def __init__(self, idnya):
		self.session = Session()
		self.idnya = idnya

	def log(self, act, msg):
		logfunc = getattr(logger, act)

		msg = '[ worker {} ] {}'.format(self.idnya, msg)

		logfunc(msg)


	def get_home(self):
		self.log('info', 'getting cookies')

		url = 'https://www.cekpengiriman.com/'

		headers = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
			"Origin": "https://www.cekpengiriman.com",


		}

		req = self.session.get(url, headers = headers)

		return req.status_code == 200



	def req_resi(self, resi):

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

		req = self.session.post(url, headers = headers, data = payload)

		if req.status_code == 200:
			return json.loads(req.text)


		self.log('error', 'resi {} error'.format(resi))

		return False


	def parse_data(self, data):

		result = data['rajaongkir']['result']
		last = result['manifest'][-1]
		return {
			'tanggal': result['delivery_status']['pod_date'],
			'status': result['delivery_status']['status']
		}