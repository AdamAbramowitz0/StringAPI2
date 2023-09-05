import smtplib, ssl

smtpServer = "smtp.gmail.com"
port=587
myEmail="ahabramowitz@gmail.com"

context = ssl.create_default_context()
newemail = """From: From Person ,senderMail@sender.com> 
To: To Person <my_email@gmail.com>
Subject: Email Test
This is the body of the email.
"""
try:
    server = smtplib.SMTP(smtpServer,port)
    server.starttls(context=context)
    server.login(myEmail, password)
except Exception as e:
    print (e)
finally:
    server.quit()
