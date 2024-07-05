import os

base_dir = os.path.abspath(os.path.dirname(__file__))
default_url = 'sqlite:///' + os.path.join(base_dir, 'app.db')

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or default_url