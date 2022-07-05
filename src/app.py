import os
import sys

from flask import Flask
from flask import request, jsonify

import sqlalchemy.orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from .utils import check
from .config import EmailSender
from time import sleep

import json

app = Flask(__name__)
db = declarative_base()
sende = EmailSender()


class User(db):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)

    def to_json(self):
        return {"id": self.id, "name": self.name, "email": self.email}

    def no_id(self):
        return {"name": self.name, "email": self.email}


if not "DATABASE_URL" in os.environ:
    print("DATABASE_URL must be set")
    sys.exit()

db_url = os.environ["DATABASE_URL"]
engine = sqlalchemy.create_engine(db_url)

if not os.path.exists(db_url):
    app.app_context().push()
    print(f"Creating {db_url}")
    db.metadata.create_all(engine)

session = sqlalchemy.orm.sessionmaker(bind=engine)


# READ
@app.route("/user", methods=["GET"])  # SELECT ALL
def select_users():
    db_session = session()
    try:
        dic_output_msg = {"user": None,
                          "message": "Fim listagem"}
        users_select = db_session.query(User).all()
        dic_output_msg["user"] = [user.to_json() for user in users_select]

        return (json.dumps(dic_output_msg), 200)
    except Exception as e:
        return jsonify(e)
    finally:
        db_session.close()


@app.route("/user/<id>", methods=["GET"])  # SELECT POR ID
def select_user(id):
    db_session = session()
    try:
        dic_output_msg = {"user": None,
                          "message": "Fim listagem"}
        user_select = db_session.query(User).filter_by(id=id).one()
        dic_output_msg["user"] = user_select.to_json()
        return (json.dumps(dic_output_msg), 200)
    except Exception as e:
        return jsonify(e)
    finally:
        db_session.close()


# CREATE
@app.route("/user", methods=["POST"])
def create_user():
    db_session = session()
    dic_output_msg = {"user": None,
                      "message": "Cadastro criado com sucesso!"}
    data = request.get_json()
    try:
        user = User(name=data["name"].capitalize(), email=data["email"])
        if check(data["email"]) == "Invalid":
           return ("Formatação do Email Invalida",400)
        try:
            db_session.query(User).filter_by(email=data["email"]).one()
            return ("Email ja cadastrado", 400)
        except:
            pass

        db_session.add(user)
        db_session.commit()
        dic_output_msg["user"] = user.to_json()
        return (json.dumps(dic_output_msg), 201)
    except Exception as e:
        return jsonify(e)
    finally:
        db_session.close()


# UPDATE
@app.route("/user/<id>", methods=["PUT"])
def update_user(id):
    db_session = session()
    dic_output_msg = {"user": None,
                      "message": "Cadastro atualizado com sucesso!"}
    user_update = db_session.query(User).filter_by(id=id).one()
    data = request.get_json()
    try:
        if 'name' in data:
            user_update.name = data['name']
        if 'email' in data:
            if check(data["email"]) != "Invalid":
                return ("Formato do Email Invalido", 400)
            user_update.email = data['email']
        db_session.add(user_update)
        db_session.commit()
        dic_output_msg["user"] = user_update.to_json()
        return (json.dumps(dic_output_msg), 200)
    except Exception as e:
        return jsonify(e)
    finally:
        db_session.close()


# DELETE
@app.route("/user/<id>", methods=["DELETE"])
def delete_user(id):
    db_session = session()
    dic_output_msg = {"user": None,
                      "message": "Cadastro deletado com sucesso"}
    try:
        user_delete = db_session.query(User).filter_by(id=id).one()
        dic_output_msg["user"] = user_delete.to_json()
        db_session.delete(user_delete)
        db_session.commit()
        return (json.dumps(dic_output_msg), 200)

    except Exception as e:
        return jsonify(e)
    finally:
        db_session.close()

@app.route("/sendmail", methods=['POST'])
def sendMail():
    db_session = session()
    try:
        users_select = db_session.query(User).all()
        emails = [user.no_id() for user in users_select]

        for user in emails:
            sleep(0.1)
            email = "T11 <ddesafionext@gmail.com>"
            sende.send(user['name'], user['email'], email)

        return (jsonify("Enviado com sucesso"), 200)
    except Exception as e:
        return jsonify(e)
    finally:
        db_session.close()


@app.route("/sendcustomail", methods=['POST'])
def sendCustom():
    db_session = session()
    try:
        users_select = db_session.query(User).all()
        emails = [user.no_id() for user in users_select]
        data = request.get_json()
        subject = data['subject']
        message = data['message']

        for user in emails:

            sleep(0.1)
            me = "T11 <ddesafionext@gmail.com>"
            sende.send(user['name'], user['email'], me, subject, message)

        return (jsonify("Enviado com sucesso"), 200)
    except:
        return ("Error", 400)
    finally:
        db_session.close()

if __name__ == "__main__":
    app.run(debug=True)
