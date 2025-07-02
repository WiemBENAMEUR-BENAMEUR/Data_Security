# Classroom-Management
This project is a data analysis website. It analyses the given data in folder data/source_course_files.
The user can be : Admin, Instructor, or Student, each user has access to different analysis. 


## Requirement : 
This project is based on Python Flask Framework, check requirements.txt

## Project overview : 
#### Login page :
Login page allows the user to login into the web application which requires them to input username and password. There are three different kinds of users, i.e., Admin, Instructor, and student. Each kind of user will see different contents from the home (index) pages after login.
* Instructors can only see the courses they teach and logout.
* Students can only check their own information and logout.
#### Register page : 
Register page allows users to register them into the web application, in the case they do not have an account. It is required to enter username, password, email address and role when registering a user. And a register timestamp(unix epoch time) will be generated automatically. All these five values will be sent to the application’s backend to store the values in the user.txt file.
#### Courses page : 
In this page, the total number of courses will be displayed. All the course objects can be returned based on the page number. By default, the page number is 1. Each page has a maximum of 20 courses. At the bottom of the webpage, a page number list is shown. By default, the page number list is always be [1,2,3,4,5,6,7,8,9]
#### Instructors page : 
In this page, the total number of instructors will be displayed. Each instructor can teach more than one course. All the instructor objects can be returned based on the page number. By default, the page number is 1. Each page has a maximum of 20 instructors. For each instructor, we can see all the courses this instructor teaches by clicking the Teach Courses button.
#### Students page: 
In this page, the total number of students and a list of students will be displayed. Students’ info are not extracted from the files but registered manually in the register page. Admin can click the details button to see students’ details and click the delete button to remove this student
