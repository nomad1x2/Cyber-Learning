#!/bin/bash

echo "[ Enter valid IPs/subnets and ports ]"
echo "[ Enter port numbers followed by a space or comma ]"
echo -e "[ If no ports are selected, the default nmap range is chosen ]\n"

#validate ip inpit:
valid_ips=()
while true; do
	read -p "Enter target ip(s): " TARGET_IP
	valid=false
	for ip in $TARGET_IP; do
		#fail fast
		if [[ $ip =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}+(/[0-9]{1,2})?$ ]]; then
			#split using ifs
			IFS='/.' read oct1 oct2 oct3 oct4 cidr <<< "$ip"
			#is valid octets?
			if (( oct1>0 && oct1<=255 && oct2<=255 && oct3<=255 && oct4<=255 )); then
				#does cidr exist and is it valid?
				if [[ -z "$cidr" || ( $cidr =~ ^[0-9]+$ && $cidr -le 32 ) ]]; then
					valid_ips+=("$ip")
					valid=true
				else
					valid=false
				fi
			else
				valid=false
			fi
		else
			valid=false
		fi
	done
	if [[ $valid == true ]]; then
		break
	else
		echo -e "One or more IPs are invalid.\n"
		valid_ips=()
	fi
done

#grab the ports
valid_ports=()
while true; do
	read -rp "Enter target port(s) (optional): " TARGET_PORT
	if [[ -z $TARGET_PORT ]]; then
		break
	#elif [[ ${TARGET_PORT,,} == "all" ]]; then
	#	valid_ports+=("-p-")
	else
		TARGET_PORT=${TARGET_PORT//,/ }
		for port in $TARGET_PORT; do

			#check ranges
			if [[ $port == *-* ]]; then
				IFS='-' read -r start end <<< "$port"
				if [[ $start =~ ^[0-9]+$ && $end =~ ^[0-9]+$ ]] && (( start>0 && end<= 65535 && start<=end )); then
					valid_ports+=("$port")
				else
					echo -e "One or more ports are invalid.\n"
				fi
				continue
			fi

			#check single
			if [[ $port =~ ^[0-9]+$ ]] && (( port>0 && port<=65535 )); then
				valid_ports+=("$port")
			else
				echo -e "One or more ports are invalid.\n"
			fi
		done
	fi
	break
done

if [[ ${#valid_ports[@]} -eq 0 ]]; then
	port_list=""
else
	port_list="-p$(printf "%s\n" "${valid_ports[@]}" | paste -sd, -)"
fi

echo -e "\n[+] Initial scan (host discovery):
 sudo nmap -sn ${valid_ips[*]}

[+] Selected port scan:
 sudo nmap -Pn -n -vv -sT -sV $port_list ${valid_ips[*]}

[+] All port scan:
 sudo nmap -Pn -n -vv -sT -sV -p- ${valid_ips[*]}

[+] Service / default script scan:
 sudo nmap -Pn -n -vv -sT -sV -sC $port_list ${valid_ips[*]}

[+] Service / default script all ports:
 sudo nmap -Pn -n -vv -sT -sV -sC -p- ${valid_ips[*]}

[+] Service / vuln script scan:
  sudo nmap -Pn -n -vv -sT -sV $port_list --script *vuln* ${valid_ips[*]}

[+] Service / vuln script all ports:
  sudo nmap -Pn -n -vv -sT -p- --script *vuln* ${valid_ips[*]}

[+] OS scan:
  sudo nmap -Pn -n -vv -sT -O $port_list ${valid_ips[*]}
"