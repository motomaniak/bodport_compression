# file_compressor/file_compressor/celery.py
# setup for celery messaging queue 
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'file_compressor.settings')

celery_app = Celery('file_compressor')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()
