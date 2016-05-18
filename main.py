#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import cgi
import re
import webapp2
from webapp2_extras import sessions
#from webapp2_extras import session_module
from google.appengine.ext import ndb



formLogin = '''
<html>
<body>
    <form action='/login' method="post">
        <h1 align="center">Welcome</h1>
        <p align="center">
            Email*: <input type="text" name="email" value="josean@ehu.es" required/>
        <br/>
        Password*: <input type="password" name="password" value="josean" required/>
        <br/>
        <input type="submit" value="Enviar"/>
        </p>
    </form>
</body>
</html>
'''

signup_form = '''
<html>
<body>
    <form action='/registerData' method="post">
        <h1 align="center">Registration</h1>
        <p align="center">
            Email*:
                <input type="text" name="email" placeholder="Email" required/>
                <!--<div class="error">%(email_error)s</div>-->
        <br/>
            Password*:
                <input type="password" name="password" placeholder="Password" required/>
                <!--<div class="error">%(password_error)s</div>-->
        <br/>
            Repeat Password*:
                <input type="password" name="verify" placeholder="Verify" required/>
                <!--<div class="error">%(verify_error)s</div>-->
        <br/>
            Name*:
                <input type="text" name="name" placeholder="Name" required/>
                <!--<div class="error">%(name_error)s</div>-->
        <br/>
            LastName*:
                <input type="text" name="lastName" placeholder="Last Name" required/>
                <!--<div class="error">%(lastName_error)s</div>-->
        <br/>
            DNI*:
                <input type="text" name="dni" placeholder="DNI" required/>
                <!--<div class="error">%(dni_error)s</div>-->
        <br/>
        <br/>
            Secret Question:
                <input type="text" name="secretQ" placeholder="Your Secret Question"/>
                <!--<div class="error">%(question_error)s</div>-->
        <br/>
            Answer:
                <input type="text" name="answer" placeholder="Your Answer"/>
                <!--<div class="error">%(answer_error)s</div>-->
        <br/>
                <input type="submit" value="Registrar"/>
        </p>
    </form>
</body>
</html>
'''

formAdmin = """
<html>
<body>
    <form>
        <h1 align="center">Admin Zone</h1>
        <table style="border:1px solid yellowgreen;border-collapse:collapse;" align="center">
            <th style="border:1px solid yellowgreen;">Dashboard</th>
            <tr>
                <td class="admin">%(access_admin)s</td>
            </tr>
            <tr>
                <td class="admin">%(rol_admin)s</td>
            </tr>
            <tr>
                <td class="admin">%(delete_admin)s</td>
            </tr>
        </table>
    </form>
</body>
</html>
"""

formProfessor = """
<html>
<body>
    <form>
        <h1 align="center">Professor Zone</h1>
        <table style="border:1px solid yellowgreen;border-collapse:collapse;" align="center">
            <th style="border:1px solid yellowgreen;">Dashboard</th>
            <tr>
                <td class="professor">%(subject_professor)s</td>
            </tr>
            <tr>
                <td class="professor">%(rol_admin)s</td>
            </tr>
            <tr>
                <td class="professor">%(delete_admin)s</td>
            </tr>
        </table>
    </form>
</body>
</html>
"""


formAccess = """
<html>
<body>
    <form action='/changeRol' method='POST'>
        <h1 align="center">Access Zone</h1>
        <h4 align="center">Here you have the users requesting access to your database. Assign them a rol to give access.</h4>
        <table style="border:1px solid yellowgreen;border-collapse:collapse;" align="center">
            <th style="border:1px solid yellowgreen;">Name</th>
            <th style="border:1px solid yellowgreen;">Last Name</th>
            <th style="border:1px solid yellowgreen;">Email</th>
            <th style="border:1px solid yellowgreen;">Rol</th>
            <tr class="access">
                %(user_access)s
            </tr>
        </table>
        <p align="center"><input type='Submit' value='Change'/></p>
    </form>
</body>
</html>
"""

formAccess2 = """
<html>
<body>
    <form>
        <h1 align="center">Access Zone</h1>
        <p align="center">%(user_access)s</p>
    </form>
</body>
</html>
"""

