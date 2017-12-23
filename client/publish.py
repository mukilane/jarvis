from google.cloud import pubsub_v1
import time

def publish_messages(project, topic_name):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project, topic_name)
    
    for n in range(1, 10):
        data = u'Message number {}'.format(n)
        data = data.encode('utf-8')
        publisher.publish(topic_path, data=data)

    print('Published messages.')

if __name__ == '__main__':
    publish_messages('ok-jarvis', 'rpi')
