#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-tytest',
    version='0.1.0',
    author='Branko Milosavljevic',
    author_email='branko@typhoon-hil.com',
    maintainer='Branko Milosavljevic',
    maintainer_email='branko@typhoon-hil.com',
    license='MIT',
    url='https://github.com/mbranko/pytest-tytest',
    description='Typhoon HIL plugin for pytest',
    long_description=read('README.rst'),
    py_modules=['pytest_tytest'],
    python_requires='>=3.5',
    install_requires=['pytest>=5.0.0', 'pytz>=2020.1', 'tzlocal>=2.1', 'requests>=2.23'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'tytest = pytest_tytest',
        ],
    },
)