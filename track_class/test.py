#! /usr/bin/python
import sys
import pickle
import urllib2
import threading
import smtplib

sender = 'atticweng@gmail.com'
receivers = ['atticweng@gmail.com']

message = """From: From attic <atticweng@gmail.com>
To: To attic <atticweng@gmail.com>
Subject: tracking STATs 100A status

The enrollment restriction has been changed for STATS 100A

"""



def monitor():
	threading.Timer(5.0,monitor).start()
	request = urllib2.Request('http://huangshw.desktop.amazon.com:3000/')
	response = urllib2.urlopen(request) # Make the request
	htmlString = response.read()
	htmlString = htmlString.split('title dir=')[1]
	htmlString = htmlString.split('</title>')[0]
	try: 
	    file = pickle.load( open( 'old_status.html', 'rb'))
	    if pickle.load( open( 'old_status.html', 'rb')) == htmlString:
		"""print("Values haven't changed!")"""
		sys.exit(0)
	    else:
		pickle.dump( htmlString, open( 'old_status.html', "wb" ) )  
		try:
			smtpObj = smtplib.SMTP('localhost')
			smtpObj.sendmail(sender, receivers, message)
			smtpObj.sendmail(sender,'5107096677@txt.att.net', message)     
		   	print "Successfully sent email"
		except SMTPException:
			print "Error: unable to send email"
	except IOError: 
	    pickle.dump( htmlString, open( 'old_status.html', "wb" ) )
	    print('Created new file.')

monitor()
