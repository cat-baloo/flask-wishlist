from flask import render_template, redirect, url_for, request, flash, abort
from app import app, db
from models import Task
from datetime import datetime, timezone
import forms
#from itsdangerous import BadSignature, SignatureExpired

#@app.before_request
#def verify_csrf():
#  if request.method in ("POST", "PUT", "PATCH", "DELETE"):
#    token = request.form.get("csrf_token") or request.headers.get("X-CSRFToken")
    
#    if not token:
#      abort(400)
#    try:
#      csrf_serialiser.loads(token, max_age=3600)
#    except (BadSignature, SignatureExpired):
#       abort(400)

@app.route('/')
@app.route('/index')

def index():
  tasks = Task.query.all()
  return render_template('index.html', tasks=tasks, current_title='Your Christmas List')

@app.route('/tasks/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
   task = Task.query.get_or_404(task_id)
   db.session.delete(task)
   db.session.commit()
   flash(f'Deleted: {task.id}, {task.title}','success')
   return redirect(url_for('index'))

@app.route('/tasks/<int:task_id>/edit', methods=['POST'])
def edit_task(task_id):
   task = Task.query.get_or_404(task_id)
   new_title = request.form.get("title", "").strip()

   if not new_title:
      flash("Wish cannot be empty","error")

   task.title = new_title
   db.session.commit()
   return redirect(url_for("index"))

@app.route('/add', methods=['GET','POST'])
def add():
    
    form = forms.AddTaskForm()

    if form.validate_on_submit():
       t = Task(title=form.title.data, date=datetime.now(timezone.utc))
       db.session.add(t)
       db.session.commit()
       
       print('Submitted wish', form.title.data)
       return redirect(url_for('index'))
       return render_template ('about.html', form=form, title=form.title.data)
    return render_template('about.html', current_title='Secret page', form=form) 
