from lib.helper import course_data_path
from lib.helper import user_data_path
from lib.helper import course_json_files_path
from model.user import User
from datetime import datetime
import json

class Admin(User):
    def __init__(self,id=-1, username="", password="", register_time="yyyy-MM-dd_HH:mm:ss.SSS",role=""):
        super().__init__(id, username, password, register_time, role)
        pass

    def register_admin(self):
        with open(user_data_path, "a+", encoding="utf8") as file:
            if (self.id == -1):
                file.writelines(
                    str(User.generate_unique_user_id(self)) + ";;;" + "admin" + ";;;" + "password" +";;;"+ datetime.now().strftime("%m-%d-%Y_%H:%M:%S")+";;;"+"admin"+ '\n')
                return True

            else:
                return False

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)