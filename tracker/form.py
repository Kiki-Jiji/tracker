
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)



from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('form', __name__, url_prefix='/')

@bp.route("/")
def index():
    if not current_user.is_authenticated:
        return render_template("signin.html")

    return render_template("index.html")

@bp.route("/form")
def form():
    return render_template('form.html')

@bp.route("/user")
def user():
    return render_template('user.html')