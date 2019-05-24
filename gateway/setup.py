#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name='restaurant-gateway',
    version='0.0.2',
    author='chautran',
    description='Gateway for Restaurant application',
    packages=find_packages(exclude=['test', 'test.*']),
    py_modules=['gateway'],
    install_requires=[
        'marshmallow==2.15.0',
        'nameko==2.8.3',
        'Flask-API',
        'configparser==3.5.0',
        'hashids==1.2.0',
        'werkzeug',
        'redis',
        'django',
        'pytest==3.4.2',
    ],
    extras_require={
        'dev': [
            'coverage==4.5.1',
            'flake8==3.5.0'
        ],
    },
    zip_safe=True
)
