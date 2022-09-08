# 1: Light on
# 2: Light off
# 3: Display on
# 4: Display off
# 5: Boil user in
# 6: Boil user out

class Dummy(Exception):
    pass

class Storage(Exception):
    def __init__(self):
        import sqlite3
        from threading import Thread
        
        self.debug = False

        self.config = Dummy()
        self.getconf()

        self.sqlite3 = sqlite3
        self.db = sqlite3.connect(self.config.database)

        try:
            self.identity()
        except ValueError:
            return -1



        pass

    def log(self, level, action):
        import logging
        from time import time

        if self._logger == None:
            self._logger = logging.getLogger("Storage")
            self._logger.setLevel(logging.DEBUG)
            self._logger.addHandler(logging.StreamHandler())
        








    def getconf(self):
        from json import loads
        from os.path import isfile
        # Check the config.json exists
        if not isfile("config.json"):
            self.config = None
            self.parseconf({})
        else:
            f = open("config.json", "r")
            conf = loads(f)
            f.close()
            self.parseconf(conf)
            return
            

    def parseconf(self, conf):
        try:
            self.config.host = conf["userhost"]
        except KeyError:
            self.config.host = None
        
        try:
            self.config.userid = conf["userid"]
        except KeyError:
            self.config.userid = None
        
        try:
            self.config.database = conf["database"]
        except KeyError:
            self.config.database = "storage.db"

        if self.debug == False:
            try:
                if conf["debug"] == True:
                    self.debug = True
            except KeyError:
                pass
        

    def identity(self):
        cur = self.db.cursor()
        cur.execute("SELECT * FROM user")
        r = cur.fetchone()
        cur.close()
        if r == []:
            user = None
        elif r == ():
            user = None
        elif r == None:
            user = None
        else:
            user = str(r[0])
        
        if self.config.userid == None:
            if user == None: raise ValueError("No user found")
            self.config.userid = user
        elif self.config.userid != user:
            raise ValueError("User ID does not match")
        elif self.config.userid == user:
            return
        else:

        
    def getlog(self):
        cur = self.db.cursor()
        cur.execute("SELECT timestamp, action FROM log")
        r = cur.fetchall()
        cur.close()
        return r

    def find_user(self):
        # Check the computer is online with ICMP
        from os import system
        from time import sleep

        while True:
            response = os.system("ping -n 1 " + self.host + " > nul")
            if response == 0:
                self.user = True
            else:
                self.user = False
            sleep(5)
        

class Compare(Exception):
    def __init__(self):
        pass
    
    def data(self):
        pass


from flask import *
from flask_compress import Compress
import os
import json

compress = Compress()
app = Flask(__name__)
app.secret_key = os.urandom(12)






if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', threaded=True, port=80)