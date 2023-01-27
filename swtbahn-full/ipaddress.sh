IP_ADDRESS=$(hostname -I | awk '{print $1}')
while [ "$IP_ADDRESS" = "" ]
do 
 IP_ADDRESS=$(hostname -I | awk '{print $1}')
 IP_ADDRESS2=$(hostname -I | awk '{print $2}')
 sleep 1
done
echo $IP_ADDRESS
echo $IP_ADDRESS2
zenity --info --text="<span font=\"32\"><b>$IP_ADDRESS</b></br><b>$IP_ADDRESS2</b></span>" --title="IP Address"