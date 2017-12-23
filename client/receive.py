import argparse
import time
from google.cloud import pubsub_v1


def parse_message(attributes):
    for attr in attributes:
        print(attributes[attr])

def receive_messages(project, subscription_name):
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project, subscription_name)



    def callback(message):
        print('Received message: {}'.format(message))
        message.ack()
        if message.data == b'GPIO':
            parse_message(message.attributes)

    subscriber.subscribe(subscription_path, callback=callback)

    print('Listening on {}'.format(subscription_path))
    while True:
        time.sleep(100)

if __name__ == '__main__':
    receive_messages('ok-jarvis', 'pavilion')
