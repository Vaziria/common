import os

import yaml


dir_init = [
	'./report'
]

# create init dir

for d in dir_init:
	if os.path.exists(d):
		os.makedirs(d)




if __name__ == '__main__':
	pass