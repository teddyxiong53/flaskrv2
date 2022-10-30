

from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from flaskrv2.auth import login_required
from flaskrv2.model import Post, User
from flaskrv2 import db

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    posts = Post.query.all()
    return render_template('blog/index.html', posts=posts)

def get_post(id, check_author=True):
    post = (
        Post.query.join(User, User.id == Post.author_id).get(int(id))
    )
    if post is None:
        abort(404, f"post id {id} not exists")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'title is required'
        if error is not None:
            flash(error)
        else:
            post = Post(title=title, body=body, auhtor_id=g.user['id'])
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/create.html')

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None
        if not title:
            error = 'title is required'
        if error is not None:
            flash(error)
        else:
            post.title = title
            post.body = body
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    Post.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('blog.index'))

