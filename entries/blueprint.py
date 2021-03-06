import os
from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from helpers import object_list
from models import Entry, Tag
from app import app, db
from entries.forms import EntryForm

# INIT BLUEPRINTS
entries = Blueprint('entries', __name__, template_folder='templates')


# HELPER FUNCTIONS
# Helper function for additionaly filter results based on search query - 'q'
def entry_list(template, query, **context):
    valid_statuses = (Entry.STATUS_PUBLIC, Entry.STATUS_DRAFT)
    query = query.filter(Entry.status.in_(valid_statuses))
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

# Recheck database for specific entry slug with valid status
def get_entry_or_404(slug):
    valid_statuses = (Entry.STATUS_PUBLIC, Entry.STATUS_DRAFT) 
    return (Entry.query.filter((Entry.slug == slug) & (Entry.status.in_(valid_statuses))).first_or_404())

# Checks if images has right format
def allowed_image(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Entries count of particular tag
def tag_indexing(tags):
    tags_index = []
    for tag in tags:
        # If entries of tag == 0 then delete this tag
        if tag.entries.count() == 0:
            db.session.delete(tag)
        tags_index.append(tag.entries.count())
    db.session.commit()
    while 0 in tags_index:
        tags_index.remove(0)
    return tags_index


# URL ROUTES
@entries.route('/')
def index():
    entries = Entry.query.order_by(Entry.created_timestamp.desc())
    tags = Tag.query.order_by(Tag.name.asc()).all()
    tags_index = tag_indexing(tags)
    return entry_list('entries/index.html', entries,
        title='Jonas Laurinaitis - Blog Posts', tags=zip(tags, tags_index))

@entries.route('/categories/')
def tag_index():
    tags = Tag.query.order_by(Tag.name.asc())
    tags_index = [len(tag.entries.all()) for tag in tags]
    return object_list('entries/tag_index.html', tags, title= "Blog Categories", tags_index=tags_index )

@entries.route('/category/<slug>/')
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug == slug).first_or_404()
    entries = tag.entries.order_by(Entry.created_timestamp.desc())
    return entry_list('entries/tag_detail.html', entries, tag=tag, title="Blog Category - " + tag.name)

# Create
@entries.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        form = EntryForm(request.form)
        if form.validate():
            image_file = request.files['post_image']
            if image_file.filename == '':
                flash('No selected file!', 'danger')
                return redirect(request.url)
            if not allowed_image(image_file.filename):
                flash("Wrong image format! Only 'png', 'jpg', 'jpeg', 'gif' formats.", "danger")
                return redirect(request.url)
            filename_path = os.path.join(app.config['IMAGES_DIR'], secure_filename(image_file.filename))
            image_file.save(filename_path)
            img_url = image_file.filename
            entry = Entry(
                title=form.title.data,
                body=form.body.data,
                image_url=img_url,
                status=form.status.data,
                tags=form.tags.data
                )
            db.session.add(entry)
            db.session.commit()
            flash('Entry "%s" created successfully.' % entry.title, 'success')
            return redirect(url_for('entries.detail', slug=entry.slug))

    else:
        form = EntryForm()
    
    return render_template('entries/create.html', form=form, title="Create New Post")

# POST- detail view   
@entries.route('/<slug>/')
def detail(slug):
    entry = get_entry_or_404(slug)
    return render_template('entries/detail.html', entry=entry, title="Blog Post - " + entry.title)

# Edit
@entries.route('/<slug>/edit/', methods=['GET', 'POST'])
def edit(slug):
    entry = get_entry_or_404(slug)
    if request.method == 'POST':
        form = EntryForm(request.form, obj=entry)
        if form.validate():
            entry.title = form.title.data
            entry.body = form.body.data
            entry.status = form.status.data
            entry.tags = form.tags.data 
            db.session.add(entry)
            db.session.commit()
            flash(f'Entry "{entry.title}" has been saved.', 'success')
            return redirect(url_for('entries.detail',
            slug=entry.slug))
    else:
        form = EntryForm(obj=entry)

    return render_template('entries/edit.html', entry=entry, form=form)

# Delete
@entries.route('/<slug>/delete/', methods=['GET', 'POST'])
def delete(slug):
    entry = get_entry_or_404(slug)
    if request.method == 'POST':
        filename_path = os.path.join(app.config['IMAGES_DIR'], entry.image_url)
        os.remove(filename_path)
        db.session.delete(entry)
        db.session.commit()
        flash('Entry "%s" has been deleted.' % entry.title, 'success')
        return redirect(url_for('entries.index'))
    
    return render_template('entries/delete.html', entry=entry)
 