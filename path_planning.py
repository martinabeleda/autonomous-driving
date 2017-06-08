import urllib2

def baseStation_Commands():
	print "Would you like to recieve the driving commands from base station? (Y/N)"
	while 1:
		inkey = raw_input()
		if inkey is "Y": 
			target_url = "http://54.153.238.139/exp/commands.txt"
			for line in urllib2.urlopen(target_url):
				print line
			break
		if inkey is "N": break

