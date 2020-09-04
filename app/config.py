import os
import yaml

from vazutils.logger import Logger

logger = Logger(__name__)


dir_init = [
	'./report'
]

# create init dir

for d in dir_init:
	if not os.path.exists(d):
		os.makedirs(d)


_config = {}

if os.path.exists('config.yaml'):
	with open('config.yaml', 'r') as out:

		data = yaml.load(out.read(), Loader=yaml.SafeLoader)
		_config.update(data)

else:

	logger.error('tidak ada config.....')




if __name__ == '__main__':
	
	print(_config)