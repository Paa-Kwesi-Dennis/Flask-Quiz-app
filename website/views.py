from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import current_user, login_required, logout_user
from .import db
import json
from .models import User, Question



views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    users = User.query.filter_by(email=current_user.email).all()
    if current_user not in users:
        flash('You are not an admin')
        logout_user()
        return redirect(url_for('auth.login'))
    questions = Question.query.all()
    return render_template('home.html', user=current_user, questions=questions)


