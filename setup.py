import sys
import setuptools


if not sys.version_info >= (3, 5):
    sys.exit('requires Python 3.5 or newer')


setuptools.setup(
    name='toleo',
    version='0.1',
    description='compare software versions',
    author='Carl George',
    author_email='carl.george@rackspace.com',
    url='https://github.com/carlwgeorge/toleo',
    packages=['toleo'],
    install_requires=[
        'aiohttp',
        'beautifulsoup4>=4.1.2',
        'lxml',
    ],
    extras_require={
        'rpm': ['rpm'],
        'apt': ['apt_pkg'],
        'pacman': ['pyalpm'],
    },
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux'
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ]
)
