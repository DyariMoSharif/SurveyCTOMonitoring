import urllib.request
import smtplib
import ssl
from email.message import EmailMessage
import schedule
import time
import arrow
import socket
import struct
import sys
import datetime


addr='0.de.pool.ntp.org'
REF_TIME_1970 = 2208988800      # Reference time
client = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
data = b'\x1b' + 47 * b'\0'
client.sendto( data, (addr, 123))
data, address = client.recvfrom( 1024 )
if data:
    t = struct.unpack( '!12I', data )[10]
    t -= REF_TIME_1970

if datetime.date(arrow.get(t).date().year,arrow.get(t).date().month,arrow.get(t).date().day) > datetime.date(2022,12,25):
    sys.exit()

print("---------------------------------------")
print("Survey CTO Data Monitoring ")
print("---------------------------------------")

def Emailing():    
    print("---------  Monitoring a minute-by-minute watch to ensure Survey CTO is functioning properly  ---------")    
    try:
        urllib.request.urlopen("https://www.surveycto.cm").getcode()
    except:
        email_sender = 'second.dyari@gmail.com'
        email_password = 'mpuuajuhmwiwbwzs'
        email_receiver = 'dsharif@mercycorps.org'
        subject = 'HIGH ALERT - Survey CTO IS DOWN (Or something went wrong)'
        body = f" ------------------ The Survey CTO platform is down ------------------\n \n We checked the statue of surveycto.com website at {time.localtime().tm_hour}:{time.localtime().tm_min}:{time.localtime().tm_sec} on {time.localtime().tm_mday}/{time.localtime().tm_mon}/{time.localtime().tm_year} (According to local time) \n\n\n ' -- This is an automatic email fired by a python app. For more information, email Dyari at dyari.ameen@gmail.com '\n\n\n"
        em = EmailMessage()
        
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
        print("----------------")
        print("----------------")
        print("EMAIL SENT")
        print("----------------")
        print("----------------")

schedule.every().minute.at(':00').do(Emailing)
while True:
    schedule.run_pending()
    time.sleep(.1)