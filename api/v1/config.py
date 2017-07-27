import os
from datetime import timedelta

# Use a Class-based config to avoid needing a 2nd file
# os.getenv() enables configuration through OS environment variables
class ConfigClass(object):
    # Flask settings
    SECRET_KEY =               os.getenv('SECRET_KEY',       'awe345frgty5633cfr0nj3m4k4j67')
    SQLALCHEMY_DATABASE_URI =  os.getenv('DATABASE_URL',     'mysql://root:root@localhost/monitdb2')
    WTF_CSRF_ENABLED =         False
    CSRF_ENABLED =             False
    JWT_EXPIRATION_DELTA =     timedelta(seconds=2592000)
    # Mail settings
    EMAIL_USERNAME =           os.getenv('EMAIL_USERNAME',        'email@example.com')
    EMAIL_PASSWORD =           os.getenv('EMAIL_PASSWORD',        'password')
    EMAIL_DEFAULT =            os.getenv('EMAIL_DEFAULT',  '"Test App" <noreply@example.com>')
    EMAIL_SERVER =             os.getenv('EMAIL_SERVER',          'smtp.gmail.com')
    EMAIL_PORT =               int(os.getenv('EMAIL_PORT',            '465'))
    EMAIL_USE_SSL =            int(os.getenv('EMAIL_USE_SSL',         True))
    APPLICATION_ROOT =         os.getenv('APPLICATION_ROOT',       '/api/v1')
