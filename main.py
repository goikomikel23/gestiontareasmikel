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
from google.appengine.ext import ndb

myconfig_dict = {}
myconfig_dict['webapp2_extras.sessions'] = {
  'secret_key': 'aegoradhfgnfiosgbnodfngs',
}



formLogin = '''
<html>
<body>
    <form action='/login' method="post">
        <h1 align="center">Welcome</h1>
        <p align="center">
            Email*: <input type="text" name="email" value="pepe@ikasle.ehu.es" required/>
        <br/>
        Password*: <input type="password" name="password" value="pepe" required/>
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


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(formLogin)
        self.response.out.write("<p align='Center'><a href='/register'>Register</a></p>")


"""class BaseHandler(webapp2.RequestHandler):
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()
        """

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

                        #self.session['Rol'] = "Student"
                        #self.session['Email'] = email

                        #self.response.write(str(self.session['Rol']))
                        #self.response.write(str(self.session['Email']))

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
    ('/professor', Professor)
], debug=True)