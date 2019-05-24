#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name='restaurant-recommender',
    version='0.0.2',
    author='chautran',
    description='Recommender System',
    packages=find_packages(exclude=['test', 'test.*']),
    py_modules=['recommender'],
    install_requires=[
        'SQLAlchemy==1.2.6',
        'nameko==2.8.3',
        'nameko-sqlalchemy==1.1.0',
        'elasticsearch>=5.0.0,<6.0.0',
        # 'pandas==0.23.4',
        # 'scikit-learn==0.20.2',
    ],
    extras_require={
        'dev': [
            'pytest==3.4.2',
            'coverage==4.5.1',
            'flake8==3.5.0',
            'kombu==4.1.0',
        ],
    },
    zip_safe=True
)
