IP_ADDRESS1=$(hostname -I | awk '{print $1}')
IP_ADDRESS2=$(hostname -I | awk '{print $2}')
while [ "$IP_ADDRESS1" = "" ]
do 
 IP_ADDRESS1=$(hostname -I | awk '{print $1}')
 IP_ADDRESS2=$(hostname -I | awk '{print $2}')
 sleep 1
done
echo $IP_ADDRESS1
echo $IP_ADDRESS2
zenity --info --text="<span font=\"32\"><b>$IP_ADDRESS1</b> <b>$IP_ADDRESS2</b></span>" --title="IP Addresses"