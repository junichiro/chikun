import cgi , hashlib , datetime
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from utils import template_path
import settings
import models

class IndexPage(webapp.RequestHandler):
    def get(self):
      self.response.out.write(
        template.render(
            template_path('index.html') ,
            {
            } )
        )

class NewPage(webapp.RequestHandler):
    def get(self):
        md5 = hashlib.md5()
        md5.update( str( datetime.datetime.now() ) )
        hash = md5.hexdigest()
        self.redirect( "/games/" + hash )


class GamePage(webapp.RequestHandler):
    def get(self,game_id):
        game = models.Game.exist( game_id )
        if not game :
            self.response.out.write( template.render( template_path('new.html') , {} ) )
            
        else:
            if not  game.client :
                self.response.out.write( 
                    template.render( template_path('join.html') , {
                            "game" : game } )
                    )
            else :
                self.response.out.write(
                    template.render( template_path('show.html') , { 
                            "game" : game } )
                    )

    def post(self,game_id):
        game = models.Game.exist( game_id )
        if not game :
            game = models.Game()
            game.session_key = game_id
            md5 = hashlib.md5()
            md5.update( str( datetime.datetime.now()) + game_id  )
            hash = md5.hexdigest()
            game.owner = hash[5:10]
            game.owner_name = self.request.get("owner_name")

            game.put()

            self.redirect("/games/" + game_id + "/" + game.owner)

        else:
            if not game.client :
                md5 = hashlib.md5()
                md5.update( str( datetime.datetime.now()) + game_id  )
                hash = md5.hexdigest()
                game.client = hash[5:10]
                game.client_name = self.request.get("client_name")
 
                game.put()
                self.redirect("/games/" + game_id + "/" + game.client)


        self.response.out.write( game )

class GamePlayPage(webapp.RequestHandler):
    def get(self,game_id,player_id):
        print player_id
  
app = webapp.WSGIApplication(
    [('/', IndexPage), 
     ('/new' , NewPage) , 
     ('/games/(.+?)/(.+?)' , GamePlayPage ) , 
     ('/games/([^/]+?)$' , GamePage ) , 
     ],debug=True)


def main():
    run_wsgi_app( app ) 
