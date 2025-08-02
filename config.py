# config.py
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret')
    SQLALCHEMY_DATABASE_URI = (
        os.getenv('DATABASE_URL') or
        'sqlite:///' + os.path.join(basedir, 'app.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # (if you’re using CKEditor / uploads, re-add those settings here)
    CKEDITOR_PKG_TYPE     = 'full'
    CKEDITOR_FILE_UPLOADER = 'upload'
    UPLOADED_FILES_DEST   = os.path.join(basedir, 'static', 'uploads')
    UPLOADED_FILES_URL    = '/static/uploads/'
