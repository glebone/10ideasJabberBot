#!/usr/bin/python
# Created by glebone@gmail.com 26/04/2012



import sys
from restclient import GET, POST, PUT, DELETE
import json
from pysqlite2 import dbapi2 as sqlite

from jabberbot import *

class TenIdeasBot(JabberBot):

    auth_token = "0"
    cur_host = "http://stage.masterofcode.com:10101"
    db_name = "ideas_bot.sqlite"
    prefetch_users = {}



    @botcmd
    def register(self, mess, args):
        str_args = args.split(" ")
        print "8797"
        print str_args
        if len(str_args) != 2:
            return "error! Pls enter email - password"
        ha = POST(self.cur_host+"/users.json",params={'user[email]' : str_args[0], "user[password]" : str_args[1]}, async=False)
        auth_dic =  json.loads(ha)
        if 'auth_token' in auth_dic.keys():
            print auth_dic["auth_token"]
            print  mess.getFrom().getStripped()
            connection = sqlite.connect(self.db_name)
            cursor = connection.cursor()
            cursor.execute('INSERT INTO users (name, token, jabber) VALUES(?, ?, ?)', (str_args[0], auth_dic["auth_token"], mess.getFrom().getStripped()))
            connection.commit()
            cursor.close()
            connection.close()
            self.prefetch_users[str_args[0]] =  auth_dic["auth_token"]
            return "Email registered"
        else:
            return self.user_login(str_args[0], str_args[1])




    @botcmd
    def public_ideas(self, mess, args):
        cur_jid = mess.getFrom().getStripped()
        if (self.check_user(cur_jid)):
            cur_token = self.prefetch_users[cur_jid]
            ideas = GET(self.cur_host+"/ideas/public.json", params={'auth_token' : cur_token})
            print ideas
            ideas_array = json.loads(ideas)
            ideas_str = ""
            for cur_idea in ideas_array:
                print cur_idea
                cur_idea_str = cur_idea['created_at'] + " - " + cur_idea['essential'] + "\n"
                ideas_str += cur_idea_str
            return ideas_str
        else:
            return "Pls register first!"



    @botcmd
    def my_ideas(self, mess, args):
        cur_jid = mess.getFrom().getStripped()
        if (self.check_user(cur_jid)):
            cur_token = self.prefetch_users[cur_jid]
            print cur_token
            ideas = GET(self.cur_host+"/ideas.json", params={'auth_token' : cur_token})
            print ideas
            ideas_array = json.loads(ideas)
            ideas_str = ""
            for cur_idea in ideas_array:
                print cur_idea
                cur_idea_str = cur_idea['created_at'] + " - " + cur_idea['essential'] + "\n"
                ideas_str += cur_idea_str
            return ideas_str
        else:
            return "Pls register first!"




    @botcmd
    def add_idea(self, mess, args):
        print(args)
        cur_jid = mess.getFrom().getStripped()
        if (self.check_user(cur_jid)):
            cur_token = self.prefetch_users[cur_jid]
            print cur_token
            status = POST(self.cur_host+"/ideas.json?auth_token="+cur_token, params={'idea[essential]' : args}, async=False)
            print status
            return "Idea posted"
        else:
            return "Pls register first!"




    def check_user(self, user_jid):
        print "checking permissions"
        if user_jid in self.prefetch_users:
            print "have code"
            return True
        else:
            print "no jid prefetched"
            connection = sqlite.connect(self.db_name)
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM users WHERE jabber = ?', (user_jid,))
            accounts = cursor.fetchall()
            cursor.close()
            connection.close()
            print accounts
            print len(accounts)
            if len(accounts) < 1:
                return False
            cur_acc = accounts[0][2]
            print cur_acc
            self.prefetch_users.update({user_jid:cur_acc})
            return True


    def user_login(self, cur_email, cur_pass):
        ha = POST(self.cur_host+"/users/sign_in.json",params={'user[email]' : cur_email, "user[password]" : cur_pass}, async=False)
        auth_dic =  json.loads(ha)
        if 'auth_token' in auth_dic.keys():
            print auth_dic["auth_token"]
            connection = sqlite.connect(self.db_name)
            cursor = connection.cursor()
            cursor.execute('INSERT INTO users (name, token, jabber) VALUES(?, ?, ?)', (str_args[0], auth_dic["auth_token"], mess.getFrom().getStripped()))
            print "fgdfgdfg"
            connection.commit()
            cursor.close()
            connection.close()
            self.prefetch_users[str_args[0]] =  auth_dic["auth_token"]
            return "Loged in"
        else:
            return "Login failed"







if __name__ == '__main__':
    if len(sys.argv) != 3:
        print >>sys.stderr, """
        Usage: %s <jid> <password>
        """ % sys.argv[0]

    username, password = sys.argv[1:]
    auth_token = "0"
    cur_host = "http://stage.masterofcode.com:10101"
    prefetch_users = {}
    ideas_bot = TenIdeasBot(username, password)

    db_name = 'ideas_bot.sqlite'



    ideas_bot.serve_forever()

