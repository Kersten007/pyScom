#from xcom_232i import XcomRS232
from xcom_232i import constants as c

from xcom_232i.XcomRS232 import RS232_IO

#IO = XcomRS232(socket_device='/dev/ttyUSB0', baudrate=115200)

IO = RS232_IO(socket_device='/dev/ttyUSB0', baudrate=115200)

lademodus = "" #IO.get_value(c.OPERATION_MODE)
batt_phase = "" #IO.get_value(c.BAT_CYCLE_PHASE)
solarleistung = "" #IO.get_value(c.PV_POWER) * 1000 # convert from kW to W
sonnenstunden = "" #IO.get_value(c.NUM_SUN_HOURS_CURR_DAY)
ladestand = "" #IO.get_value(c.STATE_OF_CHARGE) # in %
stromprod = "" #IO.get_value(c.PROD_ENERGY_CURR_DAY)
batt_strom = "" #IO.get_value(c.BATT_CURRENT)
batt_spann = IO.get_value(c.AC_IN_VOLTAGE) # IO.get_value(c.BATT_VOLTAGE)

print(f"LModus: {lademodus} | Batt_Phase: {batt_phase} | Solar_P: {solarleistung} | SonnenH: {sonnenstunden} | Batt_V: {batt_spann} | SOC: {ladestand}")


