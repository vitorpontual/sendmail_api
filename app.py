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
    password = Column(String(40), nullable=False)
    activated = Column(Boolean, default=False)
    hash = Column(String(100))


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


if __name__ == "__main__":
    app.run(debug=True)
