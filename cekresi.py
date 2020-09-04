from gevent import monkey
import os

os.environ['logfile'] = 'logs/resi'

if __name__ == '__main__':
	monkey.patch_all()

import gevent
from gevent.pool import Pool

import random
import time

from app.config import _config
from app.worker import Worker
from app.report import Report


from vazutils.logger import Logger
	
logger = Logger(__name__)

_report = Report()



def get_data(path):

	with open(path, 'r') as out:
		hasil = out.read()

	hasil = hasil.split('\n')

	hasil = list(map(lambda x: x.strip(), hasil))

	return hasil


def create_worker(num):
	hasil = []

	for c in range(0, num):
		worker = Worker(c)
		
		worker.get_home()

		hasil.append(worker)

	return hasil


def cek_resi(worker, resi):
	data = worker.req_resi(resi)
	data = worker.parse_data(data)
	data['resi'] = resi

	_report.write(data)
	logger.info(' {} checked'.format(resi) )

def run():

	workers = create_worker(_config.get('count_worker', 4))

	for resi in get_data('resi.txt'):
		try:
			worker = random.choice(workers)

			yield {
				"func": cek_resi,
				"param": [ worker, resi ]
			}

		except Exception as e:
			logger.error(e, exc_info=True)



def run_gevent():

	worker = _config.get('count_worker', 4)
	pool = Pool(worker)

	funcs = run()

	while True:
		

		if pool.full():
			time.sleep(1)
			continue

		# getting func delete
		try:
			funcnya = next(funcs)
			pool.spawn(funcnya['func'], *funcnya['param'])
		
		except StopIteration as e:
			
			if pool.free_count() == worker:
				break



		time.sleep(0.01)


		# gevent.wait()




if __name__ == '__main__':
	from pprint import pprint

	run_gevent()