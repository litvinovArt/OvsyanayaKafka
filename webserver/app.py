import os
import time
from producer import Producer

from cassandra.cluster import Cluster
from flask import Flask, jsonify, redirect, request, render_template


KAFKA_HOST = os.environ['KAFKA_HOST']
CASSANDRA_HOST = os.environ['CASSANDRA_HOST']
WEBSERVER_PORT = os.environ['WEBSERVER_PORT']

def create_app():
    app = Flask(__name__)
    producer = Producer(KAFKA_HOST, '9092')
    cluster = Cluster([CASSANDRA_HOST])
    session = cluster.connect('users')

    @app.route('/')
    @app.route('/index')
    def index():
        return render_template('index.html', title='Create user')

    @app.route('/sender')
    def sender():
        return render_template('sender.html', title='Send message')

    @app.route('/user/<id>', methods=['GET'])
    def user(id):
        users = []
        session.execute('USE users')
        if id == "all":
            rows = session.execute("SELECT * FROM users")
            for row in rows:
                users.append({
                    'uid': row.uid,
                    'name': row.name,
                    'type': row.type,
                    'contact': row.contact,
                })
            return jsonify(users)
        else:
            user = session.execute("SELECT * FROM users WHERE uid='%s'" % (id))[0]
            return jsonify({
                'uid': user.uid,
                'name': user.name,
                'type': user.type,
                'contact': user.contact,
            })

    @app.route('/user', methods=['POST'])
    def create_user():
        req = request.json
        session.execute('USE users')
        uid = str(int(round(time.time() * 1000)))
        print session.execute("INSERT INTO users (uid, name, type, contact) VALUES (%s, %s, %s, %s)", (uid, req["name"],  req["type"], req["contact"]))
        return uid

    @app.route('/send', methods=['POST'])
    def send_message():
        req = request.json
        session.execute('USE users')
        mid = str(int(round(time.time() * 1000)))
        print session.execute("INSERT INTO messages (mid, uid, date, text, status) VALUES (%s, %s, %s, %s, %s)", (mid, req["uid"],  str(time.time()), req["message"], "sending"))
        producer.send('test-topic', mid)
        return mid

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=WEBSERVER_PORT host='0.0.0.0')