formRol = """
<html>
<body>
    <form action='/changeRol3' method='POST'>
        <h1 align="center">Rols Zone</h1>
        <h4 align="center">Change the rol to the users you want</h4>
        <table style="border:1px solid yellowgreen;border-collapse:collapse;" align="center">
            <th style="border:1px solid yellowgreen;">Name</th>
            <th style="border:1px solid yellowgreen;">Last Name</th>
            <th style="border:1px solid yellowgreen;">Email</th>
            <th style="border:1px solid yellowgreen;">Current Rol</th>
            <th style="border:1px solid yellowgreen;">Change Rol</th>
            <tr class="access">
                %(user_access)s
            </tr>
        </table>
        <p align="center"><input type='Submit' value='Change'/></p>
    </form>
</body>
</html>
"""

formRol2 = """
<html>
<body>
    <form>
        <h1 align="center">Rols Zone</h1>
        <p align="center">%(user_access)s</p>
    </form>
</body>
</html>
"""

formDelete = """
<html>
<body>
    <form action='/deleteUser' method='POST'>
        <h1 align="center">Delete Zone</h1>
        <h4 align="center">Delete the users you want</h4>
        <table style="border:1px solid yellowgreen;border-collapse:collapse;" align="center">
            <th style="border:1px solid yellowgreen;">Name</th>
            <th style="border:1px solid yellowgreen;">Last Name</th>
            <th style="border:1px solid yellowgreen;">Email</th>
            <th style="border:1px solid yellowgreen;">Rol</th>
            <th style="border:1px solid yellowgreen;">Delete</th>
            <tr class="access">
                %(user_access)s
            </tr>
        </table>
        <p align="center"><input type='Submit' value='Delete Selected'/></p>
    </form>
</body>
</html>
"""

formUsers = """
<html>
<body>
        <h4 align="center">Users in your database</h4>
        <table style="border:1px solid yellowgreen;border-collapse:collapse;" align="center">
            <th style="border:1px solid yellowgreen;">Name</th>
            <th style="border:1px solid yellowgreen;">Last Name</th>
            <th style="border:1px solid yellowgreen;">Email</th>
            <th style="border:1px solid yellowgreen;">Rol</th>
            <tr class="access">
                %(user_access)s
            </tr>
        </table>
</body>
</html>
"""

formSubject = """
<html>
<body>
    <form action='/newSubject' method="post">
        <h4 align="center">Add a new subject</h4>
        <p align="center">
            Name
        <br/>
            <input type="text" name="name" required/>
        <br/>
            Code
        <br/>
            <input type="text" name="code" required/>
        <br/>
            Description
         <br/>
            <textarea type="text" name="description"></textarea>
        <br/>
        <input type="submit" value="Create"/>
        </p>
    </form>
</body>
</html>
"""

formSubjects = """
<html>
<body>
        <h4 align="center">Your Subjects</h4>
        <table style="border:1px solid yellowgreen;border-collapse:collapse;" align="center">
            <th style="border:1px solid yellowgreen;">Code</th>
            <th style="border:1px solid yellowgreen;">Name</th>
            <th style="border:1px solid yellowgreen;">Description</th>
            <tr class="subjects">
                %(professor_subjects)s
            </tr>
        </table>
</body>
</html>
"""

formTasksDash = """
<html>
<body>
    <form>
        <h1 align="center">Tasks</h1>
        <table style="border:1px solid yellowgreen;border-collapse:collapse;" align="center">
            <th style="border:1px solid yellowgreen;">Dashboard</th>
            <tr>
                <td class="tasks">%(tasks_add)s</td>
            </tr>
            <tr>
                <td class="tasks">%(tasks_delete)s</td>
            </tr>
        </table>
    </form>
</body>
</html>
"""

formTasks = """
<html>
<body>
        <h4 align="center">Your Tasks</h4>
        <table style="border:1px solid yellowgreen;border-collapse:collapse;" align="center">
            <th style="border:1px solid yellowgreen;">Subject</th>
            <th style="border:1px solid yellowgreen;">Code</th>
            <th style="border:1px solid yellowgreen;">Description</th>
            <tr class="access">
                %(tasks)s
            </tr>
        </table>
</body>
</html>
"""

