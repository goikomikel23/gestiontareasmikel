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
    <form method="post">
        <h1 align="center">Welcome</h1>
        <p align="center">
            Login : <input type="text" name="login"/>
        <br/>
        Password: <input type="password" name="password"/>
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
            Email:
                <input type="text" name="email" placeholder="Email"/>
                <!--<div class="error">%(email_error)s</div>-->
        <br/>
            Password:
                <input type="password" name="password" placeholder="Password"/>
                <!--<div class="error">%(password_error)s</div>-->
        <br/>
            Repeat Password:
                <input type="password" name="verify" placeholder="Verify"/>
                <!--<div class="error">%(verify_error)s</div>-->
        <br/>
            Name:
                <input type="text" name="name" placeholder="Name"/>
                <!--<div class="error">%(name_error)s</div>-->
        <br/>
            LastName:
                <input type="text" name="lastName" placeholder="Last Name"/>
                <!--<div class="error">%(lastName_error)s</div>-->
        <br/>
            DNI:
                <input type="text" name="dni" placeholder="DNI"/>
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



class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(formLogin)
        self.response.out.write("<p align='Center'><a href='/register'>Register</a></p>")

class RegisterForm(webapp2.RequestHandler):
    def get(self):
        self.response.write(signup_form)

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
            u.put()

            self.response.write('<!doctype html><html><body>You have been registered as:<pre>')
            self.response.write(cgi.escape(self.request.get('email')))
            self.response.write('</pre></body></html>')

        else:
            self.response.write('<!doctype html><html><body>The email <pre>')
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
    ('/registerData', RegisterData)
], debug=True)