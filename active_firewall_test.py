#!/usr/bin/env python3

import sys
import os
import re
import subprocess
import io
import datetime


print("Firewall is active")


attack_alerts = [
	"UDP PORT SCAN ALERT",
	"TCP PORT SCAN ALERT", 
	"ICMP FLOOD POSSIBLE ALERT",
	"LAND ATTACK ALERT", 
	"UDP FLOOD ALERT",
	"ICMP FLOOD ALERT",
	"PING OF DEATH ALERT"]

attack_priorities = {
	"UDP PORT SCAN ALERT": 30,
	"TCP PORT SCAN ALERT": 30,
	"ICMP FLOOD POSSIBLE ALERT": 750,
	"LAND ATTACK ALERT": 1500,
	"UDP FLOOD ALERT": 1500,
	"ICMP FLOOD ALERT": 1500,
	"PING OF DEATH ALERT": 1500
}

ips_levels_of_danger = {}

LEVEL_OF_DANGER_TRESHOLD = 1500


IP_REGEX = r"(\d{1,3}\.){3}\d{1,3}"
OPTIONAL_PORT_REGEX = r"(:\d{1,5})*"
IP_PORT_REGEX = IP_REGEX + OPTIONAL_PORT_REGEX

# zwraca liste stringow w formacie:
# [ 'hh:mm', 'hh:mm+1' ]
# pierwsza wartosc to aktualna godzina utc
# druga, to o jedna minute pozniej
def getTimeRangeUTC():
	utcDate = datetime.datetime.utcnow()
	utcDatePlusOneMinute = utcDate + datetime.timedelta(minutes = 2)
	
	dateStringFrom = ""
	dateStringTo = ""	
	
	hour = utcDate.hour
	minute = utcDate.minute
	if hour < 10:
		dateStringFrom = dateStringFrom + "0" + str(hour)
	else:
		dateStringFrom = dateStringFrom + str(hour)
	dateStringFrom = dateStringFrom + ":"
	if minute < 10:
		dateStringFrom = dateStringFrom + "0" + str(minute)
	else:
		dateStringFrom = dateStringFrom + str(minute)
		

	hour = utcDatePlusOneMinute.hour
	minute = utcDatePlusOneMinute.minute
	if hour < 10:
		dateStringTo = dateStringTo + "0" + str(hour)
	else:
		dateStringTo = dateStringTo + str(hour)
	dateStringTo = dateStringTo + ":"
	if minute < 10:
		dateStringTo = dateStringTo + "0" + str(minute)
	else:
		dateStringTo = dateStringTo + str(minute)

	return [dateStringFrom, dateStringTo]

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
	time_range = getTimeRangeUTC()
	time_range_option = " -m time --timestart " +  time_range[0] + " --timestop " + time_range[1]
	rule = "-A INPUT " + "-s " + str(ip)+"/32" + time_range_option +" -j" + " DROP"
	return '' if rule is None else str(rule)


def addRule(allert, sourceIp, rule):
	print('Adding rule: ' + rule)
	command = "/sbin/iptables " + rule
	os.system(command)

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
				if not sourceIp in ips_levels_of_danger:
					ips_levels_of_danger[sourceIp] = 0
				ips_levels_of_danger[sourceIp] += attack_priorities[allert]
				print("IP address: " + sourceIp + " Level of danger: " + str(ips_levels_of_danger[sourceIp]))
				if(ips_levels_of_danger[sourceIp] >= LEVEL_OF_DANGER_TRESHOLD):
					print("IP " + sourceIp + " blocked for one minute due to exceeding level of danger treshold.")
					addRule(allert, sourceIp, rule)
					ips_levels_of_danger[sourceIp] = 0

for line in sys.stdin:
	print(line)
	activeFirewall(line)
