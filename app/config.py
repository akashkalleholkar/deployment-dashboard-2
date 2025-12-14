import os

class Config:
    # SQLAlchemy DB URL from environment
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_POOL_PRE_PING = True

    # App port
    PORT = int(os.getenv("PORT", "90"))    
