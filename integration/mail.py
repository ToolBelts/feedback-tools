import smtplib

sender = 'feedback-anonimo@outlook.com'
password = 'dasa@123'  # Password


def send_mail(to_addrs, message):
    recipient = to_addrs
    subject = "[Feedback - Anonimo] - Novo feedback registrado com sucesso"
    text = message

    server = smtplib.SMTP('smtp-mail.outlook.com', 587)
    server.starttls()

    server.login(sender, password)
    message = "Subject: {}\n\n{}".format(subject, text)
    server.sendmail(sender, recipient, message)
    server.close()
