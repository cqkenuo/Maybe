from datetime import datetime
import os

from flask import Blueprint, flash, redirect, render_template, url_for, current_app
from flask_login import login_required

from blog.extensions import upload_markdowns, db
from blog.forms import UpdateForm, VerifyArticleForm
from blog.decorators import admin_required
from blog.models import Article, Category, Tag
from blog.utils import markdown_to_html, save_html


bp = Blueprint('admin', __name__)


@bp.route('/')
@login_required
@admin_required
def index():
    return render_template('admin/admin.html', title='admin-management')


@bp.route('/upload/article', methods=['GET', 'POST'])
@login_required
@admin_required
def upload_article():
    form = UpdateForm()
    if form.validate_on_submit():
        utcnow = datetime.utcnow()
        title = form.title.data
        subfolder = os.path.join(str(utcnow.year), str(utcnow.month))
        markdown_path = os.path.join(current_app.config['MARKDOWN_PATH'], subfolder)
        html_path = os.path.join(current_app.config['HTML_PATH'], subfolder)
        filename = title

        upload_markdowns.save(form.markdown.data, folder=subfolder, name=filename + '.md')
        url = os.path.join('article', subfolder, title)

        article = Article(
            title=title,
            category=Category.query.filter_by(id=form.category.data).first(),
            markdown_path=markdown_path,
            html_path=html_path,
            filename=filename,
            add_time=utcnow,
            url=url)
        for t in form.tag.data.split(','):
            tag = Tag.query.filter_by(name=t).first()
            if not tag:
                tag = new_tag(t)
            article.tags.append(tag)

        db.session.add(article)
        db.session.commit()

        flash('Article uploaded.', 'success')

        return redirect(url_for('admin.index'))
    return render_template('admin/upload_article.html', form=form)


def new_tag(t):
    tag = Tag(name=t)
    db.session.add(tag)
    db.session.commit()
    return tag


@bp.route('/verify')
@login_required
@admin_required
def verify_articles():
    unverified = Article.query.filter_by(verified=False).all()
    verified = Article.query.filter_by(verified=True).all()
    return render_template('admin/verify_articles.html', unverified=unverified, verified=verified)


@bp.route('/verify/article/<int:article_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def verify_article(article_id):
    # 可扩展为在线编辑
    article = Article.query.filter_by(id=article_id).first()
    article_body = markdown_to_html(article.markdown_path, article.filename)
    temporary_path = current_app.config['TEMPORARY_HTML_PATH']
    temporary_name = current_app.config['TEMPORARY_HTML_NAME']
    save_html(article_body, temporary_path, temporary_name, verifying=True)
    form = VerifyArticleForm()
    if form.validate_on_submit():
        utcnow = datetime.utcnow()
        article.verified = True
        article.verified_time = utcnow
        db.session.add(article)
        db.session.commit()

        save_html(article_body, article.html_path, article.filename)
        return redirect(url_for('admin.verify_articles'))
    return render_template('generated/temporary.html', article_body=article_body, form=form)
