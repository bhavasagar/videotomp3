import sys
import pika, os
from pymongo import MongoClient
import gridfs
from convert import to_mp3

def main():
    client = MongoClient("host.internal.minikube", 27017)
    db_videos = client.videos
    db_mp3s = client.mp3s
    
    fs_videos = gridfs(db_videos)
    fs_mp3s = gridfs(db_mp3s)
    
    
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="rabbitmq")
    )
    channel = connection.channel()
    
    def callback(ch, method, properties, body):
        err = to_mp3.start(body, fs_videos, fs_mp3s, ch)
        if err:
            ch.basic_nack(delivery_tag=method.delivery_tag)
        
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
        
    channel.basic_consume(
        queue=os.environ.get("VIDEO_QUEUE"),
        on_message_callback=callback
    )
    print("Waiting for messages...")
    channel.start_consuming()
    
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Process intrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)