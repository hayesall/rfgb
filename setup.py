"""
Setup file for rfgb
"""

from setuptools import setup
from setuptools import find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# Get __version__ from _metadata.py
with open(path.join("rfgb", "_metadata.py")) as f:
    exec(f.read())

setup(
    name='rfgb',
    version=__version__,
    license=__license__,

    description='Relational Functional Gradient Boosting in Python.',
    long_description=long_description,

    author='Alexander L. Hayes',
    author_email='hayesall@iu.edu',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    keywords='relational-learning',
    project_urls={
        'Source Code': 'https://github.com/hayesall/rfgb',
        'Bug Tracker': 'https://github.com/hayesall/rfgb/issues',
        'Documentation': 'https://rfgb.readthedocs.io/en/latest/',
    },

    entry_points={
        'console_scripts': ['rfgb=rfgb.__main__']
    },

    packages=find_packages(exclude=['tests'])
)