formAddTask = """
<html>
<body>
    <form action='/newTask' method="post">
        <h4 align="center">Add a new task</h4>
        <p align="center">
            Subject
        <br/>
            %(subject_choose)s
        <br/>
            Code
        <br/>
            <input type="text" name="code" required/>
        <br/>
            Description
         <br/>
            <textarea type="text" name="description"></textarea>
        <br/>
        <input type="submit" value="Create"/>
        </p>
    </form>
</body>
</html>
"""


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(formLogin)
        self.response.out.write("<p align='Center'><a href='/register'>Register</a></p>")



class RegisterForm(webapp2.RequestHandler):
    def get(self):
        self.response.write(signup_form)

class Login(webapp2.RequestHandler):

    def post(self):

        email = self.request.get('email')
        password = self.request.get('password')


        user = User.query(User.email== email).count()

        if(valid_email(email)):
            if(user==0):
                self.response.write(formLogin)
                self.response.out.write("<p align='Center'>THE INTRODUCED EMAIL IS NOT REGISTERED</p>")
            else:

                authen = User.query(User.password==password, User.email==email).count()
                user = ndb.gql("Select * from User where email='"+email+"'").get()

                if(authen==1):

                    if(user.rol=='Unknown'):
                        self.response.write("<!doctype html><html><body><h3 align='center'>You have to wait till the administrator gives you access</h3><p align='center'><a href='/'>Return</a></body></html>")
                    elif(user.rol=='Student'):

                        """if self.session.get('counter'):
                            self.response.out.write('<b>La sesion existe</b><p>')
                            counter = self.session.get('counter')
                            self.session['counter'] = counter + 1
                            self.response.out.write('<h2>Numero de accesos = ' + str(self.session.get('counter')) + '</h2>')
                        else:
                            self.response.out.write('<b>Sesion Creada</b><p>')
                            self.session['counter'] = 1
                            self.response.out.write('<h2>Numero de accesos = ' + str(self.session.get('counter')) + '</h2>')


                        self.session['Rol'] = "Student"
                        self.session['Email'] = email

                        self.response.write(formLogin)
                        self.response.out.write("<p align='Center'>"+self.session['Rol']+"</p>")"""

                        self.redirect('/student')



                    elif(user.rol=='Professor'):



                        #self.session['Rol'] = "Professor"
                        #self.session['Email'] = email

                        self.redirect('/professor')

                    else:
                        #self.session['Rol'] = "Admin"
                        #self.session['Email'] = email

                        self.redirect('/admin')
                else:
                    self.response.write(formLogin)
                    self.response.out.write("<p align='Center'>PASSWORD INCORRECT</p>")
        else:
            self.response.write(formLogin)
            self.response.out.write("<p align='Center'>YOUR EMAIL DOESN'T RULES, TRY IT AGAIN</p>")

class Admin(webapp2.RequestHandler):
    def write_form(self, access_admin="", rol_admin="", delete_admin=""):
        self.response.out.write(formAdmin %
                                {"access_admin": "<a href='/access'>Access</a>",
                                 "rol_admin": "<a href='/rol'>Change Rol</a>",
                                 "delete_admin": "<a href='/delete'>Delete User</a>"})

        users = ndb.gql("SELECT * FROM User where email!='admin@ehu.es'")
        count = ndb.gql("SELECT * FROM User where email!='admin@ehu.es'").count()

        sentence2 = ""

        if (count == 0):
            self.response.out.write(
                formUsers % {"user_access": "<p align='center'>There're not users in your database</p>"})
        else:
            for user in users:
                sentence = "<tr><td>" + user.name + "</td><td>" + user.lastName + "</td><td>" + user.email + "</td><td>" + user.rol + "</td></tr>"
                sentence2 = sentence2 + sentence


            self.response.out.write(formUsers % {"user_access": sentence2})

    def get(self): self.write_form()

