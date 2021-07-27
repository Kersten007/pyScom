from flask import Flask, render_template, jsonify, request
import xtender

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/status') 
def status():
    return render_template('status.html')


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

