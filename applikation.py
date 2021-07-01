from time import sleep, time
import xtender

xt = xtender

t = time()

c=1
while True and c<30:
    c = c + 1

    print(xt.ac_output_voltage())

print(time()-t)
