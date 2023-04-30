from flask import Flask, render_template
from rabbitmq import create_queue
from module.user.routes import user_bp

app = Flask(__name__)
app.secret_key = 'secret_key'

# Creating queue in rabbitmq server
create_queue()

# routes
app.register_blueprint(user_bp, url_prefix='/')


@app.route('/')
def index():
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
