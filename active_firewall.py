#!/usr/bin/env python3

import sys
import os
import re

print("Firewall is active")

attack_alerts = ["LAND ATTACK ALERT", "TCP PORT SCAN ALERT", "UDP FLOOD ALERT"]
IP_REGEX = r"(\d{1,3}\.){3}\d{1,3}"
OPTIONAL_PORT_REGEX = r"(:\d{1,5})+"
IP_PORT_REGEX = IP_REGEX + OPTIONAL_PORT_REGEX


def getRule(ip, port, protocol):
	rule = "INPUT " + " -s " + str(ip) + " -j" + " DROP"
	return '' if rule is None else str(rule)

def addRule(allert, sourceIp):
	rule = getRule(sourceIp,'', '')
	print('Adding rule :  '+ rule)
	os.system(f"/sbin/iptables -A {rule}")

def findIpAddress(line):
	matched = re.search(IP_PORT_REGEX + " -> " + IP_PORT_REGEX, line);
	print(matched)
	if matched is not None:
		ipport = matched.group().split(" -> ")[0]
		ip = ip = re.search(IP_REGEX, ipport).group()
		return ip

def activeFirewall(line):

	for allert in attack_alerts:
		if allert in line:
			print('Find attack: ' +  allert)
			sourceIp = findIpAddress(line)
			addRule(allert, sourceIp)

for line in sys.stdin:
	activeFirewall(line)
