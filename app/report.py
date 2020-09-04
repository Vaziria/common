import csv
from datetime import datetime

from . import config

class Report:
	basename = 'report/resi_{}.csv'
	writer = None,
	headers = ['resi', 'status', 'tanggal']

	def __init__(self):
		waktu = str(datetime.utcnow())
		waktu = waktu.split('.')
		waktu = waktu[0]
		waktu = waktu.replace(':', '.')
		waktu = waktu.replace(' ', '_')

		fname = self.basename.format(waktu)

		csvfile = open(fname, 'w+', newline='')
		writer = csv.DictWriter(csvfile, fieldnames = self.headers)
		writer.writeheader()

		self.writer = writer

	def write(self, data):

		self.writer.writerow(data)


if __name__ == '__main__':

	report = Report()

	report.write({
			'resi': "asdasdasdas"
		})