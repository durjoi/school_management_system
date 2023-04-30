from flask import Flask, render_template
from rabbitmq import create_queue
from module.user.routes import user_bp
from module.subject.routes import subject_bp
from module.classes.routes import class_bp
from module.student.routes import student_bp

app = Flask(__name__)
app.secret_key = 'secret_key'

# Creating queue in rabbitmq server
create_queue()

# routes
app.register_blueprint(user_bp, url_prefix='/')
app.register_blueprint(subject_bp, url_prefix='/')
app.register_blueprint(class_bp, url_prefix='/')
app.register_blueprint(student_bp, url_prefix='/')


@app.route('/')
def index():
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
