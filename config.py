import smtplib
from app import session, User


def buscar_lista():
    db_session = session()
    try:
        users_select = db_session.query(User).all()
        emails = [user.only_email() for user in users_select]

        for i in range(len(emails)):
            sender = "No Reply <no-replay@t11.com>"
            receiver = emails[i]

            message = f"""\
            Subject: BORA BANDO DE PUTO
            To: {receiver}
            From: {sender}

            BORA JUREMA DOIDA."""

            with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
                server.login("27cff4e234ace5", "2ca0b0863196af")
                server.sendmail(sender, receiver, message)

    except:
        return "deu merda again"


buscar_lista()

