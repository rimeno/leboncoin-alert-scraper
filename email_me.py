#!/usr/local/bin/python
# coding: utf-8

import os
import settings

fromaddr = settings.EMAIL_SENDER
password = settings.EMAIL_SENDER_PSWD
toaddr = settings.EMAIL_RECEIVER
mail_server = settings.SERVER_EMAIL_SENDER

def send_email(subject, body):
	from email.mime.multipart import MIMEMultipart
	from email.mime.text import MIMEText

	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = subject

	msg.attach(MIMEText(body, 'plain'))

	import smtplib
	try:
		server = smtplib.SMTP(mail_server, 587)
		server.ehlo()
		server.ehlo()
		server.login(fromaddr, password)
		text = msg.as_string()
		server.sendmail(fromaddr, toaddr, text)
	except smtplib.socket.error:
		print('mail error')
	except smtplib.SMTPException:
		print('mail error')
