import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

    SQLALCHEMY_DATABASE_URI = 'sqlite:///placement_portal.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)

    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    REDIS_DB = int(os.getenv('REDIS_DB', 0))
    CACHE_EXPIRY = 300

    CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/1'
    CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}/2'

    UPLOAD_FOLDER = 'uploads/resumes'
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024

    ADMIN_EMAIL = 'admin@placement.edu'
    ADMIN_PASSWORD = 'admin123'
