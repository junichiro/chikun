import cgi , hashlib , datetime ,random
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
                  "games" : models.Game.all().order("-created_at")
            } )
        )

class NewPage(webapp.RequestHandler):
    def get(self):
        md5 = hashlib.md5()
        md5.update( str( datetime.datetime.now() ) )
        hash = md5.hexdigest()
        self.redirect( "/game/" + hash )


class GamePage(webapp.RequestHandler):
    def get(self,game_id):
        game = models.Game.exist( game_id )
        if not game :
            self.response.out.write( template.render( template_path('new.html') , {} ) )
            
        else:
            if not  game.client :
                self.response.out.write( 
                    template.render( template_path('join.html') , {
                            "game" : game , "actions" : models.GameAction.all().filter("game = ", game).order("-created_at")  } )
                    )
            else :
                self.response.out.write(
                    template.render( template_path('show.html') , { 
                            "game" : game , "actions" : models.GameAction.all().filter("game = ", game).order("-created_at") } )
                    )

    def post(self,game_id):
        game = models.Game.exist( game_id )
        if not game :
            game = models.Game()
            game.session_key = game_id
            game.title = self.request.get("title")
            game.size = int(self.request.get("size"))
            md5 = hashlib.md5()
            md5.update( str( datetime.datetime.now()) + game_id  )
            hash = md5.hexdigest()
            game.owner = hash[5:10]
            game.owner_name = self.request.get("owner_name")
            game.komi = float( self.request.get("komi") )
            game.black_is = self.request.get("black_is") if len( self.request.get("black_is") ) > 0 else None


            game.put()

            self.redirect("/game/" + game_id + "/" + game.owner)

        else:
            if not game.client :
                md5 = hashlib.md5()
                md5.update( str( datetime.datetime.now()) + game_id  )
                hash = md5.hexdigest()
                game.client = hash[5:10]
                game.client_name = self.request.get("client_name")
                if not game.black_is :
                    if int( random.random() * 2 ) > 0 :
                        game.black_is = "owner"
                    else :
                        game.black_is = "client"

                game.status = True


                game.put()
                self.redirect("/game/" + game_id + "/" + game.client)


        self.response.out.write( game )

class GamePlayPage(webapp.RequestHandler):
    def get(self,game_id,player_id):
        game = models.Game.exist( game_id )
        if not game :
            self.response.set_status(404)
            self.response.out.write("404 not found")
        else :
            if not game.client and game.owner == player_id :
                self.response.out.write( template.render( template_path("edit.html") , { "game" : game  , "actions" : models.GameAction.all().filter("game = " , game).order("-created_at")  } ) )
            else :
                print "aa"
  
class GamePutPage(webapp.RequestHandler):
    def get(self,game_id,player_id,pos):
        game = models.Game.exist( game_id )
        if not game :
            self.response.set_status(404)
            self.response.out.write("404 not found")
            return False
        else :
            check = models.GameAction.gql("WHERE game = :game AND position = :pos " , game = game , pos = pos )

            if check.get() :
                self.response.set_status(500)
                self.response.out.write("500 error")
                return False

            recent = models.GameAction.all().filter("status = ", True).order("-created_at")

            action = models.GameAction()
            action.game = game
            action.game_key = game.session_key
            action.player_key = player_id
            if not recent.get() :
                action.stone ="black"
                action.num = 0
                action.position = pos
                action.seek_time = 0
                action.status = False

            action.put()

            self.redirect("/game/" + game_id + "/" + player_id )

app = webapp.WSGIApplication(
    [('/', IndexPage), 
     ('/new' , NewPage) , 
     ('/game/(.+?)/(.+?)/(.+?)' , GamePutPage ),
     ('/game/(.+?)/([^/]+?)' , GamePlayPage ) , 
     ('/game/([^/]+?)$' , GamePage ) , 
     ],debug=True)


def main():
    run_wsgi_app( app ) 
