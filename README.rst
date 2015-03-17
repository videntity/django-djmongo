==================================================
djmongo - A Drop-in Django Application for MongoDB
==================================================


django-djmongo is an "API in a Box".  It provides a web-based UI for MongoDB,
the ability to import data, and create RESTful APIs without the need to write code.

Detailed documentation is in the "docs" directory.  Installation instructions are
below.

Quick Start
-----------

1. Install MongoDB according to http://docs.mongodb.org/manual/installation/
   

2. Pip install django, djmongo, and prerequisites::

    pip install django-djmongo


3. Add the "djmongo" apps and the 3rdparty apps to your
INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        #djmongo
        'djmongo',
        'djmongo.console',
        'djmongo.search',
        'djmongo.dataimport',
        
        #3rd party
        'corsheaders',  #Optional
        'bootstrapform',
        'widget_tweaks',
    )

4. (Optional) Add the CORS  to your middleware::

    MIDDLEWARE_CLASSES = (
        'corsheaders.middleware.CorsMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
    )


5. (Optional) Setup CORS headers.

Add the follwing to allow all GET CORS requests to the bottom of your settings file.
::

    #settings.py
    .
    .
    CORS_ORIGIN_ALLOW_ALL = True
    CORS_ALLOW_METHODS = ('GET',)
    
    
In the simple configuration above, we allow all GET requests from all origins hosts.


6. Append some Djmongo specific settings to your settings file.::

    #Djmongo Settings --------------
    
    #The MongoDB host
    MONGO_HOST = "127.0.0.1"
    
    #The MongoDB port
    MONGO_PORT = 27017
    
    #The default limit on searches (unless specified otherwise).
    MONGO_LIMIT = 200
    
    #The default database name when none is provided.
    MONGO_DB_NAME="nppes"
    
    #The default collection name when none is provided.
    MONGO_MASTER_COLLECTION = "pjson"

    #Instruct Django to accept standard httpauth. (Optional)
    AUTHENTICATION_BACKENDS = (#'djmongo.auth.HTTPAuthBackend',
                           'django.contrib.auth.backends.ModelBackend',)


5. Include the "djmongo" URLconf in your project's urls.py like this::

    
    ...
    # all of these are optional, but if just starting enable all.
    url(r'^',         include('djmongo.urls')),
    url(r'^console/', include('djmongo.console.urls')),
    url(r'^search/',  include('djmongo.search.urls')),
    url(r'^import/',  include('djmongo.dataimport.urls')),



6. Create the models that contain information to help with seacrching and imports.::

    python manage.py syncdb

7. Collect static content::

    python manage.py collectstatic

8. Start the development server::

    python manage.py runserver

9. Point your browser to http://127.0.0.1:8000/console



