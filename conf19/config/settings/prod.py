from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_secret('PROD_DATABASE_NAME'),
        'USER': get_secret('PROD_DATABASE_USER'),
        'PASSWORD': get_secret('PROD_DATABASE_PASSWORD'),
        'HOST': get_secret('PROD_DATABASE_HOST'),
        'PORT': get_secret('PROD_DATABASE_PORT')
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.01/howto/static-files/

STATIC_ROOT = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), 'conf19_static/')
STATIC_URL = 'https://confirmation.jmorris.webfactional.com/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static', 'site'), )

ALLOWED_HOSTS.append('confirmation.jmorris.webfactional.com')

ADMINS = (
    ('FrJim', 'jmorris@ecybermind.net'), ('FrJim', 'frjamesmorris@gmail.com')
)

