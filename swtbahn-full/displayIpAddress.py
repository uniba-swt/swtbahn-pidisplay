import time
import traceback
import datetime
import os
import ifaddr


import dothat.lcd as lcd
import dothat.touch as touch
import dothat.backlight as backlight

networkInterfaceIndex = 0

def updateDisplay():
	global networkInterfaceIndex
	lcd.clear()
	host_ip = None

#		else:
	backlight.rgb(140, 170, 170)
	# Collect information
	adapters = ifaddr.get_adapters()
	ipCollection = []

	for adapter in adapters:
		ipCollection.append([adapter.ips[0].ip, adapter.nice_name])

	host_name = None
	# Validating the networkInterfaceIndex in Range of IPs
	if networkInterfaceIndex >= len(ipCollection):
		networkInterfaceIndex = 0
	if len(ipCollection) > 0:
		host_name = ipCollection[networkInterfaceIndex][1]
		host_ip = str(ipCollection[networkInterfaceIndex][0])
	date_time = str(datetime.datetime.now())[:16] 

	if host_ip is None:
		# When no ip is found
		backlight.rgb(170, 170, 0)
		
		lcd.set_cursor_position(0, 0)
		lcd.write("No IP address")

	else:
		# Write Ip Information
		lcd.set_cursor_position(0,0)
		lcd.write(host_name)
		lcd.set_cursor_position(0,1)
		lcd.write(host_ip)
		lcd.set_cursor_position(0,2)
		lcd.write(date_time)

# Helper functions
def blinkLed():
	backlight.graph_set_led_duty(0, 1)
	
	while (True):
		backlight.graph_set_led_state(0, 1)
		time.sleep(0.5)
		backlight.graph_set_led_state(0, 0)
		time.sleep(0.5)

@touch.on(touch.CANCEL)
def handle_quit(channel, event):
	backlight.off()
	global running
	running = False

@touch.on(touch.UP)
def changeInterface(channel, event):
	global networkInterfaceIndex
	networkInterfaceIndex += 1
	updateDisplay()
	



@touch.on(touch.BUTTON)
def handle_shutdown(channel, event):
	lcd.clear()
	backlight.rgb(170, 0, 0)
	lcd.set_cursor_position(1, 1)
	lcd.write("Shutting Down!")
	
	global running
	running = False
	os.system("shutdown now")


# Main logic below

running = True
try:
	backlight.graph_off()
	lcd.set_contrast(50)

	
	while (running):
		
		updateDisplay()
		time.sleep(10)
        
except:
	print('traceback.format_exc():\n%s',traceback.format_exc())
	exit()

