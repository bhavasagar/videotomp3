import os, pika, gridfs, json
from flask import Flask, request
from flask_pymongo import PyMongo
from auth_svc import access
from auth import validate
from storage import utils

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://host.minikube.internal:27017/videos"

mongo = PyMongo(app)
fs = gridfs.GridFS(mongo.db)

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()

@app.post("/v1/login")
def login():
    print("STARTING LOGIN")
    token, err = access.login(request)
    print(token, err, "Logging data")
    if err:
        return err
    return token, 200

@app.post("/v1/upload")
def upload():
    claims, err = validate.token(request)
    if err:
        return err

    if not claims['admin']:
        return f"You are not allowed to perform this operation", 400

    if len(request.files) != 1:
        return "Please add file or upload one by one", 400

    file = request.files['file']
    if not (file.filename and file.filename.endswith('.mp4')):
        return "Please upload and mp4 formatted file", 400

    err = utils.upload(claims, file, fs, channel)
    if err:
        return err

    return "Uploaded Succesfully", 200

@app.post("/v1/download")
def download():
    pass

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)