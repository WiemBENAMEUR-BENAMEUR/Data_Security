import re
from random import randint
import json
from lib.helper import course_data_path
from lib.helper import user_data_path
from lib.helper import course_json_files_path
userfile="/Data_Security_Project/Classroom-Management-main/data/user.txt"
class User:
    current_login_user = None

    def __init__(self, id=-1, username="", password="",register_time="yyyy-MM-dd_HH:mm:ss.SSS",role="",):
        self.id = id
        self.username = username
        self.password = password
        self.register_time=register_time
        self.role=role
    def __str__(self):
        pass

    def validate_username(self, username):
        pattern = "^[A-Za-z0-9_-]*$"
        if(re.match(pattern,username)):
            return True
        else:
            return False
        pass

    def validate_password(self, password):
        if(len(password>=8)):
            return True
        else :
            return False
        pass

    def validate_email(self, email):

        pattern="^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$"
        if(re.match(pattern,email)):
            return True
        else:
            return False
        pass

    def clear_user_data(self):
        pass

    def authenticate_user(self, username,password):
        user = open(user_data_path, "r", encoding="utf8")
        for elm in user.readlines():
            fields = elm.split(";;;")
            if (fields[1] == username):
                if (fields[2].replace("\n", "") == self.encrypt_password(password)):
                    return User(int(fields[0]),fields[1],fields[2],fields[3],fields[4])
                else:
                    return User()

        pass

    def check_username_exist(self, username):
        user = open(user_data_path, "r", encoding="utf8")
        for elm in user.readlines():
            fields = elm.split(";;;")
            if (fields[1] == username):
                    return True
            else:
                    return False
        pass



    def generate_unique_user_id(self):
        range_start = 10 ** (10 - 1)
        range_end = (10 ** 10) - 1
        randedid = randint(range_start, range_end)

        admin = open(user_data_path, "r", encoding="utf8")


        for elm in admin.readlines() :
            fields = elm.split(";;;")
            if (fields[0] == str(randedid)):
                # print("foundranded id")
                randedid = randint(range_start, range_end)
                # print("changed value to "+ str(randedid))

        return randedid
        pass

    def encrypt_password(self, password):
        return password
        pass

    def register_user(self, username, password, email, register_time, role):
        with open(user_data_path, "a+", encoding="utf8") as file:
            if (self.id == -1):
                file.writelines(
                    str(User.generate_unique_user_id(self)) + ";;;" + username + ";;;" + User.encrypt_password(self,password) +";;;"+ email+";;;"+register_time+";;;"+role+ '\n')
                return True

            else:
                return False

    def date_conversion(self, register_time):
        pass

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
