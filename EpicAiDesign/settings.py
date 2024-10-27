from pathlib import Path
from mongoengine import connect
import time
from django.contrib.messages import constants as message_constants

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-x1ol#f1$-!56j3o*g$kjck##rd2w294644vt)i_sym2o8f^7g%'

DEBUG = True

ALLOWED_HOSTS = []

# connect(db="aiDesign", host="mongodb+srv://nejdbedoui:6qModREgAzqUrtIw@aidesign.duaor.mongodb.net/aiDesign?retryWrites=true&w=majority")

retries = 0

def connect_with_retry(db, host, retries, max_retries=20, retry_delay=3):
    while retries < max_retries:
        try:
            connect(db=db, host=host)
            print("Connected to the database successfully!")
            return True
        except Exception as e:
            retries += 1
            print(f"Connection failed (attempt {retries}/{max_retries}). Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)

    print("Failed to connect after several attempts. Please check your connection or credentials.")
    return False


db_name = "aiDesign"
host_url = "mongodb+srv://nejdbedoui:6qModREgAzqUrtIw@aidesign.duaor.mongodb.net/aiDesign?retryWrites=true&w=majority"

connect_with_retry(db=db_name, host=host_url, retries=retries)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'UserApp',
    'SpeechApp',
    'ImageApp',
    'MusicApp',
    'PoemApp',
    'VideoApp',
    'embed_video',
    'AlbumApp',
    'GalleryApp'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'EpicAiDesign.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'EpicAiDesign.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'testmailsenderspringboot@gmail.com'
EMAIL_HOST_PASSWORD = 'zjakcqhzmybjuvfn'

MESSAGE_TAGS = {
    message_constants.DEBUG: 'debug',
    message_constants.INFO: 'info',
    message_constants.SUCCESS: 'success',
    message_constants.WARNING: 'warning',
    message_constants.ERROR: 'danger',
}


