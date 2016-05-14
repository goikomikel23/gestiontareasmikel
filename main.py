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
import webapp2

formLogin = '''
<html>
<body>
    <form method="post">
        <h1 align="center">Welcome</h1>
        <p align="center">
            User: <input type="text" name="user"/>
        <br/>
        Password: <input type="password" name="password"/>
        <br/>
        <input type="submit" value="Enviar"/>
        </p>
    </form>
    <p align="center">
        <a href='localhost:8080/register'>Register</a>
    </p>
</body>
</html>
'''

register = ''' REGISTRATION '''

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(formLogin)

class Register(webapp2.RequestHandler):
    def get(self):
        self.response.write(register)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/register', Register)
], debug=True)

