#!/usr/bin/python

import os
import sys
import uuid
from random import randint


name = " Usage: EmulkBeacon UUID or random (default=random uuid), major (0-65535, default=0), minor (0-65535, default=0), power (0-255, default=200)"

# return a random UUID
def get_random_uuid():
  return uuid.uuid4().hex

"""eseguo il comando"""
def executeComand(comand):
	os.system(comand)
	print comand

def usage():
	print name
	sys.exit()

# convert an integer into a hex value of a given number of digits
def hexify(i, digits=2):
  format_string = "0%dx" % digits
  return format(i, format_string).upper()
	
# split a hex string into 8-bit/2-hex-character groupings separated by spaces
def hexsplit(string):
  return ' '.join([string[i:i+2] for i in range(0, len(string), 2)])

"""
EBEFD08370A247C89837E7B5634DF524
"""
def main(argv):
	#uuid = "E2 0A 39 F4 73 F5 4B C4 A1 2F 17 D1 AD 07 A9 61"
	uuid = get_random_uuid()
	major = randint(0,65535)
	minor = randint(0,65535)
	power = randint(150,255)
	device = "hci0"
	if len(sys.argv) == 5:
		try:
				
			if str(sys.argv[1]):
				uuid = str(sys.argv[1])
			if str(sys.argv[2]):
				major = str(sys.argv[2])
				if major <0 or major > 65535:
					print "Error: major id is out of bounds (0-65535)"
					sys.exit()
			if str(sys.argv[3]):
				minor = str(sys.argv[3])
				if minor < 0 or minor > 65535:
					print "Error: minor id is out of bounds (0-65535)"
					sys.exit()
			if str(sys.argv[4]):
				power = str(sys.argv[4])
				if power < 0 or power > 255:
					print "Error: power id is out of bounds (0-255)"
					sys.exit()
		except:
			usage()
	elif len(sys.argv) > 1:
		usage()
	
	uuid =  hexsplit(uuid.upper())
	
	major = hexify(major, 4)
	minor = hexify(minor, 4)
	
	major = hexsplit(major)
	minor = hexsplit(minor)
	
	power = hexify(power, 2)
	
	#uuid = "E2 0A 39 F4 73 F5 4B C4 A1 2F 17 D1 AD 07 A9 61"
	print uuid, major, minor, power
	
	executeComand("hciconfig %s up" % device)
	
	executeComand("hciconfig %s leadv" % device)
	
	executeComand("hciconfig %s noscan" % device)
    
	executeComand("hcitool -i %s cmd 0x08 0x0008 1E 02 01 1A 1A FF 4C 00 02 15 %s %s %s %s 00 >/dev/null" % (device, uuid, major, minor, power))
#0x08 0x0008

if __name__ == "__main__":
   main(sys.argv)
