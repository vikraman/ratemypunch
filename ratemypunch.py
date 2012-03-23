import webapp2

from google.appengine.ext import db

class Punch(db.Model):
    rating = db.IntegerProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    drinks = db.ListProperty(db.Key)

class Drink(db.Model):
    name = db.StringProperty()
    brand = db.StringProperty()
    image = db.BlobProperty()

class DrinkHandler(webapp2.RequestHandler):
    def get(self):
        res = ','.join([ (drink.name,drink.key()).__str__() for drink in Drink.all() ])
        self.response.out.write(res)

class DrinkAdder(webapp2.RequestHandler):
    def post(self):
        drink_name = self.request.get('name')
        drink = Drink(name=drink_name)
        drink.put()

class PunchHandler(webapp2.RequestHandler):
    def get(self):
        res = ','.join([ punch.rating for punch in Punch.all() ])
        self.response.out.write(res)

class PunchBuilder(webapp2.RequestHandler):
    def post(self):
        drinks = []
        for drink_key in self.request.get('drink_keys', allow_multiple=True):
            drinks.append(db.Key(drink_key))
        punch = Punch.gql("WHERE drinks = :1", drinks).get()
        if punch is None:
            punch = Punch(rating = 0, drinks = drinks)
            punch.put()

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.redirect("/static/wip.html")

app = webapp2.WSGIApplication([('/',MainPage), ('/drink',DrinkHandler),
    ('/drink/add',DrinkAdder),('/punch',PunchHandler),
    ('/punch/build', PunchBuilder)], debug=True)
