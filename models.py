# -*- coding: utf-8 -*-
from google.appengine.ext import db

class Game(db.Model):
    session_key = db.StringProperty()
    title = db.StringProperty()
    komi = db.FloatProperty(default=float(0))
    black_is = db.StringProperty()
    owner = db.StringProperty()
    client = db.StringProperty()
    owner_name = db.StringProperty()
    client_name = db.StringProperty()
    status = db.BooleanProperty(default=False)
    created_at = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def exist(self,session_key):
        gql = db.GqlQuery("SELECT * FROM Game WHERE session_key = :key" ,key=session_key )
        return gql.get()
     
    def display_title(self):
        return self.title if self.title else "無題の対局"

    def display_owner_name(self):
        return self.owner_name if len(self.owner_name) > 0  else "名無しさん"

    def display_client_name(self):
        return self.client_name if len(self.client_name) > 0  else "名無しさん"


    def owner_is(self):
        if not self.black_is :
            return False
        if self.black_is == "owner" :
            return "●"
        else :
            return "○"

    def client_is(self):
        if not self.black_is :
            return False
        if self.black_is == "client" :
            return "●"
        else :
            return "○"
