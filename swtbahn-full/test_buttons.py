#from RPi import GPIO
#import RPi.GPIO as GPIO
#import dothat.touch as touch
import time
from cap1xxx import Cap1166
import copy
print("hello world")

def callbackTouch(channel, event):
	print("Got {} on {}".format(event, channel))

I2C_ADDR = 0x2c

UP = 1
DOWN = 2
LEFT = 3
RIGHT = 5
BUTTON = 4
CANCEL = 0

#_cap1166 = Cap1166(i2c_addr=I2C_ADDR, alert_pin=0x)
_cap1166 = Cap1166(i2c_addr=I2C_ADDR)
_cap1166._write_byte(0x26, 0b00111111)  # Force recalibration

#time.sleep(5.0)

_cap1166.on(channel=UP, event='press', handler=callbackTouch)
_cap1166.on(channel=DOWN, event='press', handler=callbackTouch)
_cap1166.on(channel=LEFT, event='press', handler=callbackTouch)

_cap1166.start_watching()

while True:
    status = copy.deepcopy(_cap1166.get_input_status())
    #print(status)
    time.sleep(0.25)
    status2 = copy.deepcopy(_cap1166.get_input_status())
    
    #if (not status[1] == status2[1]):
    #    print("button 1 changed!")
    #print(status2[1])
    print(status)
    print(status2)
    for i in range(len(status)):
        #print("i: " + str(i) + "; status[i]: " + status[i] + "; status2[i]: " + status2[i])
        if (not status2[i] == status[i]):
            print("Button " + str(i) + " status changed")
        #else:
	    #    print("Button " + str(i) + " same")
    
    print("--------------")
    time.sleep(0.25)
