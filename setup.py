try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

config = {
	'name': 'TVDB Multipurpose Interface',
	'version': '0.1',
	'url': 'https://github.com/parnellj/tvdb_interface',
	'download_url': 'https://github.com/parnellj/tvdb_interface',
	'author': 'Justin Parnell',
	'author_email': 'parnell.justin@gmail.com',
	'maintainer': 'Justin Parnell',
	'maintainer_email': 'parnell.justin@gmail.com',
	'classifiers': [],
	'license': 'GNU GPL v3.0',
	'description': 'Downloads episode lists and data for specified television series via TVDB.',
	'long_description': 'Downloads episode lists and data for specified television series via TVDB.',
	'keywords': '',
	'install_requires': ['nose'],
	'packages': ['tvdb_interface'],
	'scripts': []
}
	
setup(**config)
