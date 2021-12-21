import smtplib, ssl
import random

def send_email(email):
	port = 465 
	password = ''


	sender_email = ''
	receiver_email = email
	verification_code = random.randint(1000, 10000)
	message = """\
	Subject: Email Verification

	This message is sent automatically. Do not reply to this message.
	Your verification code is {0}. Write this number in the application.
	Do not send this code to anybody!""".format(verification_code)


	# Create a secure SSL context
	context = ssl.create_default_context()

	with smtplib.SMTP_SSL('smtp.gmail.com', port, context = context) as server:
		server.login(sender_email, password)
		server.sendmail(sender_email, receiver_email, message)

	return verification_code

def check_verification_code(correct_code, input_code):

	try:
		
		if int(correct_code) == int(input_code):
			return True
		else:
			return False
	
	except:

		return False