==================================================
djmongo - A Drop-in Django Application for MongoDB
==================================================
0.6.1 (beta)

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

    #Make sure you have a static root set.
    STATIC_ROOT = str(os.path.join(BASE_DIR, 'collectedstatic'))
    #Djmongo Settings --------------
    
    #Pretty Bootstrap3 messages.
    from django.contrib.messages import constants as messages
    MESSAGE_TAGS ={ messages.DEBUG: 'debug',
                messages.INFO: 'info',
                messages.SUCCESS: 'success',
                messages.WARNING: 'warning',
                messages.ERROR: 'danger',}


    #Set the MongoDB host
    MONGO_HOST = "127.0.0.1"
    
    #Set the MongoDB port
    MONGO_PORT = 27017
    
    #Set the default limit on searches (unless specified otherwise).
    MONGO_LIMIT = 200
    
    #Instruct Django to accept standard httpauth. (Optional)
    AUTHENTICATION_BACKENDS = (#'djmongo.auth.HTTPAuthBackend',
                           'django.contrib.auth.backends.ModelBackend',)
                           
    #Setting DEFAULT_TO_OPEN_READ to True removes any authentication or group requirements
    #to view or search data. When set to true, you need to explicity define it as open in
    #the Console/Database Access model within the django admin.
    DEFAULT_TO_OPEN_READ = False
                           
                           


7. Include the "djmongo" URLconf in your project's urls.py like this::

    
    ...
    # all of these are optional, but if just starting enable all.
    url(r'^',         include('djmongo.urls')),
    url(r'^console/', include('djmongo.console.urls')),
    url(r'^search/',  include('djmongo.search.urls')),
    url(r'^import/',  include('djmongo.dataimport.urls')),



8. Create the models that contain information to help with seacrching and imports.

On Django 1.6::

    python manage.py syncdb

On django 1.7+::

    python manage.py migrate


9. Collect static content::

    python manage.py collectstatic

10. Start the development server::

    python manage.py runserver

11. Point your browser to http://127.0.0.1:8000



