import json, pika, traceback

def upload(claims, file, fs, channel):
    try:
        fid = fs.put(file)
     except Exception as e:
        print(e)
        return "Internal Server error", 400

    message = {
        "video_fid": str(fid),
        "username": claims["username"],
        "mp3_fid": None
    }
    try:
        channel.basic_publish(
            exchange="",
            routing_key="video",
            body=json.dumps(message)
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
    except Exception as e:
        fs.delete(fid)
        print(e)
        print(traceback.print_exc()
        return "Internal server error", 500
