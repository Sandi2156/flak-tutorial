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

@bp.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute("SELECT * from user WHERE id = ?", (user_id,)).fetchone()


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
        

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        db = get_db()
        error = None
        
        user = db.execute(
            "SELECT * from user WHERE username = ?", (username,)
        ).fetchone()
        
        if user is None:
            error = "User does not exist"
        elif not check_password_hash(user["password"], password):
            error = "Incorrect Password"
            
        if error is None:
            session.clear()
            session["user_id"] = user['id']
            return redirect(url_for("index"))
        
        flash(error)
    
    return render_template("auth/login.html")
        

@bp.route("/logout")     
def logout():
    session.clear()
    return redirect(url_for('index'))