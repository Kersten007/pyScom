from flask import Flask, render_template, jsonify, request
import xtender, threading, time
import json

#flask 
app = Flask(__name__)
olist = []

# id , zeit in s
class XPollObjekt(object):
    value = 1.0 #Speicher für die geholten werte
    def __init__(self, id = 0, name = "name", unit = "", refreshtime = 1.0) -> None:
        self.id = id
        self.name = name
        self.unit = unit
        self.refreshtime = refreshtime
        self.updatetime = time.time()
        self.value = 0.0


#Liste mit zu pollenden Xtender Objekten
def init_poll_list(api):
    olist.append(XPollObjekt(api.INFO_INPUT_VOLTAGE, "Eingangsspannung","V", 5.0))
    olist.append(XPollObjekt(api.INFO_INPUT_CURRENT, "Eingangsstrom","A", 8.0))
    olist.append(XPollObjekt(api.INFO_INPUT_POWER,   "Eingangsleistung","W", 10.0))
    olist.append(XPollObjekt(api.INFO_BATTERY_VOLTAGE, "Batteriespannung","V", 10.0))
    olist.append(XPollObjekt(api.INFO_OUTPUT_POWER, "Ausgangsleistung","W", 5.0))
    olist.append(XPollObjekt(api.INFO_OUTPUT_CURRENT, "Ausgangsstrom","A", 5.0))
    olist.append(XPollObjekt(api.INFO_STATE_OF_OUTPUT_RELAY, "Status Ausgangsrelais","on/off", 60.0))
    olist.append(XPollObjekt(api.INFO_STATE_OF_TRANSFER_RELAY, "Status Tranferrelais","on/off", 60.0))


'''
    printf("Inverter allowed  \t1124 = %d, Prohibits = %d\n", read_bool(1124,""), read_bool(1539,""));                               
    printf("Charger allowed   \t1125 = %d, Prohibits = %d\n", read_bool(1125,""), read_bool(1540,""));     
    printf("Boost allowed      \t1126 = %d, Prohibits = %d\n", read_bool(1126,""), read_bool(1541,""));                               
    printf("Transfer allowed   \t1128 = %d, Prohibits = %d\n", read_bool(1128,""), read_bool(1538,"")); 
    printf("Battery priority   \t1296 = %d, Prohibits = %d\n", read_bool(1296,""), read_bool(1579,""));
    read_bool(1155,"Absorbtion allowed \t1155 = %x\n"); 


    read_float(1138,"Battery charge current \t1138 = %.2f A\n"); 
    read_float(1108,"Battery undervoltage  \t1108 = %.2f V\n");    
    read_float(1110,"Restart undervoltage  \t1110 = %.2f V\n");             
    read_float(1109,"Battery undervo load  \t1109 = %.2f V\n");  
    read_float(1121,"Max Bat- Voltage  \t1121 = %.2f V\n");                             
    read_float(1140,"Floating Voltage  \t1140 = %.2f V\n");
    read_float(1143,"Battery Voltage level 1\t1143 = %.2f V\n");                
    read_float(1145,"Battery Voltage level 2\t1145 = %.2f V\n");               
    read_float(1164,"Egalisierungs- Voltage \t1164 = %.2f V\n");        
    read_float(1156,"Absorption Voltage  \t1156 = %.2f V\n");
    read_float(1172,"Reduced floating volt \t1172 = %.2f V\n");                      
    bat_prio_v = read_float(1297,"Battery prio voltage \t1297 = %.2f V\n");



    read_float(1143,"Voltage level 1   \t1143 = %.2f V\n"); 
    read_float(1144,"Dauer Unterspannung \t1144 = %.2f min\n");                 
    read_float(1187,"Standby level     \t1187 = %.2f %\n");         
    

    //read_float(1286,"AC Output voltage \t1286 = %.2f V\n"); 
    read_float(1107,"Maximum AC current \t1107 = %.2f A\n");
    read_float(1138,"Battery charge current \t1138 = %.2f A\n");
    read_float(1607,"Limitation Power Boost \t1607 = %.2f A\n");      


    // Fernsteuereingang geht 23.03.20
    read_long_enum(1202,"Operating mode (AUX 1) \t1202 = %ld\n"); // def: auto = 1, 
    read_bool(1578,"Remote Activated by AUX 1 \t1578 = %d\n"); // state, 1=on
    read_bool(1543,"Remote entry (AUX 1) active \t1543 = %d\n"); //
    read_long_enum(1545,"Remote Aktivierungsmodus \t1545 = %ld\n"); //, Fernsteuereingang  def:open:1/closed:0
    read_float(1255, "Bat voltage deact.(AUX 1)\t1255 = %.2f V\n");
    read_float(1247, "Battery voltage 1 act. (AUX 1)\t1247 = %.2f V\n");
    read_float(1250, "Battery voltage 2 act. (AUX 1)\t1250 = %.2f V\n");

'''








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
    time.sleep(1)
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
    b = {}
    for obj in olist:
        b.update({"id"+str(obj.id) : {"value":obj.value,"name":obj.name,"unit":obj.unit}})
    return jsonify(b)


@app.route( "/u_eingang" )
def f_u_eingang():
    return jsonify( {"u_eingang": olist[0].value} )


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