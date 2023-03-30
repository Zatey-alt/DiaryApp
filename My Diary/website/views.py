from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user, login_user, logout_user
from .models import Note, User
from . import db

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html')

@views.route('/note', methods=['GET', 'POST'])
@login_required
def note():
    if request.method == 'POST':
        note_title = request.form.get('note_title')
        note_text = request.form.get('note_text')
        if note_title and note_text:
            new_note = Note(title=note_title, text=note_text, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            return redirect(url_for('views.note'))
    return render_template('note.html', user=current_user, notes=current_user.notes)



@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    note_id = request.form.get('note_id')
    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return redirect(url_for('views.note'))