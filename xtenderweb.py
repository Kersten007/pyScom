from flask import Flask, render_template, jsonify, request
import xtender, threading, time


#flask 
app = Flask(__name__)
olist = []

# id , zeit in s
class XPollObjekt(object):
    value = 1.0 #Speicher für die geholten werte
    def __init__(self, id = 0, name = "name", refreshtime = 1.0) -> None:
        self.id = id
        self.name = name
        self.refreshtime = refreshtime
        self.updatetime = time.time()
        self.value = 0.0


#Liste mit zu pollenden Xtender Objekten
def init_poll_list(api):
    olist.append(XPollObjekt(api.INFO_INPUT_VOLTAGE, "Eingangsspannung [AC V]", 5.0))
    olist.append(XPollObjekt(api.INFO_INPUT_CURRENT, "Eingangsstrom [AC A]", 8.0))
    olist.append(XPollObjekt(api.INFO_INPUT_POWER,   "Eingangsleistung [AC W]", 10.0))


def polling_thead():
    Xtender = xtender.Xtender()
    init_poll_list(Xtender.api)    
    while (True):
        i = 0
        while  i < len(olist) :
            o = olist[i]
            if o.updatetime  < time.time():
                o.updatetime = time.time() + o.refreshtime
                o.value = Xtender.conn.read_id(o.id)
                #print(time.time(), o.name, o.refreshtime, o.value , threading.get_ident())
            i += 1
        time.sleep(0.2)



@app.before_first_request
def before_first_request():
    th = threading.Thread(target=polling_thead)
    th.start()
    print ("Thread gestartet")



@app.route('/')
def hello():
    print ("hello")
    print(olist)
    return 'Hello, World!'

@app.route('/status') 
def status():
    return render_template('status.html')


@app.route('/list') 
def list():
    s = ""
    a = []
    b = []
    for obj in olist:
        a.append({"value" : obj.value, "name" : obj.name})
        b.append({"id"+str(obj.id) : {"value" : obj.value, "name" : obj.name}})
        #b.append(obj.id, obj.name)
    return jsonify( b )




@app.route( "/u_eingang" )
def f_u_eingang():
    return jsonify( {"u_eingang": xtender.input.voltage.value} )


@app.route( "/value_by_id" )
def f_value_by_id():
    id =  request.args.get("id", default = 3000, type = int)
    j = "id_" + str(id)
    print(id)
    return jsonify( {j: xtender.read_id(id)} )



if __name__ == '__main__':
    app.run(port=5000, host='192.168.123.35', debug=True)
    pass
    

print("Ende")