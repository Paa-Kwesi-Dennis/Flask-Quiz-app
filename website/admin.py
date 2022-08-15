from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .models import Admin,Question
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user , login_required
from . import db
import json


admin = Blueprint('admin', __name__)


@admin.route('/admin', methods=['GET', 'POST'])
@login_required
def home():
    admins = Admin.query.filter_by(email=current_user.email).all()
    if current_user not in admins:
        flash('You are not an admin')
        logout_user()
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        question = request.form.get('question')
        option = request.form.get('options')

        
        if len(question) < 1:
            flash('Question can not be empty or null!', category='error')
        elif option == None:
            flash('Please choose an option!', category='error')
        else:
            new_question = Question(text=question, answer=option, author=current_user.id)
            db.session.add(new_question)
            db.session.commit()
            flash('Question added successfully!', category='success')
    return render_template('admin.html', user=current_user)


@admin.route('/delete-note', methods=['POST'])
def delete_note():
    question = json.loads(request.data)
    questionId = question['questionId']
    question = Question.query.get(questionId)
    if question:
        if question.author == current_user.id:
            db.session.delete(question)
            db.session.commit()

    return jsonify({})
