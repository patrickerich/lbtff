from setuptools import setup
from setuptools import find_packages
from os import path
from lbtff import __version__


def read_file(fname):
    with open(path.join(path.dirname(__file__), fname), encoding="utf8") as f:
        return f.read()


setup(
    name='lbtff',
    version=__version__,  # noqa: F821
    description='Line based text file filter',
    url='https://github.com/patrickerich/lbtff',
    license='MIT',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    author='Patrick Erich',
    author_email='git@patrickerich.email',
    packages=find_packages(),
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'lbtff = lbtff.cli:main',
        ]
    },
    platforms='any',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: '
        'Electronic Design Automation (EDA)',
        'Topic :: Utilities',
    ],
    zip_safe=False
)
