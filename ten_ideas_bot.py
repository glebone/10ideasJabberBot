#!/usr/bin/python
# Created by glebone@gmail.com 26/04/2012



import sys
from restclient import GET, POST, PUT, DELETE
import json
from pysqlite2 import dbapi2 as sqlite

from jabberbot import *

class TenIdeasBot(JabberBot):

    auth_token = "0"
    cur_host = "http://127.0.0.1"

    @botcmd
    def register(self, mess, args):
        self.auth_token = POST(self.host+"/users",params={'user[email]' : 'glebone@yandex.ru', "user[password]" : '123123'})
        print self.auth_token
        return self.auth_token

    @botcmd
    def doauth(self, mess, args):
        self.auth_token = "zFwrzUEQgrMNC2LGaxR1"
        return self.auth_token

    @botcmd
    def public_ideas(self, mess, args):
        print self.cur_host
        print self.auth_token
        public = GET(self.cur_host+"/ideas/public.json", params={'auth_token' : self.auth_token})
        print public
        return public

    @botcmd
    def add_idea(self, mess, args):
        print(args[0])
        status = POST(self.host+"ideas.json", params={'idea' : args[0], 'auth_token' : self.auth_token})
        print status
        return status

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print >>sys.stderr, """
        Usage: %s <jid> <password>
        """ % sys.argv[0]

    username, password = sys.argv[1:]
    auth_token = "0"
    cur_host = "http://127.0.0.1"
    ideas_bot = TenIdeasBot(username, password)
    #connection = sqlite.connect('ideas_bot.sqlite')
    #cursor = connection.cursor()
    ideas_bot.serve_forever()

