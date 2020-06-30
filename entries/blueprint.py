from flask import Blueprint, render_template, request, flash

from helpers import object_list
from models import Entry, Tag
from entries.forms import EntryForm

# Make blueprints 
entries = Blueprint('entries', __name__, template_folder='templates')

# Helper function for additionaly filter results based on search query - 'q'
def entry_list(template, query, **context):
    results = []
    search = request.args.get('q')
    if search:
        query = query.filter(
            (Entry.body.contains(search)) |
            (Entry.title.contains(search)))
        results = query.all()
        if not results:
            flash(f'There were no matches for your search "{search}".', 'danger')
    return object_list(template, query, **context)


# URL ROUTES
@entries.route('/')
def index():
    entries = Entry.query.order_by(Entry.created_timestamp.desc())
    tags = Tag.query.order_by(Tag.name.asc())
    return entry_list('entries/index.html', entries, title='Jonas Laurinaitis - Blog Posts', tags=tags)

@entries.route('/categories/')
def tag_index():
    tags = Tag.query.order_by(Tag.name.asc())
    return object_list('entries/tag_index.html', tags, title= "Blog Categories")

@entries.route('/category/<slug>/')
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug == slug).first_or_404()
    entries = tag.entries.order_by(Entry.created_timestamp.desc())
    return entry_list('entries/tag_detail.html', entries, tag=tag, title="Blog Category - " + tag.name)

@entries.route('/create/')
def create():
    form = EntryForm()
    return render_template('entries/create.html', form=form, title="Create New Post")

@entries.route('/<slug>/')
def detail(slug):
    entry = Entry.query.filter(Entry.slug == slug).first_or_404()
    return render_template('entries/detail.html', entry=entry, title="Blog Post - " + entry.title)