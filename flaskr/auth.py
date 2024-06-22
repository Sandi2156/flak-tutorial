"""
What are views and blueprint in flask

: view function has the code that you write to response to a request
: you create blueprint by combining similar kind of views and register the blueprint with the app instead of every single views separately
"""

import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from flaskr.db import get_db

"""created a blueprint named auth. as the blueprint needs to know where it's defined so passing __name__. also all the url will be prepended with /auth which are 
associated with the blueprint"""
bp = Blueprint("auth", __name__, url_prefix="/auth")