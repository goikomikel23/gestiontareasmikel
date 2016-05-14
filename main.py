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
import re
from calendar import weekday

import webapp2
import cgi
#import ndb

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
                <input type="text" name="email value="%(email)s"/>
                <div class="error">%(email_error)s</div>
        <br/>
            Password:
                <input type="password" name="password" value="%(password)s"/>
                <div class="error">%(password_error)s</div>
        <br/>
            Repeat Password:
                <input type="password" name="verify" value="%(verify)s"/>
                <div class="error">%(verify_error)s</div>
        <br/>
            Name:
                <input type="password" name="name" value="%(name)s"/>
                <div class="error">%(name_error)s</div>
        <br/>
            LastName:
                <input type="password" name="lastName" value="%(lastName)s"/>
                <div class="error">%(lastName_error)s</div>
        <br/>
            DNI:
                <input type="password" name="dni" valuel="%(dni)s"/>
                <div class="error">%(dni_error)s</div>
        <br/>
        <br/>
        Recover password Question:
            Secret Question:
                <input type="password" name="secretQ" value="%(question)s"/>
                <div class="error">%(question_error)s</div>
        <br/>
            Answer:
                <input type="password" name="answer" value="%(answer)s"/>
                <div class="error">%(answer_error)s</div>
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
    def post(self):
        self.response.write('<!doctype html><html><body>You wrote:<pre>')
        self.response.write(cgi.escape(self.request.get('email')))
        self.response.write('</pre></body></html>')


class User(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)
    email = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    verify = ndb.StringProperty(required=True)
    name = ndb.StringProperty(required=True)
    lastname = ndb.StringProperty(required=True)
    dni = ndb.StringProperty(required=True)
    question = ndb.StringProperty(required=True)
    answer = ndb.StringProperty(required=True)


class SignupHandler: #(session_module.BaseSessionHandler):
#se declara una función ...
    def write_form (self, email="", email_error="", password="", password_error="",verify="", verify_error="", name="",
                    name_error="", lastName="", lastName_error="", dni="", dni_error="", question="", question_error="",
                    answer="", answer_error=""):

        self.response.out.write(signup_form % {
            "email" : email,
            "email_error" : email_error,
            "password" : password,
            "password_error": password_error,
            "verify" : verify,
            "verify_error": verify_error,
            "name" : name,
            "name_error": name_error,
            "lastName" : lastName,
            "lastName_error": lastName_error,
            "dni" : dni,
            "dni_error" : dni_error,
            "question" : question,
            "question_error": question_error,
            "answer" : answer,
            "answer_error": answer_error,
            })


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
        sani_email = self.escape_html(user_email)
        sani_password = self.escape_html(user_password)
        sani_verify = self.escape_html(user_verify)
        sani_name = self.escape_html(user_name)
        sani_lastName = self.escape_html(user_lastName)
        sani_dni = self.escape_html(user_dni)
        sani_question = self.escape_html(user_question)
        sani_answer = self.escape_html(user_answer)
        email_error = ""
        password_error = ""
        verify_error = ""
        name_error = ""
        lastName_error = ""
        dni_error = ""
        question_error = ""
        answer_error = ""

    error = False

    if not valid_email(user_email):
        username_error = "Email incorrecto!"
        error = True
    if not valid_password(user_password):
        username_error = "Password incorrecto!"
        error = True
    if not valid_password(user_verify):
        username_error = "Verify incorrecto!"
        error = True
    if not valid_generic(user_name):
        username_error = "Name incorrecto!"
        error = True
    if not valid_generic(user_lastName):
        username_error = "lastName incorrecto!"
        error = True
    if not valid_generic(user_dni):
        username_error = "dni incorrecto!"
        error = True
    if not valid_generic(user_question):
        username_error = "question incorrecto!"
        error = True
    if not valid_generic(user_answer):
        username_error = "answer incorrecto!"
        error = True


    def escape_html(s):
        return cgi.escape(s, quote=True)


EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
GENERIC_RE = re.compile(r" ")


    def valid_email(email):
        return EMAIL_RE.match(email)
    def valid_password(password):
        return PASSWORD_RE.match(password)
    def valid_generic(generic):
        return GENERIC_RE.match(generic)

    if error:
        self.write_form(sani_email, sani_password, sani_verify, sani_name, sani_lastName, sani_dni, sani_question, sani_answer,
                        email_error, password_error, verify_error, name_error, lastName_error, dni_error, question_error, answer_error)
    else:
        user= User.query(User.email==user_email

        """

        SEGUIR AQUÍ
                              Visitante.email==user_email).count()
    if user==0:
        u=Visitante()
        u.nombre=user_username u.email=user_email
        u.password=user_password
        u.put()
        self.redirect("/welcome?username=%s" % user_username)

    else:
        self.write_form(sani_username, sani_password, sani_verify, sani_email,
                        username_error, password_error, verify_error, email_error)
        self.response.out.write ("Kaixo: %s <p> Ya estabas fichado" %user_username)

        """








app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/register', RegisterForm),
    ('/registerData', RegisterData)
], debug=True)

