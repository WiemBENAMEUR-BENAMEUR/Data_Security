
from flask import flash,render_template, Blueprint,request,redirect,url_for
import json
from model.user import User
from model.user_instructor import  Instructor
from model.course import Course
from model.user_admin import Admin
from datetime import datetime
from lib.helper import user_data_path
import ast
index_page = Blueprint("index_page", __name__)
model_user = User()

@index_page.route("/",methods=['POST','GET'])
def index():
    user = open(user_data_path, "r")
    user2=User()
    ins=Instructor()
    if(model_user.current_login_user==None):
        if request.method == "POST":
            # check whether employee exists in the database and whether
            # the password entered matches the password in the database
            for elm in user.readlines():
                fields = elm.split(";;;")
                print(fields)
                if (fields[1] == request.form["username"]) and (fields[2] == request.form["password"]):

                    if fields[4].strip() == "admin":
                        print("hh")
                        user2=user2.authenticate_user(request.form["username"], request.form["password"])

                        form_data = {'id': user2.id, 'username': user2.username, 'password': user2.password,'role': user2.role}
                        model_user.current_login_user = user2

                        return redirect(url_for("index_page.ff",user=form_data))

                    elif fields[4].strip() == "instructor":

                        print("instructor")
                        user2 = user2.authenticate_user(request.form["username"], request.form["password"])
                        form_data = {'id': user2.id, 'username': user2.username, 'password': user2.password,'role': user2.role}
                        model_user.current_login_user = user2
                        return redirect(url_for("index_page.index_istructor",user=form_data))
                    else:
                        print("chtakliii")
                        user2 = user2.authenticate_user(request.form["username"], request.form["password"])
                        form_data = {'id': user2.id, 'username': user2.username, 'password': user2.password,'role': user2.role}
                        model_user.current_login_user = user2
                        return redirect(url_for("index_page.index_student",user=form_data))
        return render_template("page-login.html")

    else :
        json_data = ast.literal_eval(json.dumps(model_user.current_login_user.toJSON()))
        parsed_json = eval(json_data)
        if(parsed_json["role"].strip()=="admin"):
            return redirect(url_for("index_page.ff"))
        elif(parsed_json["role"].strip()=="instructor"):
            return redirect(url_for("index_page.index_istructor"))
        else:
            return redirect(url_for("index_page.index_student"))





    # manually register an admin account when open index page

@index_page.route("/admin")
def ff():
    print(model_user.toJSON())
    user = request.args.get('user', None)
    if (model_user.current_login_user != None):
        json_data = ast.literal_eval(json.dumps(model_user.current_login_user.toJSON()))
        parsed_json = eval(json_data)
        print(parsed_json["role"])
        if(parsed_json["role"].strip()=="admin"):
             return render_template("app-profile.html",user=parsed_json)
        else:
            return  redirect(url_for("index_page.index"))

    else:
        return redirect(url_for("index_page.index"))
@index_page.route("/instructor")
def index_istructor():
    # print(model_user)
    user = request.args.get('user', None)
    if(model_user.current_login_user!=None):
        json_data = ast.literal_eval(json.dumps(model_user.current_login_user.toJSON()))
        parsed_json = eval(json_data)
        if (parsed_json["role"].strip() == "instructor"):
            return render_template("app-profile-instructor.html",user=parsed_json)
        else:
            return  redirect(url_for("index_page.index"))
    else:
        return  redirect(url_for("index_page.index"))

@index_page.route("/student")
def index_student():
    print(model_user.__str__())
    user = request.args.get('user', None)
    if (model_user.current_login_user != None):
        json_data = ast.literal_eval(json.dumps(model_user.current_login_user.toJSON()))
        parsed_json = eval(json_data)
        if(parsed_json["role"].strip() == "student"):
            return render_template("app-profile-student.html",user=parsed_json)
        else:
            return  redirect(url_for("index_page.index"))
    else:
        return redirect(url_for("index_page.index"))

@index_page.route("/signup",methods=['POST','GET'])
def index_signup():
    error=""
    if request.method == "POST":
        # admin = open(user_admin, "r")
        found = False
        admin = open(user_data_path, "r")
        for kz in admin.readlines():
            fds = kz.split(";;;")
            if fds[1] == request.form['username']:
                found = True

        if not found:
            with open(user_data_path, "a") as file:
                if(request.form['role']=="1"):
                    role="admin"
                elif(request.form['role']=="2"):
                    role="instructor"
                else:role="student"
                a=User()
                file.write(
                    str(a.generate_unique_user_id()) + ";;;" + request.form['username'] + ";;;" + request.form['password'] +";;;"+datetime.now().strftime("%m-%d-%Y_%H:%M:%S")+";;;"+role+";;;"+request.form['email']+ '\n')
            return redirect("/")
        else:
            error="user exists"
            flash('user already exists')
    return render_template("page-register.html",error=error)

@index_page.route("/logout")
def logout():
    # print(model_user)
    model_user.current_login_user=None
    return  redirect(url_for("index_page.index"))


