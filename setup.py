#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 Ben Lindsay <benjlindsay@gmail.com>

from distutils.core import setup

desc = 'A module for automating comput job creation and submission'

with open('README.rst', 'r') as f:
    long_desc = f.read()

setup(
  name = 'create_jobs',
  packages = ['create_jobs'],
  version = '0.1.1',
  description = desc,
  long_description = long_desc,
  requires = ['numpy', 'pandas'],
  install_requires = ['numpy', 'pandas'],
  scripts = ['bin/create_jobs'],
  author = 'Ben Lindsay',
  author_email = 'benjlindsay@gmail.com',
  url = 'https://github.com/benlindsay/create_jobs',
  keywords = ['workflow', 'simulations'],
  classifiers = [],
)
