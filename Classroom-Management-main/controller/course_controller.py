from flask import Blueprint, render_template, request, redirect, url_for
from lib.helper import render_result, render_err_result, course_data_path, user_data_path
from model.user import User
from model.course import Course
from model.user_instructor import Instructor
import ast
import pandas as pd
import json
from flask import render_template, Blueprint
from flask_paginate import Pagination, get_page_parameter
from controller.index_controller import model_user
course_page = Blueprint("course_page", __name__)

model_course = Course()
model_instructor = Instructor()
model_user = User()




def reset_database():
    pass


@course_page.route("/listcourse")
def course_list():
   if(model_user!=None):
       search = False

       page = int(request.args.get('page', 0))
       per_page = 20
       offset = (page + 1) * per_page

       insts = []
       a= Course()
       l = a.getlistcourse()
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
                               record_name='courses')


       return render_template("datacourses.html",insts=insts1, num=len(insts),pagination=pagination)


@course_page.route("/process-course",methods=['POST','GET'])
def process_course():
    if request.method == "POST":
        b = Course()
        b.get_courses()

        return redirect(url_for("course_page.course_list"))


@course_page.route("/course-details/<id>")
def course_details(id):
    if(model_user!=None):
        b=Course()
        # b.get_courses()
        obj=b.get_course_by_course_id(id)
        print(obj)
        # print(obj["course_avg_rating"])
        json_data = ast.literal_eval(json.dumps(obj))
        parsed_json = eval(json_data)
        print(parsed_json)

        return render_template("coursedetailbyid.html", obj=parsed_json)


@course_page.route("/course-delete/<id>")
def course_delete(id):
    a = Course()
    a.delete_course_by_id(id)
    return redirect(url_for("course_page.course_list"))


@course_page.route("/course-analysis")
def course_analysis():
    context = {}
    if User.current_login_user:
        explain1 = model_course.generate_course_figure1()
        explain2 = model_course.generate_course_figure2()
        explain3 = model_course.generate_course_figure3()
        explain4 = model_course.generate_course_figure4()
        explain5 = model_course.generate_course_figure5()
        explain6 = model_course.generate_course_figure6()


        context['explain1'] = explain1
        context['explain2'] = explain2
        context['explain3'] = explain3
        context['explain4'] = explain4
        context['explain5'] = explain5
        context['explain6'] = explain6
        context['current_user_role'] = User.current_login_user.role
    else:
        return redirect(url_for("course_page.course_list"))


    return render_template("04course_analysis.html", **context)