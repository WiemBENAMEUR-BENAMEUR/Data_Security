from flask import Blueprint, render_template, request, redirect, url_for,jsonify
from lib.helper import render_result, render_err_result, course_data_path, user_data_path
from model.user import User
from flask_sqlalchemy import SQLAlchemy
from model.course import Course
import json
from flask_paginate import Pagination, get_page_parameter
from controller.index_controller import model_user
import ast
import pandas as pd
from flask import render_template, Blueprint

from model.user_instructor import Instructor

instructor_page = Blueprint("instructor_page", __name__)

model_instructor = Instructor()
model_course = Course()
ROWS_PER_PAGE = 20

@instructor_page.route("/inslist")
def instructor_list():
    # print(model_user.current_login_user.toJSON())
    #
    #
    # json_data = ast.literal_eval(json.dumps(model_user.current_login_user.toJSON()))
    # parsed_json = eval(json_data)
    #
    search = False

    page = int(request.args.get('page', 0))
    per_page = 10
    offset = (page + 1) * per_page

    insts=[]
    a=Instructor()
    l=a.getlistinstructors()
    numinst=len(l)

    for b in l:
        json_data = ast.literal_eval(json.dumps(b))
        parsed_json = eval(json_data)
        insts.append(parsed_json)
    insts1 = insts[offset-10:offset]
    q = request.args.get('q')
    if q:
        search = True

    pagination = Pagination(page=page, total=len(insts),per_page=per_page,offset=offset,search=search, record_name='insts')
    offset2 = (page - 1) * per_page


    return render_template("datainstructor.html", numins=numinst,insts=insts1,pagination=pagination)




@instructor_page.route("/ins-details/<id>")
def instructor_details(id):
    if (model_user.current_login_user!= None):
        b=Instructor()
        obj=b.get_instructor_by_id(id)
        print(obj)
        json_data = ast.literal_eval(json.dumps(obj))
        parsed_json = eval(json_data)

        return render_template("instructorbyid.html", obj=parsed_json)

@instructor_page.route("/courses/<id>")
def teach_courses(id):
    # print(model_user.__str__())

    search = False

    page = int(request.args.get('page', 0))
    per_page = 20
    offset = (page + 1) * per_page
    l=[]
    b=Instructor()
    obj=b.get_instructor_by_id(id)
    json_data = ast.literal_eval(json.dumps(obj))
    parsed_json = eval(json_data)
    print(parsed_json)
    print(parsed_json['course_id_List'])
    for i in parsed_json['course_id_List']:
        a=Course()
        b=a.get_course_by_course_id(i)

        if(b != None):
            print(b)
            json_data = ast.literal_eval(json.dumps(b))
            parsed_json = eval(json_data)
            l.append(parsed_json)
    if(offset-20 <=len(l) ):
        list = l[offset - 20:offset]
    else:
        offset=len(l)-offset
        list=l[offset:len(l)]

    q = request.args.get('q')
    if q:
        search = True


    pagination = Pagination(page=page, total=len(l),offset=offset, per_page=per_page, search=search,
                            record_name='l')

    return render_template("instructorteachingcourses.html",list=list,pagination=pagination,numins=len(l))



@instructor_page.route("/instructor-analysis")
def instructor_analysis():
    # if Instructor.instructor_data.shape[0] == 0:
    #     return render_err_result(msg="no instructor in datafile")

    explain1 = model_instructor.generate_instructor_figure1()

    context = {}
    context['explain1'] = explain1

    return render_template("08instructor_analysis.html", **context)


@instructor_page.route("/process-instructor", methods=["POST"])
def process_instructor():
    if request.method == "POST":
        b = Instructor()
        b.get_instructors()


        return redirect(url_for("instructor_page.instructor_list"))