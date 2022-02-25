from flask import Blueprint, render_template, request, flash, jsonify
# A blueprint of the app which contains routes, allows for views to be separately organized
from flask_login import login_required, current_user
# current user allows access to all their information inside the user model
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

# Create route with name of blueprint
@views.route('/', methods=['GET', 'POST'])
@login_required # user cannot access homepage unless logged in
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 2:
            flash('Your note is too small', category='error')

        else:
            new_note = Note(data=note,  user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Your note has been created', category='success')

    return render_template("home.html", user=current_user)
    # current user can be referenced in home template to check if authenticated

@views.route('/delete-note', methods=['POST'])
def delete():
    note = json.loads(request.data) # receives data as string
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})




