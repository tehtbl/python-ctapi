#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='python-ctapi',
    version='0.3.1',
    packages=['ctapi'],
    install_requires=[
        'requests==2.22.0',
        'PyYAML==5.1.2',
    ],

    author='tehtbl',
    author_email='cyberworker@posteo.de',
    url='https://github.com/tehtbl/python-ctapi',
    description='Python Interface for CoinTracking.info API',
    long_description=open('README.md').read(),
    keywords='CoinTracking info btc api coin tracking',
    license='MIT',

    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Topic :: Office/Business :: Financial',
    ]

)
