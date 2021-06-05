import os.path
from decouple import config
from dj_database_url import parse as db_url
# Django settings for djpodcaster project.

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = config('DJP_DEBUG', default=False, cast=bool)

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': config(
        'DJP_DATABASE_URL',
        cast=db_url),
    # 'ts': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'tangsuanradio',
    #     'USER': '',
    #     'PASSWORD': '',
    # }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = config('DJP_LANGUAGE_CODE', default='en-us')

EMAIL_HOST = config('DJP_EMAIL_HOST', default='localhost')
EMAIL_PORT = config('DJP_EMAIL_PORT', default=25)
EMAIL_HOST_USER = config('DJP_EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('DJP_EMAIL_HOST_PASSWORD', default='')
EMAIL_USE_TLS = config('DJP_EMAIL_USE_TLS', default=True, cast=bool)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), '../../feeds').replace('\\','/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = 'http://media.fmit.cn/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = BASE_DIR + '/static'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = config('DJP_STATIC_URL', default='/static/')

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = config('DJP_SECRET_KEY')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'djpodcaster.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR+'/'+config('DJP_TEMPLATE_DIR', default='templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'djpodcaster.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'tinymce',
    'podcast',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

TINYMCE_DEFAULT_CONFIG = {
    'theme': "advanced",
    'theme_advanced_buttons1': "listbox,bold,italic,underline,separator,link,unlink,separator,bullist,numlist",
    'width': 620,
    'height': 300,
    # 'skin': "o2k7",
}

#DATABASE_ROUTERS = ['podcast.TsRouter']

FEED_PATH = os.path.join(os.path.dirname(__file__), '../../feeds/').replace('\\','/')
FEED_URL = 'http://feed.tangsuanradio.com/'