class Professor(webapp2.RequestHandler):
    def write_form(self, subject_professor="", rol_admin="", delete_admin=""):

        session = 'josean@ehu.es'

        self.response.out.write(formProfessor %
                                {"subject_professor": "<a href='/subject'>Add new subject</a>",
                                 "rol_admin": "<a href='/Tasks'>Tasks</a>",
                                 "delete_admin": "<a href='/delete'>Delete User</a>"})

        subs = ndb.gql("SELECT * FROM Subject where professor='"+session+"'")
        count = ndb.gql("SELECT * FROM Subject where professor='"+session+"'").count()

        sentence2 = ""

        if (count == 0):
            self.response.out.write(
                formSubjects % {"professor_subjects": "<p align='center'>You have not any subject assigned</p>"})
        else:
            for sub in subs:
                sentence = "<tr><td>" + sub.code + "</td><td>" + sub.name + "</td><td>" + sub.description + "</td></tr>"
                sentence2 = sentence2 + sentence


            self.response.out.write(formSubjects % {"professor_subjects": sentence2})

    def get(self): self.write_form()


class DeleteTask(webapp2.RequestHandler):

    def get(self):
        self.response.write(
            "<!doctype html><html><body><h3 align='center'>This page is under construction</h3><p align='center'><img src='images/construction.jpg' style='width:304px;height:228px;'></p><p align='center'><a href='/tasks'>Return</a></p></body></html>")


class NewTask(webapp2.RequestHandler):

    def post(self):

        session = 'josean@ehu.es'

        task_code = self.request.get('code')
        task_description = self.request.get('description')
        task_subject = self.request.get('subject')

        task = Task.query(Task.taskCode == task_code).count()

        if task == 0:
            s = Task()
            s.taskCode = task_code
            s.description = task_description
            s.subjectCode = task_subject
            s.professor = session

            s.put()

            self.response.write(
                '<!doctype html><html><body><p align="Center">The task has been added successfully</p></body></html>')

        else:
            self.response.write('<!doctype html><html><body><pre>The task ')
            self.response.write(' is already registered</pre></body></html>')

    def write_form(self, subject_choose=""):

        session = 'josean@ehu.es'

        subs = ndb.gql("select * from Subject where professor='josean@ehu.es'")

        sentence = "<select name='subject'>"

        for sub in subs:
            sentence2 = sentence + "<option value='"+sub.code+"'>"+sub.name+"</option>"
            sentence = sentence2

        sentence = sentence + "</select>"

        self.response.out.write(formAddTask %
                                {"subject_choose": sentence
                                 })

        tasks = ndb.gql("SELECT * FROM Task where professor='"+session+"'")
        count = ndb.gql("SELECT * FROM Task where professor='"+session+"'").count()

        sentence2 = ""

        if (count == 0):
            self.response.out.write(
                formTasks % {"tasks": "<p align='center'>There're not users in your database</p>"})
        else:
            for task in tasks:
                sentence = "<tr><td>" + task.subjectCode + "</td><td>" + task.taskCode + "</td><td>" + task.description + "</td></tr>"
                sentence2 = sentence2 + sentence

            self.response.out.write(formTasks % {"tasks": sentence2})

    def get(self):
        self.write_form()


class Tasks(webapp2.RequestHandler):

    def write_form(self, tasks_add="",tasks_delete=""):

        print (    "<img src='construction.jpg'>")

        session = 'josean@ehu.es'

        self.response.out.write(formTasksDash %
                                {"tasks_add": "<a href='/newTask'>New task</a>",
                                 "tasks_delete": "<a href='/deleteTask'>Delete Task</a>"
                                 })


        tasks = ndb.gql("SELECT * FROM Task where professor='" + session + "'")
        count = ndb.gql("SELECT * FROM Task where professor='" + session + "'").count()

        sentence2 = ""

        if (count == 0):
            self.response.out.write(
                formTasks % {"tasks": "<p align='center'>There're not users in your database</p>"})
        else:
            for task in tasks:
                sentence = "<tr><td>" + task.subjectCode + "</td><td>" + task.taskCode + "</td><td>" + task.description + "</td></tr>"
                sentence2 = sentence2 + sentence

            self.response.out.write(formTasks % {"tasks": sentence2})

    def get(self):
        self.write_form()

class SubjectClass(webapp2.RequestHandler):

    def get(self):
        self.response.write(formSubject)

