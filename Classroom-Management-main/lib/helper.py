"""
helper file: saves some constant values and util functions
Xinyu Li
30/3/2022
"""
from flask import jsonify
from datetime import datetime
import sys
import os
fn = getattr(sys.modules['__main__'], '__file__')
root_path = os.path.abspath(os.path.dirname(fn))
course_data_path = root_path+"/data/course.txt"
user_data_path = root_path+"/data/user.txt"

course_json_files_path = root_path+"/data/source_course_files"
figure_save_path = "static/img/"


def render_result(code=200, msg="success"):
    resp = {"code": code, "msg": msg}
    return jsonify(resp)


def render_err_result(code=-1, msg="system busy"):
    resp = {"code": code, "msg": msg}
    return jsonify(resp)


def get_day_from_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp).day





