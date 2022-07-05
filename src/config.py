import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailSender:

    ssl_context = ssl.create_default_context()

    s = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl_context)

    #s.connect("smtp.mailtrap.io", 2525)


    #s.login("114c4e1e99db01", "70f1ab0aeca10d")
    s.login("ddesafionext@gmail.com", "umapxoajunalbnvb")

    #s.starttls()


    def send(self, name, email, me, subject="Recebe o codigo de pedreiro", message="Envio de email elaborado pelo T11 do treinamento Next para o desafio prático"):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        #msg['From'] = "No-reply <no-reply@t11.com>"
        msg['From'] = "T11 <ddesafionext@gmail.com>"
        msg['To'] = f'{name} <{email}>'
        print(msg)

        text = f'''{name}, \n{message}'''

        part1 = MIMEText(text, 'plain')

        msg.attach(part1)
        print(msg)

        print("Sent email to " + email, end=" ")
        self.s.sendmail(me, email, msg.as_string())




