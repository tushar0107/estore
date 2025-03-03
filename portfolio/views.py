from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from .models import Myself
# Create your views here.

import os
from os.path import basename,join
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formatdate

# password  = 'eummrgmlgzgxpdiq'


def getMail(request):
	receiver = request.GET['receiver']
	myself = list(Myself.objects.all())[0]
	res = send_mail(myself.my_email,receiver,myself.subject,myself.mailbody,myself.password,myself.resume)
	if not res:
		return JsonResponse({'message':'An email has been sent to you. Please check your inbox'})
	else:
		return JsonResponse({'message':'I hope you have entered correct email id'})


# email sender function
def send_mail(sender,receiver,subject,body,password,files=None):
	smtp = smtplib.SMTP('smtp.gmail.com',587)
	smtp.starttls()
	smtp.login(sender,password)

	mail = MIMEMultipart()
	mail['Subject'] = subject
	mail['From'] = sender
	mail['To'] = receiver
	mail['Date'] = formatdate(localtime=True)
	mail.attach(MIMEText(body))

	# for f in files:
	part = MIMEBase('application',"octet-stream")
	file_path = str(settings.BASE_DIR)+'/media/'+str(files)
	with open(file_path,"rb") as file:
		part.set_payload(file.read())
	encoders.encode_base64(part)
	part['Content-Disposition'] = 'attachment; filename="%s"' % str(files).split('/')[1]
	mail.attach(part)

	res = smtp.sendmail(sender,receiver,mail.as_string())
	smtp.close()
	return res
