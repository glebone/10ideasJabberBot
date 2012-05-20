#!/usr/bin/python
# Created by glebone@gmail.com 26/04/2012



import sys
from restclient import GET, POST, PUT, DELETE
import json
from pysqlite2 import dbapi2 as sqlite

from jabberbot import *

class TenIdeasBot(JabberBot):

    auth_token = "0"
    cur_host = "http://127.0.0.1:3000"
    db_name = "ideas_bot.sqlite"



    @botcmd
    def register(self, mess, args):
        str_args = args.split(" ")
        print "8797"
        print str_args
        if len(str_args) != 2:
            return "error! Pls enter email - password"
        ha = POST(self.cur_host+"/users.json",params={'user[email]' : str_args[0], "user[password]" : str_args[1]}, async=False)
        auth_dic =  json.loads(ha)
        print auth_dic["auth_token"]
        print  mess.getFrom().getStripped()
        connection = sqlite.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute('INSERT INTO users (name, token, jabber) VALUES(?, ?, ?)', (str_args[0], auth_dic["auth_token"], mess.getFrom().getStripped()))
        print "fgdfgdfg"
        connection.commit()
        cursor.close()
        connection.close()
        return auth_dic["auth_token"]

    @botcmd
    def doauth(self, mess, args):
        cur_jid = mess.getFrom().getStripped()
        print cur_jid
        connection = sqlite.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users WHERE jabber = ?', (cur_jid,))
        print "fsdfsdf"
        accounts = cursor.fetchall()
        cursor.close()
        connection.close()
        print accounts
        print len(accounts)
        if len(accounts) < 1:
            return "Pls register first!"
        cur_acc = accounts[0][2]
        print cur_acc
        self.auth_token = cur_acc
        return self.auth_token

    @botcmd
    def my_ideas(self, mess, args):
        ideas = GET(self.cur_host+"/ideas.json", params={'auth_token' : self.auth_token})
        print ideas
        ideas_array = json.loads(ideas)
        ideas_str = ""
        for cur_idea in ideas_array:
            print cur_idea
            cur_idea_str = cur_idea['created_at'] + " - " + cur_idea['essential'] + "\n"
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
    cur_host = "http://127.0.0.1:3000"
    ideas_bot = TenIdeasBot(username, password)

    db_name = 'ideas_bot.sqlite'



    ideas_bot.serve_forever()

