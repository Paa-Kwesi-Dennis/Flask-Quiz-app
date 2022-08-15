from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Admin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user , login_required
from . import db


admin = Blueprint('admin', __name__)


@admin.route('/admin', methods=['GET', 'POST'])
@login_required
def home():
    admins = Admin.query.filter_by(email=current_user.email).all()
    if current_user not in admins:
        flash('You are not an admin')
        logout_user()
        return redirect(url_for('auth.login'))
    return render_template('admin.html', user=current_user)


