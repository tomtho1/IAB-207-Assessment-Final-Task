from flask import Blueprint, flash, render_template, request, url_for, redirect
#from .models import User
from .forms import LoginForm, RegisterForm
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from event.models import User
from . import db

# create a blueprint
bp = Blueprint('auth', __name__)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()

    if (register_form.validate_on_submit() == True):
        # get username, password and email from the form
        image = request.files[register_form.image.name].read()
        uname = register_form.user_name.data
        pwd = register_form.password.data
        email_id = register_form.email_id.data
        street_number = register_form.street_number.data
        street = register_form.street.data
        city = register_form.city.data
        state = register_form.state.data
        post_code = register_form.post_code.data

        # check if a user exists
        u1 = User.query.filter_by(name=uname).first()
        if u1:
            flash('User name already exists, please login.')
            return redirect(url_for('auth.login'))
        # don't store the password - create password hash
        pwd_hash = generate_password_hash(pwd)
        # create a new user model object
        new_user = User(image=image, name=uname, password_hash=pwd_hash, email=email_id,
                        street_number=street_number, street=street, city=city, state=state, post_code=post_code)
        db.session.add(new_user)
        db.session.commit()
        # commit to the database and redirect to HTML page
        return redirect(url_for('auth.login'))
    # the else is called when there is a get message
    else:
        return render_template('user.html', form=register_form, heading='Register')


# this is the hint for a login function
@bp.route('/login', methods=['GET', 'POST'])
def login():  # view function
    login_form = LoginForm()
    error = None
    if (login_form.validate_on_submit() == True):
        user_name = login_form.user_name.data
        password = login_form.password.data
        u1 = User.query.filter_by(name=user_name).first()
        if u1 is None:
            error = 'Incorrect username or password'
        # check password hash
        elif not check_password_hash(u1.password_hash, password):
            error = 'Incorrect username or password'
        if error is None:
            login_user(u1)
            # this gives the url from where the login page was accessed
            nextp = request.args.get('next')
            if nextp is None or not nextp.startswith('/'):
                return redirect(url_for('main.index'))
            return redirect(nextp)
        else:
            flash(error)
    return render_template('user.html', form=login_form, heading='Login')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    # this gives the url from where the login page was accessed
    nextp = request.args.get('next')
    if nextp is None or not nextp.startswith('/'):
        return redirect(url_for('main.index'))
    return redirect(nextp)
