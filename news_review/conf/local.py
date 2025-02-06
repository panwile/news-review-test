from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'news_review',
        'USER': 'root',
        'PASSWORD': 'DMOymmQKImbY',
        'HOST': 'my-db.zeejZbhGepUszXzTpRgEhQEuKAMwNNq.amazonaws.com',
        'OPTIONS': {'charset': 'utf8mb4'},
    },
}

SECRET_KEY = 'django-insecure-LBEVLufhzngkOtwNwmoSYqqYhvLgsCRBSsnybpheZRmxZpVItMVuLBgrSRnkzC'

EMAIL_HOST_USER = 'noreply@news-review.test'
EMAIL_HOST_PASSWORD = 'DMOymmQKImbY'
