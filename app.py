from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///uni.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'this is secret'

db = SQLAlchemy(app)


#User Tables


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))



#Database Tables
class StudentDB(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(200), nullable=False)
    student_courses = db.Column(db.String(100), nullable=False)

class TeacherDB(db.Model):
    teacher_id = db.Column(db.Integer, primary_key=True)
    teacher_name = db.Column(db.String(200), nullable=False)
    teacher_courses = db.Column(db.String(100), nullable=False)

class CourseDB(db.Model):
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(200), nullable=False)

class DepartmentDB(db.Model):
    department_id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(200), nullable=False)
    
#-----------------------------------------------------------------------------------------------------------

@app.route("/", methods = ['GET', 'POST'])
# @login_required
def visit():
    return redirect("/login")


def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/login", methods=['GET', 'POST'])
def login():
    users = User.query.all()
    if request.method == "POST":
        username_log = request.form['username']
        password_log = request.form['password']


        for user in users:
            if username_log == user.username and password_log == user.password:
                # login_user(user)
                # return redirect(url_for('welcome'))
                return render_template("index.html", username=username_log)

        else:
            return render_template("login.html")
    else:
        return render_template("login.html")


# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return "You are now logged out"

@app.route("/welcome")
def welcome():
    return render_template("index.html")

@app.route("/teachers", methods = ['GET', 'POST'])
# @login_required
def teacher():
    if request.method == "POST":
        new_name = request.form['new_name']
        new_courses = request.form['new_courses']
        new_teacher = TeacherDB(teacher_name=new_name, teacher_courses=new_courses)

        try:
            db.session.add(new_teacher)
            db.session.commit()
            return redirect('/teachers')

        except:
            return "There was an issue adding this teacher"

    else:
        lecturers = TeacherDB.query.all()
        return render_template("teachers.html", lecturers = lecturers)
    
@app.route("/teachers/delete/<int:teacher_id>")
# @login_required
def tdelete(teacher_id):
    teacher_to_delete = TeacherDB.query.get_or_404(teacher_id)

    try:
        db.session.delete(teacher_to_delete)
        db.session.commit()
        return redirect('/teachers')

    except:
        return "There was a problem deleting that Teacher"

@app.route("/teachers/update/<int:teacher_id>", methods=['GET','POST'])
# @login_required
def tupdate(teacher_id):
    lecturer = TeacherDB.query.get_or_404(teacher_id)

    if request.method == 'POST':
        lecturer.teacher_name = request.form['new_name']
        lecturer.teacher_courses = request.form['new_courses']

        try:
            db.session.commit()
            return redirect('/teachers')

        except:
            return 'There was an issue updating this teacher'

    else:
        return render_template("teacherupdate.html", lecturer = lecturer)

#------------------------------------------------------------------------------------------------------

@app.route("/students", methods = ['GET', 'POST'])
# @login_required
def student():
    if request.method == "POST":
        new_name = request.form['new_name']
        new_courses = request.form['new_courses']
        new_student = StudentDB(student_name=new_name, student_courses=new_courses)

        try:
            db.session.add(new_student)
            db.session.commit()
            return redirect('/students')

        except:
            return "There was an issue adding this student"

    else:
        pupils = StudentDB.query.all()
        return render_template("students.html", pupils = pupils)
    
@app.route("/students/delete/<int:student_id>")
# @login_required
def sdelete(student_id):
    student_to_delete = StudentDB.query.get_or_404(student_id)

    try:
        db.session.delete(student_to_delete)
        db.session.commit()
        return redirect('/students')

    except:
        return "There was a problem deleting that student"

@app.route("/students/update/<int:student_id>", methods=['GET','POST'])
# @login_required
def supdate(student_id):
    pupil = StudentDB.query.get_or_404(student_id)

    if request.method == 'POST':
        pupil.student_name = request.form['new_name']
        pupil.student_courses = request.form['new_courses']

        try:
            db.session.commit()
            return redirect('/students')

        except:
            return 'There was an issue updating this student'

    else:
        return render_template("studentupdate.html", pupil = pupil)
#------------------------------------------------------------------------------------------------------------
@app.route("/departments", methods = ['GET', 'POST'])
# @login_required
def department():
    if request.method == "POST":
        new_department = request.form['new_department_name']
        new_dentry = DepartmentDB(department_name=new_department)

        try:
            db.session.add(new_dentry)
            db.session.commit()
            return redirect('/departments')

        except:
            return "There was an issue adding this department"

    else:
        sections = DepartmentDB.query.all()
        return render_template("departments.html", sections = sections)
    
@app.route("/departments/delete/<int:department_id>")
# @login_required
def ddelete(department_id):
    department_to_delete = DepartmentDB.query.get_or_404(department_id)

    try:
        db.session.delete(department_to_delete)
        db.session.commit()
        return redirect('/departments')

    except:
        return "There was a problem deleting that department"

@app.route("/departments/update/<int:department_id>", methods=['GET','POST'])
# @login_required
def dupdate(department_id):
    section = DepartmentDB.query.get_or_404(department_id)

    if request.method == 'POST':
        section.department_name = request.form['new_department_name']

        try:
            db.session.commit()
            return redirect('/departments')

        except:
            return 'There was an issue updating this course'

    else:
        return render_template("departmentupdate.html", section = section)


#------------------------------------------------------------------------------------------------------------

@app.route("/courses", methods = ['GET', 'POST'])
# @login_required
def course():
    if request.method == "POST":
        new_course = request.form['new_course_name']
        new_entry = CourseDB(course_name=new_course)

        try:
            db.session.add(new_entry)
            db.session.commit()
            return redirect('/courses')

        except:
            return "There was an issue adding this course"

    else:
        majors = CourseDB.query.all()
        return render_template("courses.html", majors = majors)
    
@app.route("/courses/delete/<int:course_id>")
# @login_required
def cdelete(course_id):
    course_to_delete = CourseDB.query.get_or_404(course_id)

    try:
        db.session.delete(course_to_delete)
        db.session.commit()
        return redirect('/courses')

    except:
        return "There was a problem deleting that course"

@app.route("/courses/update/<int:course_id>", methods=['GET','POST'])
# @login_required
def cupdate(course_id):
    major = CourseDB.query.get_or_404(course_id)

    if request.method == 'POST':
        major.course_name = request.form['new_course']

        try:
            db.session.commit()
            return redirect('/courses')

        except:
            return 'There was an issue updating this course'

    else:
        return render_template("courseupdate.html", major = major)


if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(debug=True)


#testing git
