from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

# Create route with name of blueprint
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            # checks if hashed password matches password from the form
            if check_password_hash(user.password, password):
                flash('You are logged in!', category='success')
                login_user(user, remember=True) # stores user in session
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password', category='error')
        else:
            flash('Email does not exist', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get("email")
        first_name = request.form.get("first_name")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')

        elif len(email) < 4:
            flash('Email needs to be more than 4 characters', category='error')
        elif len(first_name) < 3:
            flash('Name needs to be longer than 2 characters', category='error')
        elif len(password1) < 5:
            flash('Password needs to be longer than 4 characters', category='error')
        elif password1 != password2:
            flash('Passwords do not match', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)

            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    # current user determines what links are shown in the nav bar
    return render_template("sign_up.html", user=current_user)

@auth.route('/logout')
@login_required # cannot access this page unless user is logged in
def logout():
    logout_user()
    return redirect(url_for('auth.login')) # after user logs out, returns them to login page