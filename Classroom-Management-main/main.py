from flask import Flask
from controller.index_controller import index_page
from controller.course_controller import course_page
from controller.instructor_controller import instructor_page
from controller.user_controller import user_page
from sync_users import sync_users_from_db  # <-- Add this


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.register_blueprint(index_page, url_prefix="/")
app.register_blueprint(course_page, url_prefix="/course")
app.register_blueprint(instructor_page, url_prefix="/instructor")
app.register_blueprint(user_page, url_prefix="/user")

if __name__ == "__main__":
    sync_users_from_db()  # <-- Call the sync before app starts
    app.run(host="0.0.0.0", debug=True)