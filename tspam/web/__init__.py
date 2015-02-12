import smtplib

def send_email(to_address, message, subject="Info", from_address="asingh@taunton.com"):
    _user="beforebetabot@gmail.com"
    _password='123dfvlabs'
    _to = None
    if isinstance(to_address, list):
        _to = to_address
    else:
        _to = [to_address]
    # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(_user,_password)
    server.sendmail(from_address, _to, 'Subject: %s\n\n%s' % (subject, message))
    server.quit()
