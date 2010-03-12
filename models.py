# -*- coding: utf-8 -*-
from google.appengine.ext import db

class Game(db.Model):
    session_key = db.StringProperty()
    title = db.StringProperty()
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
        return self.owner_name if self.owner_name else "名無しさん"
