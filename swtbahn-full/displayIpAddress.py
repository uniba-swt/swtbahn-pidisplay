import time
import traceback
import datetime
import os
import ifaddr
from ipaddress import ip_address, IPv4Address


import dothat.lcd as lcd
import dothat.touch as touch
import dothat.backlight as backlight

networkInterfaceIndex = 0
doNotRefreshDisplay = False
apIsOnline = True
apIp = None
eduroamIp = None
def scanWifiIP(ipCollection):
	global apIp, eduroamIp
	for ipString in ipCollection[wlan0]:
		if type(ip_address(ipString) is IPv4Address):
			if ipString[0:2] == "10.":
				apIp = ipString
			else:
				eduroamIp = ipString



def updateDisplay():
	global networkInterfaceIndex, apIp, apIsOnline, eduroamIp
	lcd.clear()


	# Collect information
	adapters = ifaddr.get_adapters()
	ipCollection = []

	for adapter in adapters:
		ipCollection.append([adapter.ips[0].ip, adapter.nice_name])
	
	# Definition of Vars #+defho
		
	host_ip = None
	host_name = None
	date_time = str(datetime.datetime.now())[:16] 
	# Validating the networkInterfaceIndex in Range of IPs
	if networkInterfaceIndex >= len(ipCollection):
		networkInterfaceIndex = 0

	if len(ipCollection) > 0:
		host_name = ipCollection[networkInterfaceIndex][1]
		if networkInterfaceIndex == "wlan0":
			scanWifiIP(ipCollection)
			if apIsOnline:
				host_ip = apIp
			else:
				host_ip = eduroamIp
		else:
			host_ip = str(ipCollection[networkInterfaceIndex][0])

	if host_ip is None:
		# When no ip is found
		backlight.rgb(170, 170, 0)
		
		lcd.set_cursor_position(0, 0)
		lcd.write("No IP address")

	else:
		backlight.rgb(140, 170, 170)

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

@touch.on(touch.DOWN)
def switchToEduroam(channel, event):
	global doNotRefreshDisplay, apIsOnline
	doNotRefreshDisplay = True
	lcd.clear()
	lcd.write("Switching to")
	lcd.set_cursor_position(0,1)
	lcd.write("Eduroam mode")
	os.system("sudo systemctl daemon-reload")
	os.system("sudo service hostapd stop")
	os.system("sudo service dnsmasq stop")
	os.system("sudo service raspapd stop")
	time.sleep(2)
	os.system("sudo wpa_supplicant -i wlan0 -c /etc/wpa_supplicant/wpa_supplicant.conf -B")
	os.system("sudo dhclient wlan0")
	doNotRefreshDisplay = False
	apIsOnline = False
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
		if not doNotRefreshDisplay:
			updateDisplay()
		time.sleep(10)
        
except:
	print('traceback.format_exc():\n%s',traceback.format_exc())
	exit()
