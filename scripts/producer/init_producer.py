import sys
import time
import random
from producer import AProducer


def run():
    mocks = [
        # {
        #     'proto': 'sms',
        #     'contact': '+79997305889',
        #     'message': 'test message from space to m0sk1t phone'
        # },
        {
            'proto': 'email',
            'contact': 'm0sk1t@bk.ru',
            'message': 'test message from space to m0sk1t mail'
        },
        # {
        #     'proto': 'sms',
        #     'contact': '+79158334170',
        #     'message': 'test message from space to artlitvinov phone'
        # },
        {
            'proto': 'email',
            'contact': 'work.litvinov.artem@gmail.com',
            'message': 'test message from space to artlitvinov mail'
        },
    ]
    args = {'host': 'localhost', 'port': '9092'}
    for arg in sys.argv:
        entry = arg.split("=")
        if len(entry) == 2:
            args[str(entry[0])] = str(entry[1])
    a_producer = AProducer(args['host'], args['port'])

    while True:
        message = raw_input("Enter your message: ")
        mock = mocks[random.randint(0, 3)]
        mock["message"] = message
        a_producer.send('test-topic', mock)
        print "your message sent to", mock

if __name__ == "__main__":
    run()
