from google.appengine.ext import ndb


class Todo(ndb.Model):
    task = ndb.StringProperty()
    nastanek = ndb.DateTimeProperty(auto_now_add=True)
