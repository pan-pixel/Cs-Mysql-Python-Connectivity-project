#We are using simple mail transfer protocol
import smtplib
from email.message import EmailMessage

def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to

#one can make the sending email of its own
#you need to activate two step verification and use the app password as the password
#Or simply just use the given ID! Its open for all!! XD
    user = "pollutionucp@gmail.com"
    msg['from'] = user
    password = "cvjhxitjteiairxh"
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(user,password)
    server.send_message(msg)
    print("Message sent succefully!!")
    server.quit()

if __name__ == '__main__':
    email_alert("Hey","Hello World","prathamarora333@gmail.com")
