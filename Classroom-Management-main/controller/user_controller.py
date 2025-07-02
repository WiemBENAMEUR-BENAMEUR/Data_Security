from flask import flash, Blueprint, render_template, request, redirect, url_for
from lib.helper import render_result, render_err_result, course_data_path, user_data_path
from model.course import Course
from model.user import User
from model.user_admin import Admin
from model.user_instructor import Instructor
from model.user_student import Student
from flask_paginate import Pagination
from datetime import datetime
import ast
import uuid
import sys
import os
import json

userfile = "./data/_demo_user.txt"

user_page = Blueprint("user_page", __name__)

model_user = User()
model_course = Course()
model_student = Student()


def generate_user(login_user_str):
    login_user = None  # a User object
    return login_user


@user_page.route('/resetdb')
def deletedb():
    fn = getattr(sys.modules['__main__'], '__file__')
    root_path = os.path.abspath(os.path.dirname(fn))
    print(root_path)
    with open(user_data_path, "w") as fp:
        fp.truncate()
    with open(course_data_path, "w") as fp:
        fp.truncate()
    a = Admin()
    a.register_admin()

    return redirect(url_for("index_page.ff"))


@user_page.route('/studentslist')
def liststudent():
    search = False

    page = int(request.args.get('page', 0))
    per_page = 10
    offset = (page + 1) * per_page

    insts = []
    a = Student()
    l = a.getliststudent()
    numinst = len(l)

    for b in l:
        json_data = ast.literal_eval(json.dumps(b))
        parsed_json = eval(json_data)
        insts.append(parsed_json)

    insts1 = insts[offset - 10:offset]
    q = request.args.get('q')
    if q:
        search = True

    pagination = Pagination(page=page, total=len(insts), per_page=per_page, offset=offset, search=search,
                            record_name='insts')

    return render_template("datadtudents.html", numins=numinst, insts=insts1, pagination=pagination)


@user_page.route("/course-delete/<id>")
def student_delete(id):
    a = Student()
    a.delete_student_by_id(id)
    return redirect(url_for("user_page.liststudent"))


@user_page.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')  # Not saved currently
        password = request.form.get('password')
        role = request.form.get('role')

        if not username or not password or not role:
            flash("⚠ Please fill in all required fields.", "error")
            return redirect(url_for('user_page.signup'))

        # Generate user data
        user_id = str(uuid.uuid4().int)[:8]
        register_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user_data = f"{user_id};;;{username};;;{password};;;{register_time};;;{role}\n"

        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(user_data_path), exist_ok=True)

            # Append user to file
            with open(user_data_path, "a", encoding="utf-8") as f:
                f.write(user_data)

            flash(f"✅ User '{username}' registered successfully!", "success")
            return redirect(url_for("user_page.signup"))  # You can change this to login page
        except Exception as e:
            flash(f"❌ Failed to register user: {e}", "error")
            return redirect(url_for('index_page.index_istructor'))

    # GET request
    return render_template("page-login.html")
