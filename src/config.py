import os
from dotenv import load_dotenv
load_dotenv()
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///instance/fiber_forum.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-string')
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'instance/uploads')
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024  # 8 MB
