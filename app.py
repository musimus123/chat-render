from flask import Flask, render_template
from flask_socketio import SocketIO, send
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chat.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

socketio = SocketIO(
    app,
    cors_allowed_origins="*"
)

class Mensaje(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contenido = db.Column(db.Text)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("message")
def recibirMensaje(mensaje):

    nuevo = Mensaje(
        contenido=mensaje
    )

    db.session.add(nuevo)
    db.session.commit()

    send(mensaje, broadcast=True)

if __name__ == "__main__":
    socketio.run(
        app,
        host="0.0.0.0",
        port=5000,
        debug=True
    )