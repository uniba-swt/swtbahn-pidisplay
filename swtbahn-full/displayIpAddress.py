#!/usr/bin/env python

import time
import traceback
import socket
import datetime
import os

import dothat.lcd as lcd
import dothat.touch as touch
import dothat.backlight as backlight


# Helper functions

def tryGetIPAddress():
	try:
		return socket.gethostbyname(socket.gethostname() + ".local")
	except:
		return 0

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
		lcd.clear()

		# Wait for IP-Address
		if not tryGetIPAddress():
			# Draw warning
			backlight.rgb(170, 170, 0)
			
			lcd.set_cursor_position(0, 0)
			lcd.write("No IP address")
		else:
			backlight.rgb(140, 170, 170)
			
			# Collect information
			host_name = socket.gethostname() 
			host_ip = tryGetIPAddress()
			date_time = str(datetime.datetime.now())[:16] 
			
			# Display IP information
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
