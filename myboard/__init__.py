# myboard/__init__.py

from flask import Blueprint

myboard_bp = Blueprint(
    'myboard',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/myboard/static'
)

from . import views
