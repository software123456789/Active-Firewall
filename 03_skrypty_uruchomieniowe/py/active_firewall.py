#!/usr/bin/env python3

import sys
import os
import re
import subprocess
import io

print("Firewall is active")

attack_alerts = ["LAND ATTACK ALERT", "TCP PORT SCAN ALERT", "UDP FLOOD ALERT"]
IP_REGEX = r"(\d{1,3}\.){3}\d{1,3}"
OPTIONAL_PORT_REGEX = r"(:\d{1,5})+"
IP_PORT_REGEX = IP_REGEX + OPTIONAL_PORT_REGEX

def checkDangerIpBlocked(rule):
	proc = subprocess.Popen(['iptables-save'], stdout=subprocess.PIPE)
	match = False
	for line in io.TextIOWrapper(proc.stdout, encoding="utf-8"):
		if not line:
			break
		match = (rule in line)

		if match:
			break

	return match

def getRule(ip, port, protocol):
	rule = "-A INPUT " + "-s " + str(ip)+"/32" + " -j" + " DROP"
	return '' if rule is None else str(rule)

def addRule(allert, sourceIp, rule):
	print('Adding rule: ' + rule)
	os.system(f"/sbin/iptables {rule}")

def findIpAddress(line, num):
	matched = re.search(IP_PORT_REGEX + " -> " + IP_PORT_REGEX, line);
	if matched is not None:
		ipport = matched.group().split(" -> ")[num]
		ip = ip = re.search(IP_REGEX, ipport).group()
		return ip

def activeFirewall(line):
	for allert in attack_alerts:
		if allert in line:
			print('Find attack: ' +  allert)
			sourceIp = findIpAddress(line,0)
			destIp = findIpAddress(line,1)
			rule = getRule(sourceIp,'', '')
			if not checkDangerIpBlocked(rule):
				addRule(allert, sourceIp,rule)

for line in sys.stdin:
	activeFirewall(line)
