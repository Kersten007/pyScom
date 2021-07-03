#Modul Xtender, einfach mit import xtender einbinden

#from os import name
from xcom232 import xcom232


__conn = xcom232(port='/dev/ttyUSB0')
api = __conn.api

def read_id(id=0):
    return __conn.read_id(id)

def write_id(self, val):
    pass

class xtender_obj:
    def __init__(self, name = "Objekt Name", id = 0):
        self.name = name
        self.id = id

    @property
    def value(self):
        return read_id(self.id)

    @value.setter
    def value(self, val):
        return write_id(self.id, val)


class __battery:
    temperatur = xtender_obj("Battery temperatur", api.INFO_BATTERY_TEMPERATURE)
    voltage = xtender_obj("Batterie Voltage", api.INFO_BATTERY_VOLTAGE)
    charge_current = xtender_obj("Batterie Charge Current", api.INFO_BATTERY_CHARGE_CURRENT)

class __input:
    voltage = xtender_obj("Battery temperatur", api.INFO_INPUT_VOLTAGE)
    current = xtender_obj("Battery temperatur", api.INFO_INPUT_CURRENT)
    frequency = xtender_obj("Battery temperatur", api.INFO_INPUT_FREQUENCY)

class __output:
    pass

class __state:
    pass

battery = __battery()
input = __input()
output = __output()
state = __state()





