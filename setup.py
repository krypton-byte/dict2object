from setuptools import setup
from os import path
base_dir = path.abspath(path.dirname(__file__))
setup(
  name = 'dictionary to object',
  packages = ['dict2object'],
  include_package_data=True,
  version = '0.0.1',
  license='MIT',
  description = 'Python dictionray to Object',
  author = 'Krypton Byte',
  author_email = 'galaxyvplus6434@gmail.com',
  url = 'https://github.com/krypton-byte/dict2object',
  download_url = 'https://github.com/krypton-byte/dict2object/archive/0.0.1.tar.gz',
  keywords = ['json','dictionary', 'object', 'toObject'],
  install_requires=[],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)