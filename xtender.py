#from Xcom_API import Xcom_API
from os import name
from xcom232 import xcom232


__conn = xcom232(port='/dev/ttyUSB0')
api = __conn.api

def read_id(id=0):
    return __conn.read_id(id)

def ac_input_voltage():
    return read_id(api.INFO_INPUT_VOLTAGE)

def ac_output_voltage():
    return __conn.read_id(api.INFO_OUTPUT_VOLTAGE)
