"""
What are views and blueprint in flask

: view function has the code that you write to response to a request
: you create blueprint by combining similar kind of views and register the blueprint with the app instead of every single views separately
"""

import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from flaskr.db import get_db

from werkzeug.security import check_password_hash, generate_password_hash

"""created a blueprint named auth. as the blueprint needs to know where it's defined so passing __name__. also all the url will be prepended with /auth which are 
associated with the blueprint"""
bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        db = get_db()
        error = None
        
        if not username:
            error = "Username is required"
        if not password:
            error = "Password is required"
            
        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))
        flash(error)
    
    return render_template("auth/register.html")
        