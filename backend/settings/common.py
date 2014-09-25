"""
Django settings for backend project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

from configurations import Configuration


class Common(Configuration):

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = os.environ.get('SECRET_KEY', None)
    # '^zw8t-tw1(^5qn$t@ng2f_w#d-%hsc6a^tet+vo&(=s1s^ioic'

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    TEMPLATE_DEBUG = True

    ALLOWED_HOSTS = []

    # Application definition

    INSTALLED_APPS = (
        'suit',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        # 3rd patry
        'rest_framework',
        'pipeline',

        # applications
        'backend.main',
    )

    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        # 3rd parties
        'pipeline.middleware.MinifyHTMLMiddleware',
    )

    ROOT_URLCONF = 'backend.urls'

    WSGI_APPLICATION = 'backend.wsgi.application'

    # Database
    # https://docs.djangoproject.com/en/1.7/ref/settings/#databases

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db', 'db.sqlite3'),
        }
    }

    # Internationalization
    # https://docs.djangoproject.com/en/1.7/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.7/howto/static-files/

    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'assets')

    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'static'),  # static files
        os.path.join(BASE_DIR, 'client'),  # client side code
    )

    STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'

    # Templates

    TEMPLATE_DIRS = (
        os.path.join(BASE_DIR, 'templates'),
    )

    TEMPLATE_CONTEXT_PROCESSORS = Configuration.TEMPLATE_CONTEXT_PROCESSORS + (
        'django.core.context_processors.request',
        'backend.common.context.partials_list',  # list of partial templates for angularJS
    )

    # Logging configuration

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,

        'formatters': {
            'simple': {
                'format': '%(levelname)s %(message)s',
            },
        },

        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
            },
        },

        'loggers': {
            'backend.libs': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True,
            },
        },
    }

    # ********************
    # 3rd parties settings
    # ********************

    # Django Suit configuration example

    SUIT_CONFIG = {
        'ADMIN_NAME': 'Code sample - django project',
        'MENU_EXCLUDE': ('auth.group', 'auth'),
    }

    # django-pipeline

    PIPELINE_CSS = {
        'theme': {
            'source_filenames': (
                'vendors/bootstrap/dist/css/bootstrap.min.css',
                'css/theme.css',
            ),
            'output_filename': 'theme.css',
            'extra_context': {
                'media': 'screen,projection',
            },
        },
    }

    PIPELINE_JS = {
        'vendors': {
            'source_filenames': (
                'vendors/angularjs/angular.min.js',
                'vendors/angular-animate/angular-animate.min.js',
                'vendors/angular-route/angular-route.min.js',
                'vendors/angular-resource/angular-resource.min.js',
                'vendors/angular-bootstrap/ui-bootstrap-tpls.min.js',
            ),
            'output_filename': 'vendors.js',
        },
        'client': {
            'source_filenames': (
                'app.js',
                'controllers/*.js',
            ),
            'output_filename': 'client.js',
        },
    }
