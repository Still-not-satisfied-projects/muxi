# coding: utf-8
# muxi~setup~file

"""
	setup.py
	~~~~~~~~

		:muxi: a python web framework
			~simple and powerful~
"""

from setuptools import setup


setup(
	name='muxi',
	version=0.11,
	url='http://github.com/neo1218/muxi/',
    license='MIT',
    author='neo1218',
    author_email='neo1218@yeah.net',
    description='a python web framework'
                'simple and powerful',
    long_description=__doc__,
    packages=['muxi', 'muxi.cli', 'muxi.form'],  # packages is importent
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Werkzeug>=0.7',
        'Jinja2>=2.4',
        'itsdangerous>=0.21',
        'click>=2.0',
		'mana>=2.6',
		'flask-wtf'
		# what's more...
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    entry_points='''
        [console_scripts]
		muxi=muxi.cli.cli:cli
    '''
)
