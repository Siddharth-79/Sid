from flask import Blueprint, render_template, request, flash, jsonify, redirect
from flask_login import login_required, current_user
from sqlalchemy.orm import query
from .models import Note
from . import db
import json
from .import static

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


# @views.route('/delete-note', methods=['GET', 'POST'])
# def delete_note():
#     note = json.loads(request.data)
#     noteId = note['noteId']
#     note = Note.query.get(noteId)
#     if note:
#         if note.user_id == current_user.id:
#             db.session.delete(note)
#             db.session.commit()

#     return jsonify({})


# @views.route('/delete-note', methods=['POST'])
# def delete_note():
#     note = json.loads(request.data)

@views.route("/delete/<int:id>")
def delete(id):
    task_to_delete = Note.query.get_or_404(id)


    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem'