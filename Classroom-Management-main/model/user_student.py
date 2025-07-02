from model.user import User
import json
from lib.helper import course_data_path
from lib.helper import user_data_path
from lib.helper import course_json_files_path
class Student(User):
    def __init__(self,id=-1, username="", password="", register_time="yyyy-MM-dd_HH:mm:ss.SSS",role="",email=""):
        super().__init__(id, username, password, register_time, role)
        self.emai=email
        pass

    def get_student_by_id(self,id):
        with open(user_data_path, "r", encoding="utf8") as fi:
            f = fi.readlines()
            for h in f:
                inst = h.strip().split(";;;")
                if (inst[0] == id):
                    a = Student(int(inst[0]), inst[1], inst[2], inst[3], inst[4], inst[5])
                    return a.toJSON()


    def delete_student_by_id(self,iduser):
        with open(user_data_path, "r") as infile:
            lines = infile.readlines()

        with open(user_data_path, "w") as outfile:
            for line in lines:
                inst = line.strip().split(";;;")
                if (inst[0] != iduser):
                    outfile.write(line)
        pass
    def getliststudent(self):
        List = []

        with open(user_data_path, "r", encoding="utf8") as fi:
            filelinesins = fi.readlines()
            for obj in filelinesins:
                inst = obj.strip().split(";;;")
                if (inst[4] == "student"):
                    a = Student(inst[0], inst[1], inst[2], inst[3], inst[4], inst[5])
                    List.append(a.toJSON())
        return List

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)