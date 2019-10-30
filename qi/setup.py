#-*- coding: utf-8 -*-

import sys
import setuptools
import configparser
from setuptools import setup

config = configparser.ConfigParser()
config.read('conf.ini')

setup(name="qi",
      version=config["qi"]["version"],
      author=config["qi"]["author"],
      author_email=config["qi"]["author_email"],
      url=config["qi"]["url"],
      packages=setuptools.find_packages()
)