import smtplib


def sendValidationLink(link, email):
    s = smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()
    s.login('stringapi134@gmail.com',)
    message = "\n VALIDATION EMAIL: " + link

    s.sendmail("stringapi134@gmail.com", email, message)
    s.quit()
    return "SUCESS"
def makeAdamHappy():
    s = smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()
    s.login('stringapi134@gmail.com','')
    message = "Somebody just entered the site!"

    s.sendmail("stringapi134@gmail.com", "ahabramowitz@gmail.com", message)
    s.quit()
    return "SUCESS"
