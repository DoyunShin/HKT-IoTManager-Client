# Client 192.168.50.14 
# Computer, TV, Light, Ondol(Boiler) = 0, 1, 2, 3
# on, off = 1, 0

class Dummy(Exception):
    pass

class Storage(Exception):
    def __init__(self):
        from htmadmin import HTMLFILES
        self.conf = Dummy()
        self.config()
        self.conf.scoreserver = "192.168.50.17"
        self.data = datahandler(self)
        self.html = HTMLFILES(self)

        
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
        
        return 0


class datahandler(Exception):
    def __init__(self, storage):
        self.storage = storage
        self.data = []
        self.led = False
        self.boil = False
        self.dataload()
        pass
    
    def dataload(self):
        from json import load
        f = open('data.json', 'r')
        data = load(f)
        if self.storage.conf.userid != data['userid']:
            raise NameError('Userid is not matched')
        
        self.data = data["data"]
        
        f.close()
        return 0

    def datastore(self):
        from json import dump
        f = open('data.json', 'w')
        f.write(dump({"userid": self.storage.conf.userid, "data": self.data}))
        f.close()
        return 0

    def actionupdate(self, action: int, value: bool):
        if action in [0,1,2,3,4]:
            self.data.append([action, value])
            self.datastore()
            return 0
        else:
            raise ValueError('Invalid action')


from flask import *

app = Flask(__name__)
app.debug = True

@app.route('/')



@app.route('/worktest')
def pagetest():
    return "It Works!"

@app.route('/test')
def test():
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)