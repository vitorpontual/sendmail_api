import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailSender:

    s = smtplib.SMTP()

    s.connect("smtp.mailtrap.io", 2525)

    s.login("114c4e1e99db01", "70f1ab0aeca10d")

    def send(self, name, email, me):
        print('aqui')
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Recebe o codigo de pedreiro"
        msg['From'] = "No-reply <no-reply@t11.com>"
        msg['To'] = f'{name} <{email}>'

        text = "Envio de email elaborado pelo T11 do treinamento Next para o desafio prático"

        part1 = MIMEText(text, 'plain')

        msg.attach(part1)

        self.s.sendmail(me, email, msg.as_string())
        print("Sent email to " + email, end="")




