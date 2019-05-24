#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name='restaurant-authentication',
    version='0.0.1',
    author='chautran',
    description='Django-Authentication for Restaurant application',
    packages=find_packages(exclude=['test', 'test.*']),
    py_modules=['authentication'],
    install_requires=[
        "Django==2.0.4",
        "configparser==3.5.0",
        'hashids==1.2.0',
        'psycopg2==2.7.4',
        'uwsgi==2.0.17'
    ],
    extras_require={
        'dev': [
            'pytest==3.4.2',
            'coverage==4.5.1',
            'flake8==3.5.0'
        ],
    },
    zip_safe=True
)
