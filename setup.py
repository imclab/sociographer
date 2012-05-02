#!/usr/bin/env python2

import setuptools
from distutils.core import setup

setup(name='sociographer',
      version='0.1',
      description='Social graph visualizer.',
      author='Tony Young',
      author_email='tony@rfw.name',
      packages=['sociographer'],
      entry_points={
        "console_scripts": [
          'sociographer = sociographer:main'
      ]}
     )

