import os

class Config:
    """Base configuration."""
    SECRET_KEY = os.getenv('STRIPE_SECRET_KEY_TEST')
    PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY_TEST')
    DEBUG = False

    # --- Shared Constants ---


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration."""
    pass  #  Or add production-only settings here

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


