from __main__ import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    systems = db.relationship('System', backref='user', lazy=True)

def __repr__(self):
    return '<User %r>' % self.username
