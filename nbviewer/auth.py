import imaplib,re

def check_login_credentials(username, password):
	i = imaplib.IMAP4_SSL('imap.gmail.com')
	try:
		i.login(username,password)
		return True
	except:
		return False
