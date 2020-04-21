#!/usr/bin/env python3

import sys

print("Firewall is active")

attack_alerts = ["LAND ATTACK ALERT", "TCP PORT SCAN ALERT", "UDP FLOOD ALERT"]

def addRule(allert):
	print('Adding rule: ' + allert)

def activeFirewall(line):

	for allert in attack_alerts:
		if allert in line:
			print('Find attack: ' +  allert)
			addRule(allert)


for line in sys.stdin:
	activeFirewall(line)
