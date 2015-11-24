# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from collections import defaultdict
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
from study.utils import generate_random_string


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


# ###########################################
# #+---------------------------------------+#
# #|        Application definition         |#
# #+---------------------------------------+#
# ###########################################

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': {
                'console',
            },
            'level': 'INFO',
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

LANGUAGE_CODE = 'pl-pl'
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
MEDIA_URL = '/media/'
