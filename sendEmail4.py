import smtplib
from email.mime.text import MIMEText
import sys,os

def sendEmail(tgt_email, msg_type, file_name, runtime):
    port = 587

    notify_email_pw = os.environ.get('notify_email_pw')

    sender = 'no-reply@openrig.io'
    receiver = tgt_email

    if msg_type == "submit":

        msg = MIMEText('Your OpenRig job (' + file_name + ') has been submitted')
        msg['Subject'] = 'OpenRig Job submitted'
    else:
        if msg_type == "finish":
            msg = MIMEText('Your OpenRig job (' + file_name + ')  has completed.\nPlease log into your ftp to see the output logfile.\nYour runtime is '+ runtime)
       	    msg['Subject'] = 'OpenRig Job complete'
        else:
            msg = MIMEText('Your OpenRig job (' + file_name + ') had errors. File not found')
       	    msg['Subject'] = 'OpenRig Job failed'
	
    msg['From'] = 'notifications@openrig.io'
    msg['To'] = tgt_email
    user = 'support@openrig.io'
    password = notify_email_pw

    with smtplib.SMTP("mail.privateemail.com", port) as server:
        server.starttls() # Secure the connection
        server.login(user, password)
        server.sendmail(sender, receiver, msg.as_string())
        print("mail successfully sent")

if __name__ == "__main__":
    sendEmail(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

