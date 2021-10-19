#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name='restaurant-products',
    version='0.0.2',
    description='Store and serve products in a restaurant',
    author='chautran',
    packages=find_packages(exclude=['test', 'test.*']),
    py_modules=['products'],
    install_requires=[
        "marshmallow==2.15.0",
        "nameko==2.14.0",
        "redis==2.10.6"
    ],
    extras_require={
        'dev': [
            'pytest==3.4.2',
            'coverage==4.5.1',
            'flake8==3.5.0',
            'kombu==4.1.0'
        ]
    },
    zip_safe=True,
)
