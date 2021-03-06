from flask import render_template, flash, redirect, url_for, abort, request
from app.post import bp
from app import db
from flask_login import login_required, current_user
from app.models import Post, Comment
from app.post.forms import PostForm, CommnetForm


@login_required
@bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommnetForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            comment = Comment(
                comment=form.comment.data,
                post=post,
                author=current_user
            )
            db.session.add(comment)
            db.session.commit()
            flash('You commented on this post!')
            return redirect(url_for('post.post_detail', post_id=post.id))
    comments = post.comments.order_by(Comment.timestamp.desc())
    return render_template('post/detail_post.html', title=post.title, post=post, form=form, comments=comments)


@login_required
@bp.route('/post/new-post', methods=['GET', 'POST'])
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('main.index'))
    return render_template('post/create_post.html', title='New Post', form=form)


@bp.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        db.session.commit()
        flash('Your post has been updated!')
        return redirect(url_for('post.post_detail', post_id=post.id))
    form.title.data = post.title
    form.body.data = post.body
    return render_template('post/create_post.html', title='Update Post', form=form)



@bp.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('You post has been deleted!')
    return redirect(url_for('main.index'))

@bp.route('/post/<int:comment_id>/delete')
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    post = comment.post
    if comment.author != current_user:
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    flash('You comment has been deleted!')
    return redirect(url_for('post.post_detail', post_id=post.id))
