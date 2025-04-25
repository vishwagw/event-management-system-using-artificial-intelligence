# libs
import schedule
import time
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# python files:
import QR_scan
import empty_slot_detect
import b

class Static_variable: #creating a static variable
    count_hour = 0

class scheduling_remainders:# to remind the user everyhour abt his parking
    def __init__(self):
        self.data = "Your car been parked for %d hours! just a reminder\n"%(Static_variable.count_hour)
    def job(self):
        #send this in mail
        temp = Mailing(self.data)
        temp.send_mail()
    def schedule(self,job):#job is the function to be scheduled again and again
        if Static_variable.count_hour==0: #so that first time it doesnt take one hour to print out the hourly counter
            job()
        Static_variable.count_hour+=1
        schedule.every(1).hour.do(job)
        while True:  #becomes false once the user takes out the car
            schedule.run_pending()
            time.sleep(1)

# for sending the final destination, path, to travel and so on.
class Mailing:
    def __init__(self,data):
        self.data=data
        self.message_body = "  " #initially the body should have no messages
    def send_mail(self):
        try:
            server = smtplib.SMTP("smtp.gmail.com",587)  # we are trying to create a session with gmail server
            server.starttls()  #we are trying to set up a transport layer security system to encrypt the mails being sent   #security feature
            server.login("danceboyyaya@gmail.com","chandra69chandra") #email ans password of host server which ll send the mails and config1 contains it
            self.message_body = self.data
            server.sendmail("danceboyyaya@gmail.com",price[-1][-2],self.message_body) #config 2 python file has email of users
            print("if it came till here then message sent successfully\n")
            #terminating the server now
            server.quit()
        except smtplib.SMTPConnectError as s:
            print(s)

class image_mail:
    def __init__(self, receiver_mail):
        self.receiver_mail = receiver_mail
    def send_image(self):
        email = ''
        password = ''
        send_to_email = self.receiver_mail
        subject = 'parking details'
        message = 'From ---'
        file_location = 'out.jpg'
        msg = MIMEMultipart()
        msg ['To'] = send_to_email
        msg['subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        filename = os.path.basename(file_location)
        attachment = open(file_location, 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        msg.attach(part)
        server = smtplib.SMTP('gmail', 587)
        server.starttls()
        server.login(email, password)
        text = msg.as_string()
        server.sendmail(email, send_to_email, text)
        server.quit()
    
inp = 1
if inp:
    print('SCAN QR')
    output = QR_scan.scan().stri('b')
    price = b.check(output)
    print("This is price : ", price[0])
    if price [0] == 1:
        empty_slot_detect.empty()
        try:
            user_image = image_mail(price[-1][-2])
            user_image.send_image
            user_schedule = scheduling_remainders()
            user_schedule.schedule(user_schedule.job())
        except : 
            pass
    elif price[0] > 1:
        user_money = Mailing(str(int(print[0])))
        user_money.send_mail()
        print("Thanks for using our service")
    else:
        print("You haven't subscribed\n")



    