class NewSubject(webapp2.RequestHandler):

    def post(self):

        session = "josean@ehu.es"

        subject_name = self.request.get('name')
        subject_code = self.request.get('code')
        subject_description = self.request.get('description')

        sub = Subject.query(Subject.name == subject_name, Subject.code == subject_code).count()

        if sub == 0:
            s = Subject()
            s.name = subject_name
            s.code = subject_code
            s.description = subject_description
            s.professor = session

            s.put()

            self.response.write('<!doctype html><html><body><p align="Center">The subject has been added successfully</p></body></html>')

        else:
            self.response.write('<!doctype html><html><body><pre>The email ')
            self.response.write(cgi.escape(self.request.get('email')))
            self.response.write(' is already registered</pre></body></html>')

class Student(webapp2.RequestHandler):
    def write_form(self, access_admin="", rol_admin="", delete_admin=""):
        self.response.out.write(formAdmin %
                                {"access_admin": "<a href='/access'>Access</a>",
                                 "rol_admin": "<a href='/rol'>Change Rol</a>",
                                 "delete_admin": "<a href='/delete'>Delete User</a>"})

        users = ndb.gql("SELECT * FROM User where email!='admin@ehu.es'")
        count = ndb.gql("SELECT * FROM User where email!='admin@ehu.es'").count()

        sentence2 = ""

        if (count == 0):
            self.response.out.write(
                formUsers % {"user_access": "<p align='center'>There're not users in your database</p>"})
        else:
            for user in users:
                sentence = "<tr><td>" + user.name + "</td><td>" + user.lastName + "</td><td>" + user.email + "</td><td>" + user.rol + "</td></tr>"
                sentence2 = sentence2 + sentence


            self.response.out.write(formUsers % {"user_access": sentence2})

    def get(self): self.write_form()


class Access(webapp2.RequestHandler):

    def write_form(self, user_access=""):

        users = ndb.gql("SELECT * FROM User WHERE rol = 'Unknown'")
        count = ndb.gql("SELECT * FROM User WHERE rol = 'Unknown'").count()

        sentence2 = ""

        if(count==0):
            self.response.out.write(formAccess2 % {"user_access": "<p align='center'>There're not users requesting access</p>"})
        else:
            for user in users:
                sentence = "<tr><td>"+user.name+"</td><td>"+user.lastName+"</td><td>"+user.email+"</td>"
                assignRol = "<td class='assignRol'><input type='radio' name='"+user.name+"' value='Student'>Student<input type='radio' name='"+user.name+"' value='Professor'>Professor</td></tr>"

                sentence = sentence + assignRol

                sentence2 = sentence2 + sentence

            self.response.out.write(formAccess % {"user_access": sentence2})

    def get(self):
        self.write_form()

class ChangeRol(webapp2.RequestHandler):

    def post(self):
        users = ndb.gql("SELECT * FROM User WHERE rol = 'Unknown'")

        for user in users:
            rol = self.request.get(user.name)
            user.rol = rol
            user.put()

        self.response.out.write(formAccess2 % {"user_access": "THE ROLS HAVE BEEN CHANGED"})


class ChangeRol2(webapp2.RequestHandler):

    def write_form(self, user_access=""):

        users = ndb.gql("SELECT * FROM User where email!='admin@ehu.es'")
        count = ndb.gql("SELECT * FROM User where email!='admin@ehu.es'").count()

        sentence2 = ""

        if (count == 0):
            self.response.out.write(
                formRol % {"user_access": "<p align='center'>There're not users</p>"})
        else:
            for user in users:
                sentence = "<tr><td>" + user.name + "</td><td>" + user.lastName + "</td><td>" + user.email + "</td><td>"+ user.rol + "</td>"
                assignRol = "<td class='assignRol'><input type='radio' name='" + user.name + "' value='Student'>Student<input type='radio' name='" + user.name + "' value='Professor'>Professor</td></tr>"

                sentence = sentence + assignRol
                sentence2 = sentence2 + sentence

            self.response.out.write(formRol % {"user_access": sentence2})

    def get(self):
        self.write_form()


class ChangeRol3(webapp2.RequestHandler):

    def post(self):
        users = ndb.gql("SELECT * FROM User WHERE email!='admin@ehu.es'")

        for user in users:
            rol = self.request.get(user.name)

            if rol:
                user.rol = rol
                user.put()

        self.response.out.write(formRol2 % {"user_access": "THE ROLS HAVE BEEN CHANGED"})


