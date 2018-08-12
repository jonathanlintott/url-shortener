from datetime import datetime

from application import db


class UrlPair(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    original_url = db.Column(db.Text(), nullable=False)
    shortened_url = db.Column(db.String(32), nullable=False,
                              index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow,
                          nullable=False)
