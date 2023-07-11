from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
import secrets

app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['UPLOAD_FOLDER'] = 'E:/uplod'
socketio = SocketIO(app)

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

@app.route('/')
def index():
    form = UploadFileForm()
    return render_template('index.html', form=form)

@app.route('/', methods=['POST'])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        return "File has been uploaded."
    return render_template('index.html', form=form)

@socketio.on('message')
def handle_message(data):
    sender = data['sender']
    message = data['message']
    print('received message from ' + sender + ': ' + message)
    emit('message', {'sender': sender, 'message': message}, broadcast=True)

@socketio.on('image')
def handle_image(data):
    sender = data['sender']
    image_data = data['image']
    print('received image from ' + sender)
    emit('image', {'sender': sender, 'image': image_data}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
