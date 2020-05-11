"""
Django settings for dwitter project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_URL = 'https://www.dwitter.net/'

PARENT_HOST = 'dwitter.net'

REGISTRATION_OPEN = True        # If True, users can register
ACCOUNT_ACTIVATION_DAYS = 7     # One-week activation window; you may, of course, use a different value.
REGISTRATION_AUTO_LOGIN = True  # If True, the user will be automatically logged in.
LOGIN_REDIRECT_URL = BASE_URL        # The page you want users to arrive at after they successful log in
LOGIN_URL = BASE_URL + '/accounts/login/'  # The page users are directed to if they are not logged in,
                                # and are trying to access pages requiring authentication

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

ALLOWED_HOSTS = [
    'dweet.localhost',
    'localhost',
    'www.localhost',
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_filters',
    'rest_framework',
    'rest_framework.authtoken',
    'dwitter',
    'registration',
    'dwitter.user',
    'dwitter.feed',
    'dwitter.dweet',
    'anymail',
    'compressor',
    'dbbackup',
    'debug_toolbar',
    'corsheaders',
    'django_hosts',

]

DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': 'backups'}

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'PAGE_SIZE': 10,                   # Default to 10
    'MAX_PAGE_SIZE': 100,             # Maximum limit allowed when using `?page_size=xxx`.
    'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer',),
    'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework.authentication.TokenAuthentication', )

}

# List of callables that know how to import templates from various sources.
#TEMPLATE_LOADERS = (
#            'django.template.loaders.filesystem.Loader',
#            'django.template.loaders.app_directories.Loader',
#            # 'django.template.loaders.eggs.Loader',
#            )

MIDDLEWARE = [
    'django_hosts.middleware.HostsRequestMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django_hosts.middleware.HostsResponseMiddleware',
]

ROOT_URLCONF = 'dwitter.urls'

ROOT_HOSTCONF = 'dwitter.hosts'
DEFAULT_HOST = 'www'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'builtins': [
                'django_hosts.templatetags.hosts_override',
            ],
        },
    },
]

WSGI_APPLICATION = 'dwitter.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CORS_URLS_REGEX = r'^/api(v2beta)?/.*$'
CORS_ORIGIN_ALLOW_ALL = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        'compressor.finders.CompressorFinder',
        )


def show_debug_toolbar_when_debug_true_but_not_for_the_dweet_subdomain(request):
    if request.host.name == 'dweet':
        return False
    # Import here so that we get the settings from local.py as well
    from django.conf import settings
    return settings.DEBUG


DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK':
    show_debug_toolbar_when_debug_true_but_not_for_the_dweet_subdomain
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'dwitter-default',
    }
}

SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 3600 * 24 * 365 * 100 # Keep user logged in until logout is requested (or 100 years, whichever comes first)
