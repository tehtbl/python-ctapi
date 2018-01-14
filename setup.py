#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='python-ctapi',
    version='0.3.0',
    packages=['ctapi'],
    install_requires=[
        'requests==2.18.4',
        'future==0.16.0',
        'PyYAML==3.11',
    ],

    author='tbl42',
    author_email='cyberworker@posteo.de',
    url='https://github.com/tbl42/python-ctapi',
    description='Python Interface for CoinTracking.info API',
    long_description=open('README.md').read(),
    keywords = 'cointracking info btc api',
    license='MIT',

    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Topic :: Office/Business :: Financial',
    ]

)
