from notifications.send import sender
import pika, os, sys


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="rabbitmq")
    )
    channel = connection.channel()

    def callback(ch, method, properties, body):
        err = sender.notify(body)
        if err:
            ch.basic_nack(delivery_tag=method.delivery_tag)

        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(
        queue=os.environ.get("MP3_QUEUE"),
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