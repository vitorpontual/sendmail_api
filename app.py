import os
import sys

from flask import Flask
from flask import Response, request, jsonify

import sqlalchemy.orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

import json


app = Flask(__name__)
db = declarative_base()

class User(db):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)

    def to_json(self):
        return {"id": self.id, "name": self.name, "email": self.email}



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
    dic_output_msg = {"user": None,
                      "200": "Fim listagem"}
    users_select = db_session.query(User).all()
    dic_output_msg["user"] = [user.to_json() for user in users_select]
    return Response(json.dumps(dic_output_msg))


@app.route("/user/<id>", methods=["GET"])  # SELECT POR ID
def select_user(id):
    db_session = session()
    try:
        dic_output_msg = {"user": None,
                          "200": "Fim listagem"}
        user_select = db_session.query(User).filter_by(id=id).one()
        dic_output_msg["user"] = user_select.to_json()
        return Response(json.dumps(dic_output_msg))
    except Exception as e:
        return jsonify(e)
    finally:
        db_session.close()


# CREATE
@app.route("/user", methods=["POST"])
def create_user():
    db_session = session()
    dic_output_msg = {"user": None,
                      "201": "Cadastro criado com sucesso!"}
    data = request.get_json()
    try:
        user = User(name=data["name"], email=data["email"])
        db_session.add(user)
        db_session.commit()
        dic_output_msg["user"] = user.to_json()
        return Response(json.dumps(dic_output_msg))
    except Exception as e:
        return jsonify(e)
    finally:
        db_session.close()


# UPDATE
@app.route("/user/<id>", methods=["PUT"])
def update_user(id):
    db_session = session()
    dic_output_msg = {"user": None,
                      "200": "Cadastro atualizado com sucesso!"}
    user_update = db_session.query(User).filter_by(id=id).one()
    data = request.get_json()
    try:
        if 'name' in data:
            user_update.name = data['name']
        if 'email' in data:
            user_update.email = data['email']
        db_session.add(user_update)
        db_session.commit()
        dic_output_msg["user"] = user_update.to_json()
        return Response(json.dumps(dic_output_msg))
    except Exception as e:
        return jsonify(e)
    finally:
        db_session.close()


# DELETE
@app.route("/user/<id>", methods=["DELETE"])
def delete_user(id):
    db_session = session()
    dic_output_msg = {"user": None,
            "200": "Cadastro deletado com sucesso"}
    try:
        user_delete = User.query.filter_by(id=id).one()
        dic_output_msg["user"] = user_delete.to_json()
        db_session.delete(user_delete)
        db_session.commit()
        return Response(json.dumps(dic_output_msg))
    except Exception as e:
        return jsonify(e)
    finally:
        db_session.close()


if __name__ == "__main__":
    app.run(debug=True)
