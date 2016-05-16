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
from google.appengine.ext import ndb



formLogin = '''
<html>
<body>
    <form action='/login' method="post">
        <h1 align="center">Welcome</h1>
        <p align="center">
            Email*: <input type="text" name="email" value="admin@ehu.es" required/>
        <br/>
        Password*: <input type="password" name="password" value="admin" required/>
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
    <form>
        <h1 align="center">Access Zone</h1>
        <table style="border:1px solid yellowgreen;border-collapse:collapse;" align="center">
            <th style="border:1px solid yellowgreen;">Name</th>
            <th style="border:1px solid yellowgreen;">Last Name</th>
            <th style="border:1px solid yellowgreen;">Email</th>
            <tr>
                <td class="access">%(name_acess)s</td>
                <td class="access">%(lastName_acess)s</td>
                <td class="access">%(email_acess)s</td>
            </tr>
        </table>
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

                if(authen==1):
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
                                 "rol_admin": "<a href='/rol'>Assign Rol</a>",
                                 "delete_admin": "<a href='/delete'>Delete User</a>"})

    def get(self): self.write_form()

class Access(webapp2.RequestHandler):

    def write_form(self, name_access="", lastName_access="", email_access=""):

        user = User.query(User.rol == "Unknown")
        name = user.name

        self.response.out.write(formAccess % {"access_admin": name
                                              })

    def get(self): self.write_form()

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
    ('/access', Access)
], debug=True)