from flask import render_template, redirect, url_for, request, flash, abort, Blueprint, jsonify
from extensions import db
from models import Task
from datetime import datetime, timezone
import forms

bp = Blueprint("routes", __name__)

@bp.route("/health")
def health():
    return jsonify({"status": "ok"})

@bp.route("/tasks", methods=["GET"])
def list_tasks():
    tasks = Task.query.all()
    return jsonify([{"id": t.id, "title": t.title, "date": t.date.isoformat()} for t in tasks])


@bp.route("/", methods=["GET"])
@bp.route("/index", methods=["GET"])
def index():
    tasks = Task.query.all()
    return render_template("index.html", tasks=tasks, current_title="Your Christmas List")


@bp.route("/tasks/<int:task_id>/delete", methods=["POST"])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash(f"Deleted: {task.id}, {task.title}", "success")
    # Use blueprint endpoint name
    return redirect(url_for("routes.index"))



@bp.route("/tasks/<int:task_id>/edit", methods=["POST"])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    new_title = request.form.get("title", "").strip()

    if not new_title:
        flash("Wish cannot be empty", "error")
        return redirect(url_for("routes.index"))

    task.title = new_title
    db.session.commit()
    return redirect(url_for("routes.index"))



@bp.route("/add", methods=["GET", "POST"])
def add():
    form = forms.AddTaskForm()

    if form.validate_on_submit():
        # If models.Task.date is a Date column, store a date; else change the column to DateTime
        t = Task(title=form.title.data, date=datetime.now(timezone.utc).date())
        db.session.add(t)
        db.session.commit()

        flash(f"Added: {t.title}", "success")
        return redirect(url_for("routes.index"))

    # GET or validation errors
    return render_template("about.html", current_title="Secret page", form=form)
