import os, pika, gridfs, json, base64
from flask import Flask, request, send_file
from flask_pymongo import PyMongo, ObjectId
from auth_svc import access
from auth import validate
from storage import utils

app = Flask(__name__)

video_mongo = PyMongo(app, uri="mongodb://host.minikube.internal:27017/videos")
mp3s_mongo = PyMongo(app, uri="mongodb://host.minikube.internal:27017/mp3s")

video_fs = gridfs.GridFS(video_mongo.db)
mp3s_fs = gridfs.GridFS(mp3s_mongo.db)

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()

@app.post("/v1/login")
def login():
    token, err = access.login(request)
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

    err = utils.upload(claims, file, video_fs, channel)
    if err:
        return err

    return "Uploaded Succesfully", 200

@app.get("/v1/download")
def download():
    if not request.args.get("fid"):
        return "File id is required"
    
    fid = request.args.get("fid")
    try:
        out = mp3s_fs.get(ObjectId(fid))
        return send_file(out, download_name=f"{fid}.mp3")
    except Exception as e:
        print(e)
        return "Internal server error", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)