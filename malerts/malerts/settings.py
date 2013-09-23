import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Chris Han', 'chan@zehnergroup.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.mysql',	# Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',							# Or path to database file if using sqlite3.
        'USER': '',									# Not used with sqlite3.
        'PASSWORD': '',								# Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        'OPTIONS': { 'init_command': 'SET storage_engine=MYISAM;' },	# This is SPATIAL INDEXES
    }	
}

GEOS_LIBRARY_PATH = "/usr/local/lib/libgeos_c.so"

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/var/www/envs/alerts_django/media/'
STATIC_ROOT = '/var/www/envs/alerts_django/static/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = 'http://alerts.metro.net/media/'
STATIC_URL = 'http://alerts.metro.net/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'ly-s%%#&+x(9%_qb#(&3w4rtzs^&)=gmff!lajsch;oihqefgh16ipjik#63w_!'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'malerts.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
	'grappelli',	# import this BEFORE django.contrib.admin
	'django_wysiwyg',
	'ckeditor',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.gis',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'gtfs',
    'south',
    'tastypie',
    'backbone_tastypie',
    'tastypie_swagger',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
)

# DEVSERVER
DEVSERVER_ARGS = []
# Additional command line arguments to pass to the runserver command (as defaults).
DEVSERVER_DEFAULT_ADDR = '127.0.0.1'
# The default address to bind to.
DEVSERVER_DEFAULT_PORT = '8082'
# The default port to bind to.
# DEVSERVER_WSGI_MIDDLEWARE
# A list of additional WSGI middleware to apply to the runserver command.
DEVSERVER_MODULES = []
# A list of devserver modules to load.
DEVSERVER_IGNORED_PREFIXES = ['/media', '/uploads', 'static']
# A list of prefixes to surpress and skip process on. By default, 
# ADMIN_MEDIA_PREFIX, MEDIA_URL and STATIC_URL (for Django >= 1.3) 
# will be ignored (assuming MEDIA_URL and STATIC_URL is relative):

# GRAPPELLI
GRAPPELLI_ADMIN_TITLE = 'ALERTS.METRO.NET'

# SWAGGER
# TASTYPIE_SWAGGER_API_MODULE = 'mainsite.urls.api'

# DJANGO-WYSIWYG
DJANGO_WYSIWYG_FLAVOR = "ckeditor"
# DJANGO_WYSIWYG_FLAVOR = 'yui'       # Default
DJANGO_WYSIWYG_FLAVOR = 'ckeditor'  # Requires you to also place the ckeditor files here:
DJANGO_WYSIWYG_MEDIA_URL = STATIC_URL + "ckeditor/"

# DJANGO-CKEDITOR
CKEDITOR_UPLOAD_PATH = "/var/www/metro_alerts/media/uploads"
CKEDITOR_UPLOAD_PREFIX = "http://alerts.metro.net/media/uploads/"
CKEDITOR_CONFIGS = {
	'default': {
        'toolbar': [
            [      'Undo', 'Redo',
              '-', 'Bold', 'Italic', 'Underline',
              '-', 'Link', 'Unlink', 'Anchor',
              '-', 'Format',
              '-', 'SpellChecker', 'Scayt',
              '-', 'Maximize',
            ],
            [      'HorizontalRule',
              '-', 'Table',
              '-', 'BulletedList', 'NumberedList',
              '-', 'Cut','Copy','Paste','PasteText','PasteFromWord',
              '-', 'SpecialChar',
              '-', 'Source',
              '-', 'About',
            ]
        ],
        'width': 750,
        'height': 100,
	},
}
"""
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': [
            [      'Undo', 'Redo',
              '-', 'Bold', 'Italic', 'Underline',
              '-', 'Link', 'Unlink', 'Anchor',
              '-', 'Format',
              '-', 'SpellChecker', 'Scayt',
              '-', 'Maximize',
            ],
            [      'HorizontalRule',
              '-', 'Table',
              '-', 'BulletedList', 'NumberedList',
              '-', 'Cut','Copy','Paste','PasteText','PasteFromWord',
              '-', 'SpecialChar',
              '-', 'Source',
              '-', 'About',
            ]
        ],
        'width': 840,
        'height': 300,
        'toolbarCanCollapse': False,
    }
}
"""

try:
    from settings_local import *
except ImportError:
    pass
