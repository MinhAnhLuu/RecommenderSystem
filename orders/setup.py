#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name='restaurant-orders',
    version='0.0.2',
    author='chautran',
    description='Store and serve orders in a restaurant',
    packages=find_packages(exclude=['test', 'test.*']),
    py_modules=['orders'],
    install_requires=[
        'SQLAlchemy==1.2.6',
        'nameko==2.14.0',
        'nameko-sqlalchemy==1.1.0',
        #'alembic==1.0.2',
        'marshmallow==2.15.0',
        'psycopg2==2.7.4',
        'hashids==1.2.0'
    ],
    extras_require={
        'dev': [
            'pytest==3.4.2',
            'coverage==4.5.1',
            'flake8==3.5.0',
            'kombu==4.1.0'
        ],
    },
    zip_safe=True
)
