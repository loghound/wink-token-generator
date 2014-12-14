#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import cgi
import json

import webapp2
from google.appengine.api import urlfetch


MAIN_PAGE_HTML = """\
<!DOCTYPE html>
<html>
<head lang="en">
    <meta charset="UTF-8">
    <title></title>
</head>
<body>
<form action="/token" method="post">
    This little web app will give you the info you need to integrate wink devices into the Home Assistant App
    <br /><br />Wink Username (email):<br>
    <input type="text" name="username" >
    <br>
    Wink Password:<br>
    <input type="password" name="password" >
    <br><br>
    <input type="submit" value="Submit">
</form>
</body>
</html>
"""


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write(MAIN_PAGE_HTML)


class Guestbook(webapp2.RequestHandler):
    def post(self):
        url = "https://winkapi.quirky.com/oauth2/token"
        body = dict(
            client_id="SECRET_CLIENT_ID",
            client_secret="SECRET_CLIENT_SECRET",
            password=cgi.escape(self.request.get('password')),
            username=cgi.escape(self.request.get('username')),
            grant_type="password"
        )
        headers = {"Content-Type": "application/json"}

        result = urlfetch.fetch(url=url,
                                payload=json.dumps(body),
                                method=urlfetch.POST,
                                headers=headers)

        if result.status_code < 205:
            json_results = json.loads(result.content)

            self.response.write(
                "Put the following lines in your configuration file in the wink section<br /><pre>access_token: " +
                json_results["access_token"] +
                "<br />refresh_token: " + json_results["refresh_token"] + "<br /></pre>");
        else:
            self.response.write("Error getting bearer token")


app = webapp2.WSGIApplication([
                                  ('/', MainPage),
                                  ('/token', Guestbook),
                              ], debug=True)