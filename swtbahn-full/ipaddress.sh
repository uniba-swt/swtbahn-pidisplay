IP_ADDRESS=$(hostname -I | awk '{print $1}')
while [ "$IP_ADDRESS" = "" ]
do 
 IP_ADDRESS=$(hostname -I | awk '{print $1}')
 sleep 1
done
echo $IP_ADDRESS
zenity --info --text="<span font=\"32\"><b>$IP_ADDRESS</b></span>" --title="IP Address"