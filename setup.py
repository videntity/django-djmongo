import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    long_description_content_type="text/markdown",
    name='django-djmongo',
    version='0.7.6.8',
    packages=['djmongo', 'djmongo.console', 'djmongo.console.migrations',
              'djmongo.accounts', 'djmongo.accounts.migrations',
              'djmongo.aggregations', 'djmongo.aggregations.migrations',
              'djmongo.write', 'djmongo.write.migrations',
              'djmongo.management.commands',
              'djmongo.management',
              'djmongo.read', 'djmongo.read.views', 'djmongo.read.migrations',
              'djmongo.delete', 'djmongo.delete.views', 'djmongo.delete.migrations',
              'djmongo.dataimport', 'djmongo.dataimport.migrations', ],
    include_package_data=True,
    license='GPL2',
    description='A reusable Django application providing a web interface for MongoDB and a RESTful API Toolkit.',
    long_description=README,
    url='https://github.com/videntity/django-djmongo',
    author='Alan Viars',
    author_email='sales@videntity.com',
    install_requires=[
        'django==2.2.7', 'pymongo', 'django-widget-tweaks',
        'django-bootstrap-form',
        'django-cors-headers', 'jdt', 'jsonschema',
        'django-localflavor', 'django-markdown-deux', ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
