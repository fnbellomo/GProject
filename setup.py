from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup
from setuptools import find_packages

setup(name=’GProject’,
      version = '1.0',
      author = 'Ezequiel Fogliatto, Franco Bellomo, Michel Aguena, David',
      author_email = '',
      url = 'http://example.com',
      packages = find_packages(numpy, matplotlib);
      )
