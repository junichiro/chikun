from google.appengine.ext import db

class Game(db.Model):
    session_key = db.StringProperty()
    owner = db.StringProperty()
    client = db.StringProperty()
    owner_name = db.StringProperty()
    client_name = db.StringProperty()
    created_at = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def exist(self,session_key):
        gql = db.GqlQuery("SELECT * FROM Game WHERE session_key = :key" ,key=session_key )
        return gql.get()
