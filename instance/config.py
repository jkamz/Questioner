"""
Environment and app configurations
"""

import os


class Config(object):
    """Parent configuration class"""
    DEBUG = False
    SECRET = os.getenv('SECRET')
    # DATABASE_URI = os.getenv('DATABASE_URL')
    POSTGRES_USER = "jkamz"
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_DB = "questioner"
    POSTGRES_HOST = "localhost"


class DevelopmentConfig(Config):
    """Configurations for development env"""
    DEBUG = True


class TestingConfig(Config):
    """Testing configurations with a different test db"""
    TESTING = True
    DEBUG = True
    POSTGRES_DB = "testdb"


class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False
    POSTGRES_USER = "epctuwdaikjkjj"
    POSTGRES_PASSWORD = "b20f4aaa747147ce35302b2d2b62baf50160704d9444f0afd4d7b8c39d394e6f"
    POSTGRES_DB = "d8vae2f9bj8fkb"
    POSTGRES_HOST = "ec2-54-235-67-106.compute-1.amazonaws.com"


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
