#!/usr/bin/env python

from setuptools import find_packages, setup

setup(name='Mongo REST',
      version='0.1.0',
      description='MongoDB REST Server',
      author='Brett Langdon',
      author_email='brett@blangdon.com',
      url='http://ww.github.com/brettlangdon/mongo-rest',
      install_requires=['pymongo', 'flask', 'flask-restful', 'jsonschema'],
      packages=find_packages())
