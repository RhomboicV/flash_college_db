from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///uni.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Users
class AdminUser:
    def __init__(self, id, admin_username, admin_password):
        self.id = id
        self.admin_username = admin_username
        self.admin_password = admin_password

    def __repr__(self):
        return f'<AdminUser: {self.admin_username}>'

#Database and Tables
db = SQLAlchemy(app)

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

# @app.route("/login", methods = ['GET', 'POST'])
# def login():
#     if request.method = 'POST':
#         admin_username

@app.route("/", methods = ['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route("/teachers", methods = ['GET', 'POST'])
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
def tdelete(teacher_id):
    teacher_to_delete = TeacherDB.query.get_or_404(teacher_id)

    try:
        db.session.delete(teacher_to_delete)
        db.session.commit()
        return redirect('/teachers')

    except:
        return "There was a problem deleting that Teacher"

@app.route("/teachers/update/<int:teacher_id>", methods=['GET','POST'])
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
def sdelete(student_id):
    student_to_delete = StudentDB.query.get_or_404(student_id)

    try:
        db.session.delete(student_to_delete)
        db.session.commit()
        return redirect('/students')

    except:
        return "There was a problem deleting that student"

@app.route("/students/update/<int:student_id>", methods=['GET','POST'])
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
def ddelete(department_id):
    department_to_delete = DepartmentDB.query.get_or_404(department_id)

    try:
        db.session.delete(department_to_delete)
        db.session.commit()
        return redirect('/departments')

    except:
        return "There was a problem deleting that department"

@app.route("/departments/update/<int:department_id>", methods=['GET','POST'])
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
def cdelete(course_id):
    course_to_delete = CourseDB.query.get_or_404(course_id)

    try:
        db.session.delete(course_to_delete)
        db.session.commit()
        return redirect('/courses')

    except:
        return "There was a problem deleting that course"

@app.route("/courses/update/<int:course_id>", methods=['GET','POST'])
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
    app.run(debug=True)