from flask import flash , Blueprint, render_template, request, redirect, url_for
from lib.helper import render_result, render_err_result, course_data_path, user_data_path
from model.course import Course
from model.user import User
from model.user_admin import Admin
from model.user_instructor import Instructor
from model.user_student import Student
import ast
from flask_paginate import Pagination
from lib.helper import course_data_path
from lib.helper import user_data_path
import sys
import os
import json
userfile="./data/_demo_user.txt"

user_page = Blueprint("user_page", __name__)

model_user = User()
model_course = Course()
model_student = Student()


def generate_user(login_user_str):
    login_user = None # a User object

    return login_user

@user_page.route('/resetdb')
def deletedb():
    fn = getattr(sys.modules['__main__'], '__file__')
    root_path = os.path.abspath(os.path.dirname(fn))
    print(root_path)
    with open(user_data_path, "w") as fp:
        fp.truncate()
    with open(course_data_path,"w") as fp:
        fp.truncate()
    a=Admin()
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
        print(json_data)
        parsed_json = eval(json_data)
        insts.append(parsed_json)
    insts1 = insts[offset - 10:offset]
    q = request.args.get('q')
    if q:
        search = True

    pagination = Pagination(page=page, total=len(insts), per_page=per_page, offset=offset, search=search,
                            record_name='insts')
    offset2 = (page - 1) * per_page

    return render_template("datadtudents.html", numins=numinst, insts=insts1, pagination=pagination)

@user_page.route("/course-delete/<id>")
def student_delete(id):
    a = Student()
    a.delete_student_by_id(id)
    return redirect(url_for("user_page.liststudent"))
# use @user_page.route("") for each page url



