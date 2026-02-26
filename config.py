import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "secret123"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "instance/students.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False