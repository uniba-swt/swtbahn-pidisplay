import time
import traceback
import datetime
import os
import ifaddr
import signal

import dothat.lcd as lcd
import dothat.touch as touch
#import dothat.backlight as backlight


networkInterfaceIndex = 0
refreshDisplay = True


# Helper functions
def updateDisplay():
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
#		backlight.rgb(170, 170, 0)
		
		lcd.set_cursor_position(0, 0)
		lcd.write("No IP address")
	else:
		# IP found
#		backlight.rgb(140, 170, 170)
		
		# Write IP Information
		lcd.set_cursor_position(0,0)
		lcd.write(host_name)
		lcd.set_cursor_position(0,1)
		lcd.write(host_ip)
		lcd.set_cursor_position(0,2)
		date_time = str(datetime.datetime.now())[:16] 
		lcd.write(date_time)

def blinkLed():
	#backlight.graph_set_led_duty(0, 1)
	
	while True:
		#backlight.graph_set_led_state(0, 1)
		time.sleep(0.5)
		#backlight.graph_set_led_state(0, 0)
		time.sleep(0.5)

# Display buttons
@touch.on(touch.CANCEL)
def handle_quit(channel, event):
	#backlight.off()
	os.kill(os.getpid(), signal.SIGKILL)

def changeInterface():
        global networkInterfaceIndex
        print("Hallo Bernhard")
        networkInterfaceIndex += 1
        updateDisplay()


@touch.on(touch.UP)
def touchUp(channel, event):
	changeInterface()

@touch.on(touch.DOWN)
def switchToEduroam(channel, event):
	global refreshDisplay
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
	RefreshDisplay = True
	updateDisplay()

@touch.on(touch.BUTTON)
def handle_shutdown(channel, event):
	lcd.clear()
	#backlight.rgb(170, 0, 0)
	lcd.set_cursor_position(1, 1)
	lcd.write("Shutting Down!")
	os.system("sudo shutdown now")

# Main logic below
def main():
	try:
		#backlight.graph_off()
		lcd.set_contrast(50)
		
		while True:
			if refreshDisplay:
				updateDisplay()
			time.sleep(10)
			changeInterface()
	except:
		print('traceback.format_exc():\n%s',traceback.format_exc())
		exit()

if __name__ == "__main__":
	main()
