import datetime
import re
from app import db


# Format title string to url by given expression
def to_url(title):
    return re.sub('[^\w]+', '-', title).lower()


# Defining model - blog entries
class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    slug = db.Column(db.String(100))
    body = db.Column(db.Text)
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    modified_timestamp = db.Column(
        db.DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now)

    def __init__(self, *args, **kwargs):
        super(Entry, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug():
        self.slug = ''
        if self.title:
            self.slug = to_url(self.title)
    
    def __repr__(self):
        return '<Entry: %s>' % self.title
    