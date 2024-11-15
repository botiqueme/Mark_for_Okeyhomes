import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fallback-secret-key'
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT')

    DEBUG = True

    def __init__(self):
        if self.SECRET_KEY == 'fallback-secret-key':
            raise ValueError("No SECRET_KEY set for Flask application")
