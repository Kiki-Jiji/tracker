
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

from tracker.db import add_weight

bp = Blueprint('form', __name__, url_prefix='/')

@bp.route("/")
def index():
    if not current_user.is_authenticated:
        return render_template("signin.html")
    return render_template("index.html")

@bp.route("/form", methods=['GET','POST'])
def form():

    if request.method == 'POST':
        weight = request.form['number']
        date = request.form['date']
        user_id = current_user.id
        error = None

        if not weight:
            error = 'Weight is required.'
        if not date:
            error = 'Date is required'
        if error is not None:
            flash(error)

        add_weight(weight = weight, date= date, user_id=user_id)
        flash("Weight added successfully")

        
    return render_template('form.html')

@bp.route("/user")
def user():
    return render_template('user.html')