"""
Environment and app configurations
"""

import os


class Config(object):
    """Parent configuration class"""
    DEBUG = False
    SECRET = os.getenv('SECRET')
    # DATABASE_URI = os.getenv('DATABASE_URL')
    POSTGRES_USER = "postgres"
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_DB = "questionerdb"
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


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
