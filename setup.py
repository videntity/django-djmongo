import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-djmongo',
    version='0.7.6.4',
    packages=['djmongo', 'djmongo.console', 'djmongo.console.migrations',
              'djmongo.accounts', 'djmongo.accounts.migrations',
              'djmongo.aggregations', 'djmongo.aggregations.migrations',
              'djmongo.write', 'djmongo.write.migrations',
              'djmongo.management.commands',
              'djmongo.management',
              'djmongo.search', 'djmongo.search.migrations',
              'djmongo.dataimport', 'djmongo.dataimport.migrations', ],
    include_package_data=True,
    license='GPL2',
    description='A reusable Django application providing a web interface for MongoDB and a RESTFul API Toolkit.',
    long_description=README,
    url='https://github.com/videntity/django-djmongo',
    author='Alan Viars',
    author_email='sales@videntity.com',
    install_requires=[
        'django==1.9.5', 'pymongo', 'django-widget-tweaks',
        'django-bootstrap-form',
        'django-cors-headers', 'jdt', 'jsonschema',
        'django-localflavor'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
