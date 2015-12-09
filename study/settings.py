import os
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
from study.utils import generate_random_string

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


CONFIG_DEFAULTS = {
    'site_url': 'http://127.0.0.1:9500',
    'debug_mode': False,
    'secret_key': generate_random_string(48),
    'postgresql': {
        'host': '127.0.0.1',
        'port': 5432,
        'database': 'study',
        'username': 'study_web',
        'password': 'fancyc0ws',
        'conn_max_age': 120,
    },
    'redis': {
        'host': '127.0.0.1',
        'port': 6379,
        'database': 1,
        'password': 'bouncingcl0uds',
    },
    'smtp': {
        'host': '127.0.0.1',
        'port': 1025,
    },
    'allowed_hosts': [
        '*',
    ],
    'graph_api': {
        'appid': '',
        'appsecret': '',
    }
}
CONFIG_FILE = os.path.join(BASE_DIR, 'config.yml')
CONFIG_ROOT = dict()


def load_config(config_file=None):
    global CONFIG_ROOT
    config_file = config_file or CONFIG_FILE

    with open(config_file, 'r') as stream:
        CONFIG_ROOT = yaml.load(stream, Loader=Loader)


def save_config(destination_file=None, defaults=False):
    destination_file = destination_file or CONFIG_FILE
    config = CONFIG_ROOT if not defaults else CONFIG_DEFAULTS

    with open(destination_file, 'w+') as stream:
        stream.write(yaml.dump(config, default_flow_style=False, Dumper=Dumper))


if not os.path.exists(CONFIG_FILE):
    save_config(defaults=True)
    CONFIG_ROOT = CONFIG_DEFAULTS
else:
    load_config()


# ###########################################
# #+---------------------------------------+#
# #|         Application settings          |#
# #+---------------------------------------+#
# ###########################################

SECRET_KEY = CONFIG_ROOT.get('secret_key')
DEBUG = CONFIG_ROOT.get('debug_mode', False)
ALLOWED_HOSTS = CONFIG_ROOT.get('allowed_hosts', [])
ROOT_URLCONF = 'study.urls'
WSGI_APPLICATION = 'study.wsgi.application'
LOGIN_URL = '/user/login/'


# ###########################################
# #+---------------------------------------+#
# #|        Application definition         |#
# #+---------------------------------------+#
# ###########################################

INSTALLED_APPS = (
    # Internal applications
    'core',
    'user',
    'cal',

    # Django applications
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd applications
    'social.apps.django_app.default',
    'djcelery',
    'django_markdown',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

AUTHENTICATION_BACKENDS = (
    # python-social-auth
    'social.backends.facebook.FacebookOAuth2',

    'django.contrib.auth.backends.ModelBackend',
)

AUTH_USER_MODEL = 'user.UserProfile'

# ###########################################
# #+---------------------------------------+#
# #|               Templates               |#
# #+---------------------------------------+#
# ###########################################

def get_template_loaders():
    if DEBUG:
        return [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader'
        ]

    return [
            ('django.template.loaders.cached.Loader', (
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ))
        ],


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # python-social-auth
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
            ],
            'loaders': get_template_loaders(),
        },
    },
]


# ###########################################
# #+---------------------------------------+#
# #|               Databases               |#
# #+---------------------------------------+#
# ###########################################

_CONFIG_POSTGRESQL = CONFIG_ROOT.get('postgresql')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': _CONFIG_POSTGRESQL.get('host'),
        'PORT': _CONFIG_POSTGRESQL.get('port'),
        'NAME': _CONFIG_POSTGRESQL.get('database'),
        'USER': _CONFIG_POSTGRESQL.get('username'),
        'PASSWORD': _CONFIG_POSTGRESQL.get('password'),
        'CONN_MAX_AGE': _CONFIG_POSTGRESQL.get('conn_max_age'),
    }
}


# ###########################################
# #+---------------------------------------+#
# #|                Caches                 |#
# #+---------------------------------------+#
# ###########################################

_CONFIG_REDIS = CONFIG_ROOT.get('redis')


