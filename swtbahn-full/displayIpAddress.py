#!/usr/bin/env python

import time
import traceback
import socket
import datetime
import os

import dothat.lcd as lcd
import dothat.touch as touch
import dothat.backlight as backlight

def tryGetIPAddress():
	try:
		return socket.gethostbyname(socket.gethostname() + ".local")
	except:
		return 0

@touch.on(touch.BUTTON)
def handle_left(channel, event):
	lcd.clear()
	backlight.rgb(255, 0, 0)
	lcd.set_cursor_position(1, 1)
	lcd.write("Shutting Down!")
	
	global running
	running = False
	os.system("shutdown now")

running = True

try:
	lcd.clear()
	lcd.set_contrast(50)

	
	while (running):
		# Wait for IP-Address
		if not tryGetIPAddress():
			# Draw warning
			backlight.rgb(0, 255, 255)
	
			lcd.set_cursor_position(0, 0)
			lcd.write("No IP address")
		else:
			backlight.rgb(255, 255, 220)
			backlight.single_rgb(0, 255, 0, 0)
			
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
			
		time.sleep(10)
        
except:
	print('traceback.format_exc():\n%s',traceback.format_exc())
	exit()
