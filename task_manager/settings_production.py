"""
Production settings for AWS deployment
"""
from .settings import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Allow your AWS domain
ALLOWED_HOSTS = [
    os.environ.get('AWS_DOMAIN', ''),
    os.environ.get('AWS_ALB_DNS', ''),
    '.elasticbeanstalk.com',
    '.amazonaws.com',
    'localhost',
    '3.237.38.122',
    '127.0.0.1'
]

# Add your domain if using custom domain
if os.environ.get('CUSTOM_DOMAIN'):
    ALLOWED_HOSTS.append(os.environ.get('CUSTOM_DOMAIN'))

# Security settings
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

 #Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Use environment variable for SECRET_KEY
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', SECRET_KEY)

# Database - Use AWS RDS
if os.environ.get('RDS_DB_NAME'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('RDS_DB_NAME'),
            'USER': os.environ.get('RDS_USERNAME'),
            'PASSWORD': os.environ.get('RDS_PASSWORD'),
            'HOST': os.environ.get('RDS_HOSTNAME'),
            'PORT': os.environ.get('RDS_PORT', '5432'),
            'OPTIONS': {
                'connect_timeout': 10,
            }
        }
    }
else:
    # Fallback to default database if RDS not configured
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Static files (CSS, JavaScript, Images)
# Use AWS S3 for static and media files
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', '')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'us-east-1')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

if AWS_STORAGE_BUCKET_NAME:
    # S3 Static settings
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
    
    # S3 Media settings
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
else:
    # Fallback to local storage
    STATIC_URL = '/static/'
    STATIC_ROOT = BASE_DIR / 'staticfiles'
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'

# Email configuration (AWS SES)
if os.environ.get('AWS_SES_REGION'):
    EMAIL_BACKEND = 'django_ses.SESBackend'
    AWS_SES_REGION_NAME = os.environ.get('AWS_SES_REGION')
    AWS_SES_REGION_ENDPOINT = f'email.{AWS_SES_REGION_NAME}.amazonaws.com'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/error.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Cache configuration (AWS ElastiCache)
if os.environ.get('ELASTICACHE_ENDPOINT'):
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': f"redis://{os.environ.get('ELASTICACHE_ENDPOINT')}:6379/1",
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            }
        }
    }

