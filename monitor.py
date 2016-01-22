import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from requests.auth import HTTPBasicAuth
from datetime import datetime
import time


# The URL_dict stores all the URL's that are to being pinged as a key of the dictionary
# The value of each Key is 0 or 1, where 1 represents email notification has not been sent
# and 0 represents email notification has been sent.
URL_dict = {'https://urcpp.berea.edu':1 ,'https://bcsr.berea.edu':1,'https://cas.berea.edu':1,'https://labor.berea.edu/forms':1}
SEND_TO = 'heggens@berea.edu'


def check_url(url):
	"""
	Takes in an url as a argument, and gets the request for that url
	then compares the status code returned by the server to check if it is ok.
	Returns: A list contatining a boolean that is True if the status is OK, and the status code.
	"""
	r = requests.get(url,  verify=False)	
	result = r.status_code == requests.codes.ok or r.status_code == 401 # we skip 401 because we know the server is not down but auth issue.
	return [result, r.status_code]
		

def send_notification(url, status):
	"""
	sends email with the given url and status to the email address
	set in the global variable SEND_TO
	"""
	payload = {'TO':SEND_TO, 
		'FROM': 'heggens@berea.edu',
		'BCC':'',
		'SUBJECT': "Server is down!!",
		'BODY': str(datetime.now())+": The system " + str(url) + " is down with status: " + str(status),
		'CC': ''}
	r = requests.post('https://54.209.213.107/mailer/mail.php', data=payload, verify=False, auth=('studentlabor', 'DanforthLabor123!'))
	print "NOTIFICATION SENT FOR" + " STATUS: " + str(status) + " AT  URL: " + url


def main():
	# Keep looping to constantly monitory
	while True:
		#loop through all the URLs in the dictionary
		for url in URL_dict.keys():
			result = check_url(url+':443')	# append port at the end of the URL
			# if the URL is bad and email notification not send
			if not result[0] and URL_dict[url]==1:
				send_notification(url, result[1])
				URL_dict[url] = 0
			# if the URL is good and notification is send
			if result[0] and URL_dict[url]==0:
				URL_dict[url] = 1
		time.sleep(120)
main()
