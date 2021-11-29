#!/usr/bin/env python

import time
import traceback
import socket
import datetime

import dothat.lcd as lcd

def tryGetIPAddress():
	try:
		return socket.gethostbyname(socket.gethostname() + ".local")
	except:
		return 0

try:
	lcd.clear()
	lcd.set_contrast(50)
	
	# Wait for IP address
	if not tryGetIPAddress():
		# Draw warning
		lcd.set_cursor_position(0,0)
		lcd.write("No IP-Address")
	while not tryGetIPAddress():
		time.sleep(10)

	# Collect information
	host_name = socket.gethostname() 
	host_ip = tryGetIPAddress()
	date_time = str(datetime.datetime.now())[:16] 

	# Display IP information
	lcd.clear()
	lcd.set_cursor_position(0,0)
	lcd.write(host_name)
	lcd.set_cursor_position(0,1)
	lcd.write(host_ip)
	lcd.set_cursor_position(0,2)
	lcd.write(date_time)
        
except:
	print('traceback.format_exc():\n%s',traceback.format_exc())
	exit()
