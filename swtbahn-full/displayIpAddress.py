import time
import traceback
import datetime
import os
import ifaddr
import signal

import dothat.lcd as lcd
import dothat.touch as touch
import dothat.backlight as backlight

networkInterfaceIndex = 0
refreshDisplay = True

# Helper functions
def updateDisplay():
	global refreshDisplay
	if not refreshDisplay:
		return
	lcd.clear()

	# Collect IP information
	adapters = ifaddr.get_adapters()
	ipCollection = []

	for adapter in adapters:
		ipCollection.append([adapter.ips[0].ip, adapter.nice_name])

	# Restrict networkInterfaceIndex to the range of available IPs
	global networkInterfaceIndex
	if networkInterfaceIndex >= len(ipCollection):
		networkInterfaceIndex = 0
	host_ip = None
	host_name = None
	if len(ipCollection) > 0:
		host_name = ipCollection[networkInterfaceIndex][1]
		host_ip = str(ipCollection[networkInterfaceIndex][0])

	if host_ip is None:
		# No IP found
		backlight.rgb(170, 170, 0)
		
		lcd.set_cursor_position(0, 0)
		lcd.write("No IP address")
	else:
		# IP found
		backlight.rgb(140, 170, 170)
		
		# Write IP Information
		lcd.set_cursor_position(0,0)
		lcd.write(host_name)
		lcd.set_cursor_position(0,1)
		lcd.write(host_ip)
		lcd.set_cursor_position(0,2)
		date_time = str(datetime.datetime.now())[:16]
		lcd.write(date_time)

def changeInterface(): 
	global networkInterfaceIndex 
	networkInterfaceIndex += 1

# Display buttons
@touch.on(touch.CANCEL)
def handle_quit(channel, event):
	print("Cancel button pressed")
	backlight.off()
	os.kill(os.getpid(), signal.SIGKILL)

@touch.on(touch.UP)
def touchUp(channel, event):
	print("UP button pressed")
	changeInterface()
	updateDisplay()

@touch.on(touch.DOWN)
def switchToEduroam(channel, event):
	global refreshDisplay
	print("DOWN button pressed")
	refreshDisplay = False
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
	refreshDisplay = True
	updateDisplay()

@touch.on(touch.BUTTON)
def handle_shutdown(channel, event):
	print("BUTTON (shutdown) button pressed")
	lcd.clear()
	backlight.rgb(170, 0, 0)
	lcd.set_cursor_position(1, 1)
	lcd.write("Shutting Down!")
	os.system("sudo shutdown")

def handle_sig_end_display(signum, frame):
	lcd.clear()
	backlight.rgb(0, 0, 0)
	print("Ending displayIpAddress.py")
	exit()

# Main logic below
def main():
	# Register Signal handler for SIGINT and SIGTERM, to shut down the
	# LCD properly when receiving these signals
	signal.signal(signal.SIGINT, handle_sig_end_display)
	signal.signal(signal.SIGTERM, handle_sig_end_display)
	# Main logic
	try:
		backlight.graph_off()
		lcd.set_contrast(50)
		while True:
			# Every 10 seconds, switch display to next IP address
			changeInterface()
			updateDisplay()
			time.sleep(10)
	except:
		print('traceback.format_exc():\n%s',traceback.format_exc())
		exit()

if __name__ == "__main__":
	main()
