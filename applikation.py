from time import sleep, time
import xtender

t = time()


c=1
while True and c<20:
    c = c + 1

    #print(str(xtender.ac_output_voltage()) + " " + str(xtender.battery_voltage()))

    print(xtender.battery.temperatur.value)
    print(xtender.battery.voltage.value)
    print(xtender.input.voltage.value)

print("")
print(time()-t)
