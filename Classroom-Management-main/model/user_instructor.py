import os
import re
from model.user import User
from flask import jsonify
import json
from lib.helper import course_data_path
from lib.helper import user_data_path
from lib.helper import course_json_files_path
class Instructor(User):
    def __init__(self,id=-1, username="", password="", register_time="yyyy-MM-dd_HH:mm:ss.SSS",role="",course_id_list=[]):
        super().__init__(id, username, password,register_time,role)
        self.course_id_List=course_id_list
        pass

    def __str__(self):
        pass

    def get_instructors(self):
        t = []

        for dirs in os.listdir(course_json_files_path):
            print(dirs)
            for dirssub in os.listdir(course_json_files_path +'/'+ dirs):
                print(dirssub)
                for file in os.listdir(course_json_files_path +'/'+ dirs + "/" + dirssub):
                    with open(course_json_files_path+'/'+ dirs + "/" + dirssub + "/" + file,
                              encoding="ISO-8859-1") as f:
                        fin = f.read()
                        a = re.findall('"course", "items":(.*?)"remaining_item_count"', fin)
                        t.append(a)
        a = 0
        f = []
        setofinsctructor = set([])
        for b in t:
            idcourse = re.findall('"_class": "course", "id": ([0-9]+)', str(b))
            courseinstructor = re.findall('"_class": "course" ,(.*?)image_125_H"', str(b))
            # print(courseinstructor)

            instructors = re.findall('"visible_instructors":(.*?)is_practice_test_course"', str(b))
            # print(instructors)
            a += len(idcourse)

            for i in range(len(idcourse)):
                # f.append(idcourse[i])
                idinstructor = re.findall('"id": ([0-9]+)', instructors[i])
                f.append((idinstructor, idcourse[i]))
                # for j in range(len(idinstructor)):
                #     dictr[idinstructor[j]] =idcourse[i]
                #     if()
                username = re.findall('"display_name": "(.*?)"', instructors[i])
                # print(username)
                jobtitle = re.findall('"job_title": "(.*?)"', instructors[i])
                # print(jobtitle)
                # print(len(h))

                if (len(jobtitle) <= 2):
                    for j in range(len(idinstructor)):
                        setofinsctructor.add(
                            idinstructor[j] + ";;;" + username[j] + ";;;" + idinstructor[
                                j] + ";;;" + "xxxx-xx-xx_xx:xx:xx.xxx" + ";;;" + "instructor")

        def findcoursesidbyinstructor(idinsctructor):
            t = ""
            for i in range(len(f)):
                for j in range(len(f[i][0])):
                    if (f[i][0][j] == idinsctructor):
                        t += f[i][1] + "-"
            return t

        for i in setofinsctructor:
            with open(user_data_path, "a+", encoding="utf8") as fileinstructor:
                idinstructor1 = re.search('([0-9]+);;;', i).group(1)
                fileinstructor.writelines(i + ";;;" + findcoursesidbyinstructor(idinstructor1) + "\n")
            pass

    def getlistinstructors(self):
        List =[]

        with open(user_data_path, "r", encoding="utf8") as fi:
            filelinesins = fi.readlines()
            for obj in filelinesins:
                inst=obj.strip().split(";;;")
                if(inst[4]=="instructor"):
                    a = Instructor(inst[0],inst[1],inst[2],inst[3],inst[4],inst[5])
                    List.append(a.toJSON())



        return List
        pass


    def get_instructor_by_id(self, id):
        with open(user_data_path, "r", encoding="utf8") as fi:
            f=fi.readlines()
            for h in f:
                inst=h.strip().split(";;;")
                if(inst[0]==id):
                    a=Instructor(int(inst[0]), inst[1], inst[2],inst[3],inst[4],inst[5].split("-"))
                    return a.toJSON()
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)