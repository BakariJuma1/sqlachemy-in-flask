from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__='users'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String)
    location = db.Column(db.String)
    date_created = db.Column(db.DateTime,default=datetime.now)

@app.route('/')
def root():
    return 'Flask is running'

@app.route('/<name>/<location>') 
def index(name,location):
    user = User(name=name,location=location)
    db.session.add(user)
    db.session.commit()
    return f"added new user {user.name} from {user.location}"

@app.route('/<name>')
def get_user(name):
    user = User.query.filter_by(name=name).first()
    return f'The user is located in {user.location}'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)