__author__ = 'Dell'

from django.core.mail import send_mail

def getResetMessage(username,link):
    resetMessage = '''
Dear %s,
    You can reset your password by clicking on the link below.
http://127.0.0.1:8000/%s
If you have any problems, please contact us at info.ewallet@gmail.com
Thanks

                                                    e-Wallet
'''% (username, link )
    return resetMessage



ADMIN = 'info.ewallet@gmail.com'

def sendEmail(subject, message, mailingList = []):

    if mailingList:
        send_mail(
            subject,
            message,
            'mailer.ewallet@gmail.com',
            mailingList,
        )
        return True
    return False