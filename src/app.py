from flask import Flask,jsonify
import datetime
import socket

app = Flask(__name__)


@app.route('/api/v1/info')

def info():
    return jsonify(
        hostName=socket.gethostname(),
        currentTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        message='You are doing great! :3',
        deployed_on='kubernetes',
        app_env='dev',
        app_name='python-app-0'), 200

@app.route('/api/v1/healthz')

def health():
    return jsonify(status='ok'), 200

if __name__ == '__main__':

    app.run(host="0.0.0.0")