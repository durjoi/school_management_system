from flask import Flask
from rabbitmq import create_queue

app = Flask(__name__)

# Creating queue in rabbitmq server
create_queue()


@app.route('/')
def index():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
