# encoding: utf-8

"""
    mana
    ~~~~

    happy generate flask project
"""
from setuptools import setup, find_packages


setup(
    name='muxi',
    version='0.11',
    packages=find_packages(),
    url='https://github.com/neo1218/muxi',
    license='MIT',
    author='neo1218',
    author_email='neo1218@yeah.net',
    description='generate muxi project',
    long_description=__doc__,
    # if you would be using a package instead use packages instead
    # of py_modules:
    # packages=['flask_sqlite3'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'click'
    ],
    # /mana/mana.py/click::mana
    entry_points='''
        [console_scripts]
        muxi=cli:cli
    ''',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
