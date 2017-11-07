#!/usr/bin/python

import alsaaudio, time, audioop
import sys, struct, pymodbus
from pymodbus.client.sync import ModbusTcpClient
from struct import pack, unpack

client = ModbusTcpClient('192.168.1.1')

# Open the device in nonblocking capture mode. The last argument could
# just as well have been zero for blocking mode. Then we could have
# left out the sleep call in the bottom of the loop
inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK)

inp.setchannels(1)
inp.setrate(8000)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)

inp.setperiodsize(160)
tankval = 0
while True:
    l,data = inp.read()
    #bleh = client.write_register(12289,10) # tank fill state
    #bleh = client.write_register(12292,2000) # tank fill state
    if l:
    	soundval = int(audioop.max(data, 2)) / 100
        #print soundval
        tankval = soundval
        if tankval > 50:
          tankval = tankval - 10
        if tankval > 70:
          tankval = tankval - 20
        #print tankval
        turbineval = tankval + 1000 
        turbineval = turbineval * 2.8
        print turbineval
        if turbineval > 3607:
          turbineval = 3607
          if tankval > 100:
            tankval = 100
          
        bleh = client.write_register(12289,tankval) # tank fill state
        bleh = client.write_register(12292,turbineval) # tank fill state
    time.sleep(.005)
