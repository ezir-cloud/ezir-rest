from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///githubrepo.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICTIONS'] = False
db = SQLAlchemy(app)


class GithubRepo(db.Model):
    JobId = db.Column(db.Integer, primary_key=True)
    JobType = db.Column(db.String(80),  nullable=False)
    CreatedAt = db.Column(db.DateTime, default=datetime.utcnow)
    UpdatedAt = db.Column(db.DateTime)
    JobObject = db.Column(db.String(120), )


    def __repr__(self):
        return '<JobId %r>' % self.JobId