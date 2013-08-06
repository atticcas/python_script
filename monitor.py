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
	request = urllib2.Request('http://www.registrar.ucla.edu/schedule/subdet.aspx?srs=263303210&term=13F&session=')
	response = urllib2.urlopen(request) # Make the request
	htmlString = response.read()
	htmlString = htmlString.split('\"ctl00_BodyContentPlaceHolder_subdet_lblEnrollRestrict\"')[1]
	htmlString = htmlString.split('</span>')[0]
	htmlString = htmlString.split('>')[1]
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
			smtpObj.sendmail(sender,'5107096677', message)     
		   	print "Successfully sent email"
		except SMTPException:
		   print "Error: unable to send email"
	except IOError: 
	    pickle.dump( htmlString, open( 'old_status.html', "wb" ) )
	    print('Created new file.')

monitor()
