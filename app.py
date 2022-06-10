import os
import sys
from flask import Flask
import sqlalchemy.orm
from sqlalchemy import Column, Integer, String, Boolean


app = Flask(__name__)

db = sqlalchemy.orm.declarative_base()


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
@app.route("/users", methods=["GET"])  # SELECT ALL
def select_users():
    dic_output_msg = {"user": None,
                      "200": "Fim listagem"}
    users_select = User.query.all()
    dic_output_msg["user"] = [user.to_json() for user in users_select]
    return Response(json.dumps(dic_output_msg))


@app.route("/user/<id>", methods=["GET"])  # SELECT POR ID
def select_user(id):
    dic_output_msg = {"user": None,
                      "200": "Fim listagem"}
    user_select = User.query.filter_by(id=id).first()
    dic_output_msg["user"] = user_select.to_json()
    return Response(json.dumps(dic_output_msg))


# CREATE
@app.route("/user", methods=["POST"])
def create_user():
    dic_output_msg = {"user": None,
                      "201": "Cadastro criado com sucesso!"}
    try:
        data = request.get_json()
        user = User(name=data["name"], email=data["email"])
        db.session.add(user)
        db.session.commit()
        dic_output_msg["user"] = user.to_json()
        return Response(json.dumps(dic_output_msg))
    except:
        return Response(json.dumps("400 Erro ao criar cadastro"))


# UPDATE
@app.route("/user/<id>", methods=["PUT"])
def update_user(id):
    dic_output_msg = {"user": None,
                      "200": "Cadastro atualizado com sucesso!"}
    user_update = User.query.filter_by(id=id).first()
    data = request.get_json()
    try:
        if 'name' in data:
            user_update.name = data['name']
        if 'email' in data:
            user_update.email = data['email']
        db.session.add(user_update)
        db.session.commit()
        dic_output_msg["user"] = user_update.to_json()
        return Response(json.dumps(dic_output_msg))
    except:
        return Response(json.dumps("400 Erro ao atualizar cadastro"))


# DELETE
@app.route("/user/<id>", methods=["DELETE"])
def delete_user(id):
    dic_output_msg = {"user": None,
            "200": "Cadastro deletado com sucesso"}
    try:
        user_delete = User.query.filter_by(id=id).first()
        dic_output_msg["user"] = user_delete.to_json()
        db.session.delete(user_delete)
        db.session.commit()
        return Response(json.dumps(dic_output_msg))
    except:
        return Response(json.dumps("400 Erro ao deletar cadastro"))


if __name__ == "__main__":
    app.run(debug=True)
