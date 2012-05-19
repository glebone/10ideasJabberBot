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
        str_args = args.split(" ")
        print "8797"
        print str_args
        if len(str_args) < 2:
            return "error"
        print str_args[0]
        print str_args[1]
        ha = POST(self.cur_host+"/users.json",params={'user[email]' : str_args[0], "user[password]" : str_args[1]}, async=False)
        auth_dic =  json.loads(ha)
        print auth_dic
        print  mess.getFrom().getStripped()
        print auth_dic["auth_token"]
        self.my_cursor.execute('insert into users (name, token, jabber) values(?, ?, ?)', (str_args[0], auth_dic["auth_token"], mess.getFrom().getStripped()))
        print "fgdfgdfg"
        self.my_connection.commit
        return auth_dic["auth_token"]

    @botcmd
    def doauth(self, mess, args):
        self.auth_token = "zFwrzUEQgrMNC2LGaxR1"
        return self.auth_token

    @botcmd
    def my_ideas(self, mess, args):
        ideas = GET(self.cur_host+"/ideas.json", params={'auth_token' : self.auth_token})
        ideas_array = json.loads(ideas)
        print ideas_array
        ideas_str = ""
        print "2"
        for cur_idea in ideas_array:
            print "3"
            print cur_idea
            cur_idea_str = cur_idea['created_at'] + " - " + cur_idea['essential']
            ideas_str += cur_idea_str
        return ideas_str



    @botcmd
    def public_ideas(self, mess, args):
        print self.cur_host
        print self.auth_token
        public = GET(self.cur_host+"/ideas/public.json", params={'auth_token' : self.auth_token})
        print public
        return public

    @botcmd
    def add_idea(self, mess, args):
        print(args)
        status = POST(self.cur_host+"/ideas.json?auth_token="+self.auth_token, params={'idea[essential]' : args}, async=False)
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
    my_connection = sqlite.connect('ideas_bot.sqlite')
    my_cursor = my_connection.cursor()
    my_cursor.execute('insert into users (name, token, jabber) values(?, ?, ?)', ("dsdf", "dsfsdf", "fdsfsdfdsfsf"))
    my_connection.commit
    ideas_bot.serve_forever()

