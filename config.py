# -*- coding: utf-8 -*-

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flask@minitech.site>'
    FLASKY_ADMIN = os.environ.get('FLASK_ADMIN')

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.minitech.site'
    MAIL_PORT = 465
    #MAIL_USE_TLS = True
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('FLASKY_MAIL_USERNAME')#sender
    MAIL_PASSWORD = os.environ.get('FLASKY_MAIL_PASSWD')#sender
    SQLALCHEMY_DATABASE_URI = os.environ.get('FLASKY_SQLALCHEMY_DATABASE_URI')

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('FLASKY_SQLALCHEMY_DATABASE_URI')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('FLASKY_SQLALCHEMY_DATABASE_URI')
    
config = {
    'development':DevelopmentConfig,
    'testing':TestConfig,
    'production':ProductionConfig,
    'default':DevelopmentConfig
    }