def get_redis_config():
    if 'host' in _CONFIG_REDIS:
        location = "%s:%d" % (_CONFIG_REDIS.get('host'), _CONFIG_REDIS.get('port', 6379))
    elif 'unix_socket_path' in _CONFIG_REDIS:
        location = _CONFIG_REDIS.get('unix_socket_path')
    else:
        raise ValueError("Redis host or unix socket path must be set")

    def options():
        kwargs = {
            'PARSER_CLASS': 'redis.connection.HiredisParser',
        }

        if 'password' in _CONFIG_REDIS:
            kwargs['PASSWORD'] = _CONFIG_REDIS.get('password')

        return kwargs

    kwargs = {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': location,
        'OPTIONS': options()
    }

    return kwargs

CACHES = {
    'default': get_redis_config()
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'


# ###########################################
# #+---------------------------------------+#
# #|          Internationalization         |#
# #+---------------------------------------+#
# ###########################################

LOGS_DIR = os.path.join(BASE_DIR, "logs")
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR, exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': "%(asctime)s %(levelname)s %(name)s %(message)s",
        },
        'detailed': {
            'format': "%(asctime)s %(levelname)s %(name)s %(process)d %(thread)d %(message)s",
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': "logging.NullHandler",
        },
        'console': {
            'level': 'DEBUG',
            'class': "logging.StreamHandler",
            'formatter': 'simple',
        },
        'file': {
            'level': 'DEBUG',
            'class': "logging.handlers.RotatingFileHandler",
            'filename': os.path.join(LOGS_DIR, "django.log"),
            'maxBytes': 1024*1024*5,
            'backupCount': 25,
            'formatter': 'detailed',
        },
    },
    'loggers': {
        'django': {
            'handlers': {
                'file',
                'console',
            },
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': {
                'file',
            },
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': {
                'console',
            },
            'level': 'DEBUG',
            'propagate': True,
        },
        '': {
            'handlers': {
                'file',
                'console',
            },
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# ###########################################
# #+---------------------------------------+#
# #|          Internationalization         |#
# #+---------------------------------------+#
# ###########################################

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Warsaw'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# ###########################################
# #+---------------------------------------+#
# #|             Static files              |#
# #+---------------------------------------+#
# ###########################################

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static/core'),
)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# ###########################################
# #+---------------------------------------+#
# #|               Messages                |#
# #+---------------------------------------+#
# ###########################################

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'


# ###########################################
# #+---------------------------------------+#
# #|                 Email                 |#
# #+---------------------------------------+#
# ###########################################

_CONFIG_SMTP = CONFIG_ROOT.get('smtp')

EMAIL_HOST = _CONFIG_SMTP.get('host')
EMAIL_PORT = _CONFIG_SMTP.get('port')


# ###########################################
# #+---------------------------------------+#
# #|          Python Social Auth           |#
# #+---------------------------------------+#
# ###########################################

_CONFIG_GRAPH = CONFIG_ROOT.get('graph_api')

SOCIAL_AUTH_USER_MODEL = 'user.UserProfile'
SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'email']
SOCIAL_AUTH_FACEBOOK_KEY = _CONFIG_GRAPH.get('appid')
SOCIAL_AUTH_FACEBOOK_SECRET = _CONFIG_GRAPH.get('appsecret')
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'locale': 'en_US',
    'fields': 'id, email, age_range, first_name, last_name',
}
SOCIAL_AUTH_FACEBOOK_USERNAME_IS_FULL_EMAIL = True
SOCIAL_AUTH_FACEBOOK_UUID_LENGTH = 16
SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',

    'user.pipelines.get_username',

    'social.pipeline.social_auth.associate_by_email',

    'user.pipelines.create_user',

    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',

    'user.pipelines.save_avatar',
    'core.pipelines.debug',
)
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/dashboard/'
SOCIAL_AUTH_LOGIN_ERROR_URL = '/user/login/error/'
SOCIAL_AUTH_LOGIN_URL = '/user/login/'
SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL = '/user/settings/'
SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = '/user/settings/'
SOCIAL_AUTH_INACTIVE_USER_URL = '/user/login/inactive/'


# ###########################################
# #+---------------------------------------+#
# #|          Python Social Auth           |#
# #+---------------------------------------+#
# ###########################################

CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'
