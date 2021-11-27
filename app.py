# Client 192.168.50.14
# Server 192.168.50.17
# Computer, TV, Light, Ondol(Boiler) = 0, 1, 2, 3
# on, off = 1, 0

class Dummy(Exception):
    pass

class Storage(Exception):
    def __init__(self):
        from htmadmin import HTMLFILES
        from threading import Thread
        self.conf = Dummy()
        self.config()
        self.conf.scoreserver = "192.168.50.17"
        self.data = datahandler(self)
        self.html = HTMLFILES(self)

        self.usercheck = Thread(target=self.data.usrchk)
        self.usercheck.start()

        pass
    
    def config(self):
        from json import load
        f = open('config.json', 'r')
        config = load(f)
        self.configparser(config)
        f.close()

        return 0

    def configparser(self, config):
        try:
            if config['host'] == None:
                raise NameError('No host value')
            elif config['host'] == '':
                raise NameError('No host value')
            else:
                self.conf.host = config['host']
        except KeyError:
            raise KeyError('Config Host is not defined')
        
        try:
            self.conf.userid = config['userid']
        except KeyError:
            raise KeyError('Config Userid is not defined')

        try:
            if config['checker'] in ["ping", "ftp"]:
                self.conf.checker = config['checker']
            else:
                print("Attribute error on checker. Set to ping")
                self.conf.checker = "ping"
        except KeyError:
            self.conf.checker = "ping"
        
        return 0
    
    def usrchk(self):
        from time import sleep

        if self.conf.checker == "ping":
            from os import system
            while True:
                rtn = system("ping -n 1 " + self.conf.host + " > nul")
                if rtn == 0: 
                    if self.data.user == False: self.data.actionupdate(4, True)
                else:
                    if self.data.user == True: self.data.actionupdate(4, False)
                sleep(5)
        
        elif self.conf.checker == "ftp":
            userid = "test"
            password = "test"
            import ftplib
            while True:
                try:
                    # timeout 2 sec
                    ftp = ftplib.FTP(self.conf.host, userid, password, timeout=2)
                    ftp.quit()
                    if self.data.user == False: self.data.actionupdate(4, True)
                    break
                except ftplib.all_errors:
                    if self.data.user == False: self.data.actionupdate(4, False)
                    sleep(5)
                    break
        pass

class datahandler(Exception):
    def __init__(self, storage):
        self.storage = storage
        self.data = []
        self.led = False
        self.boil = False
        self.user = False
        self.dataload()
        pass
    
    def dataload(self):
        from json import loads
        f = open('data.json', 'r')
        data = loads(f.read())
        if self.storage.conf.userid != data['userid']:
            if (data['userid'] == None or data['userid'] == '') and data["data"] == []:
                self.data = []
                self.datastore()
            else:
                raise NameError('Userid is not matched')
        
        self.data = data["data"]
        
        f.close()
        return 0

    def datastore(self):
        from json import dumps
        f = open('data.json', 'w')
        f.write(dumps({"userid": self.storage.conf.userid, "data": self.data}))
        f.close()
        return 0

    def actionupdate(self, action: int, value: bool):
        from time import time
        if action in [0,1,2,3,4]:
            self.data.append([action, value, time()])
            self.datastore()
            if action == 2:
                self.led = value
            elif action == 3:
                self.boil = value
            elif action == 4:
                self.user = value

            return 0
        else:
            raise ValueError('Invalid action')
    
    def sendtoserver(self, action: int, value: bool):
        from json import dumps
        from requests import get

        r = get(self.storage.conf.scoreserver + "/action", json={"userid": self.storage.conf.userid, "action": action, "value": int(value)})
        if r.status_code == 200:
            return 0
        else:
            raise ValueError('Server error')


from flask import *

storage = Storage()
app = Flask(__name__)
app.debug = True

@app.route('/')
def main():
    rtn = request.args
    print(rtn)
    return "1"


@app.route('/worktest')
def pagetest():
    return "It Works!"

@app.route('/test')
def test():
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)