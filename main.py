import logging
import urllib
import urllib2
import hashlib
 
from google.appengine.api import mail
from google.appengine.ext import webapp, db
from google.appengine.api import urlfetch, memcache, users
from google.appengine.ext.webapp import util, template
from google.appengine.api.labs import taskqueue
from django.utils import simplejson
from django.template.defaultfilters import timesince 

class HackUp(db.Model):
    user = db.UserProperty(auto_current_user_add=True)
    details = db.StringProperty(required=True, multiline=True)
    address = db.StringProperty(required=True, multiline=True)
    created = db.DateTimeProperty(auto_now_add=True)
    when = db.DateTimeProperty(auto_now_add=True)

# Handlers:
class ViewHandler(webapp.RequestHandler):
    def get(self,id):
       user = users.get_current_user()
       self.response.out.write(template.render('templates/view.html', locals()))

class CreateHandler(webapp.RequestHandler):
    def get(self):
       user = users.get_current_user()
       self.response.out.write(template.render('templates/create.html', locals()))
       
    def post(self, update_id):
       user = users.get_current_user()
       self.redirect('/')

class ConfirmHandler(webapp.RequestHandler):
    def post(self, update_id):
       user = users.get_current_user()
       self.redirect('/')

class MainHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            logout_url = users.create_logout_url('/')
        else:
            login_url = users.create_login_url('/')
        self.response.out.write(template.render('templates/main.html', locals()))
    
def main():
    application = webapp.WSGIApplication([
        ('/', MainHandler), #This list all the upcoming hackups and has a link to create a new one
        ('/view/(.+)', ViewHandler), #This allows to see details of the hackup, who is going, and confirm
        ('/confirm/(.+)', ConfirmHandler), #This allows to confirm going to a hackup
        ('/create', CreateHandler), #This allows to create a new thing
      ], debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()