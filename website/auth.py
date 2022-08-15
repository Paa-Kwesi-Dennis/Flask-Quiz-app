from flask import Blueprint, render_template, request, flash, redirect, url_for,session
from .models import User, Admin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user , login_required
from . import db


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        session['account_type'] = request.form.get('account_type')


        user = User.query.filter_by(email=email).first()
        admin_user = Admin.query.filter_by(email=email).first()
        users = User.query.all()
        admins = Admin.query.all()



        if user:
            if session['account_type'] == 'user':
                if check_password_hash(user.password, password):
                    flash('Logged in successfully!', category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('views.home'))
                else:
                    flash('Incorrect password, try again.', category='error')
            else:
                flash("Email does not exist", category='error')

        if admin_user:
            if session['account_type'] == 'admin':
                if check_password_hash(admin_user.password, password):
                    flash('Logged in successfully as Admin!', category='success')
                    login_user(admin_user, remember=True)
                    return redirect(url_for('admin.home'))
                else:
                    flash('Incorrect password, try again.', category='error')
            else:
                flash('Email does not exist', category='error')


        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        session['account_type'] = request.form.get('account_type')

        user = User.query.filter_by(email=email).first()
        admin_user = Admin.query.filter_by(email=email).first()
        users = User.query.all()
        admins = Admin.query.all()

        if user or admin_user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            if session['account_type'] == 'user':
                new_user = User(email=email, password=generate_password_hash(password1, method='sha256'), first_name=first_name)
                db.session.add(new_user)
                db.session.commit()
                flash("Account Created", category='success')
                login_user(new_user, remember=True)
                return redirect(url_for('views.home'))
            elif session['account_type'] == 'admin':
                new_admin_user = Admin(email=email, password=generate_password_hash(password1, method='sha256'), first_name=first_name)
                db.session.add(new_admin_user)
                db.session.commit()
                flash("Admin Account Created", category='success')
                login_user(new_admin_user, remember=True)
                return redirect(url_for('admin.home'))
                

        
    return render_template('signup.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

