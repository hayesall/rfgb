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

# Import rfgb in order to read the metadata.
import rfgb

setup(
    name='rfgb',
    version=rfgb.__version__,
    license=rfgb.__license__,

    description='Relational Functional Gradient Boosting in Python.',
    long_description=long_description,

    author='Alexander L. Hayes',
    author_email='alexander@batflyer.net',

    classifiers=[
        # Development Information
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        'Intended Audience :: Science/Research',

        # Supported Python versions
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],

    keywords='relational-learning',
    project_urls={
        'Source': 'https://github.com/starling-lab/rfgb.py',
        'Tracker': 'https://github.com/starling-lab/rfgb.py/issues'
    },

    packages=find_packages(exclude=['tests'])
)
