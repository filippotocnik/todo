from google.appengine.ext import ndb


class Sporocilo(ndb.Model):
    ime = ndb.StringProperty()
    tekst = ndb.StringProperty()
    nastanek = ndb.DateTimeProperty(auto_now_add=True)