class DeleteUser(webapp2.RequestHandler):

    def write_form(self, user_access=""):

        users = ndb.gql("SELECT * FROM User where email!='admin@ehu.es'")
        count = ndb.gql("SELECT * FROM User where email!='admin@ehu.es'").count()

        sentence2 = ""

        if (count == 0):
            self.response.out.write(
                formDelete % {"user_access": "<p align='center'>There're not users in your database</p>"})
        else:
            for user in users:
                sentence = "<tr><td>" + user.name + "</td><td>" + user.lastName + "</td><td>" + user.email + "</td><td>"+ user.rol + "</td>"
                assignRol = "<td align='center'class='assignRol'><input type='radio' name='" + user.name + "' value='Delete'></td></tr>"

                sentence = sentence + assignRol
                sentence2 = sentence2 + sentence

            self.response.out.write(formDelete % {"user_access": sentence2})

    def get(self):
        self.write_form()

class DeleteUser2(webapp2.RequestHandler):

    def post(self):
        users = ndb.gql("SELECT * FROM User WHERE email!='admin@ehu.es'")

        for user in users:
            rol = self.request.get(user.name)

            if rol:
                user.delete()
                #HACER BIEN EL BORRADO, NO FUNCIONA


        self.response.out.write(formRol2 % {"user_access": "THE ROLS HAVE BEEN CHANGED"})



class RegisterData(webapp2.RequestHandler):
    def write_form(self, email="", email_error="", password="", password_error="", verify="", verify_error="", name="",
                   name_error="", lastName="", lastName_error="", dni="", dni_error="", question="", question_error="",
                   answer="", answer_error=""):

        def get(self):
            self.write_form()


    def post(self):
        user_email = self.request.get('email')
        user_password = self.request.get('password')
        user_verify = self.request.get('verify')
        user_name = self.request.get('name')
        user_lastName = self.request.get('lastName')
        user_dni = self.request.get('dni')
        user_question = self.request.get('question')
        user_answer = self.request.get('answer')

        user = User.query(User.name == user_name, User.email == user_email).count()

        if user == 0:
            u = User()
            u.email = user_email
            u.password = user_password
            u.verify = user_verify
            u.name = user_name
            u.lastName = user_lastName
            u.dni = user_dni
            u.question = user_question
            u.answer = user_answer
            u.rol = "Unknown"
            u.put()

            self.response.write('<!doctype html><html><body>You have to wait till the administrator gives you access</body></html>')

        else:
            self.response.write('<!doctype html><html><body><pre>The email ')
            self.response.write(cgi.escape(self.request.get('email')))
            self.response.write(' is already registered</pre></body></html>')




def escape_html(s):
    return cgi.escape(s, quote=True)


class User(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    email = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    verify = ndb.StringProperty(required=True)
    name = ndb.StringProperty(required=True)
    lastName = ndb.StringProperty(required=True)
    dni = ndb.StringProperty(required=True)
    question = ndb.StringProperty(required=True)
    answer = ndb.StringProperty(required=True)
    rol = ndb.StringProperty(required=False)

class Subject(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    name = ndb.StringProperty(required=True)
    description = ndb.StringProperty(required=True)
    code = ndb.StringProperty(required=True)
    professor = ndb.StringProperty(required=True)

class Task(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    subjectCode = ndb.StringProperty(required=True)
    taskCode = ndb.StringProperty(required=True)
    description = ndb.StringProperty(required=True)
    professor = ndb.StringProperty(required=True)


EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
GENERIC_RE = re.compile(r" ")


def valid_email(email):
    return EMAIL_RE.match(email)
def valid_password(password):
    return PASSWORD_RE.match(password)
def valid_generic(generic):
    return GENERIC_RE.match(generic)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/register', RegisterForm),
    ('/registerData', RegisterData),
    ('/admin', Admin),
    ('/login', Login),
    ('/access', Access),
    ('/changeRol', ChangeRol),
    ('/changeRol3', ChangeRol3),
    ('/rol', ChangeRol2),
    ('/delete', DeleteUser),
    ('/deleteUser', DeleteUser2),
    ('/student', Student),
    ('/professor', Professor),
    ('/subject', SubjectClass),
    ('/newSubject', NewSubject),
    ('/Tasks', Tasks),
    ('/newTask', NewTask),
    ('/deleteTask', DeleteTask)
], debug=True)