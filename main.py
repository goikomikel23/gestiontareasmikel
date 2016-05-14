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
from calendar import weekday

import webapp2
import cgi

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

formRegister = '''
<html>
<body>
    <form action='/registerData' method="post">
        <h1 align="center">Registration</h1>
        <p align="center">
            Email: <input type="text" name="email"/>
        <br/>
        Password: <input type="password" name="password"/>
        <br/>
        Repeat Password: <input type="password" name="password"/>
        <br/>
        Name: <input type="password" name="name"/>
        <br/>
        LastName: <input type="password" name="lastName"/>
        <br/>
        DNI: <input type="password" name="dni"/>
        <br/>
        <br/>
        Recover password Question:
        Secret Question: <input type="password" name="secretQ"/>
        <br/>
        Answer: <input type="password" name="answer"/>
        <br/>
        <input type="submit" value="Registrar"/>
        </p>
    </form>
</body>
</html>
'''

holacaracola = ''' holaaa '''

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(formLogin)
        self.response.out.write("<p align='Center'><a href='/register'>Register</a></p>")

class RegisterForm(webapp2.RequestHandler):
    def get(self):
        self.response.write(formRegister)

class RegisterData(webapp2.RequestHandler):
    def post(self):
        self.response.write('<!doctype html><html><body>You wrote:<pre>')
        self.response.write(cgi.escape(self.request.get('email')))
        self.response.write('</pre></body></html>')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/register', RegisterForm),
    ('/registerData', RegisterData)
], debug=True)

