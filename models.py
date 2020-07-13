from datetime import datetime
import re
import pytz
from app import db

# Format title string to url by given expression
def to_url(title):
    return re.sub('[^\w]+', '-', title).lower()

# Current date var
now = datetime.now()

# Defining intermediary table which reference blog entries with specific tag
entry_tags = db.Table('entry_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('entry_id', db.Integer, db.ForeignKey('entry.id'))
)

# Defining model - blog entries
class Entry(db.Model):
    STATUS_PUBLIC = 0
    STATUS_DRAFT = 1
    STATUS_DELETED = 2

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    slug = db.Column(db.String(100))
    body = db.Column(db.Text)
    image_url = db.Column(db.String(100))
    status = db.Column(db.SmallInteger, default=STATUS_PUBLIC)
    created_timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    modified_timestamp = db.Column(
        db.DateTime,
        default=datetime.utcnow(),
        onupdate=datetime.utcnow())
    
    tags = db.relationship('Tag', secondary=entry_tags,
        backref=db.backref('entries', lazy='dynamic'))

    def __init__(self, *args, **kwargs):
        super(Entry, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        self.slug = ''
        if self.title:
            self.slug = to_url(self.title)

    def __repr__(self):
        return '<Entry: %s>' % self.title

    @property
    def tag_list(self):
        return ', '.join(tag.name for tag in self.tags)

# Defining model for storing tags
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    slug = db.Column(db.String(64), unique=True)

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        self.slug = to_url(self.name)

    def __repr__(self):
        return '<Tag %s>' % self.name



