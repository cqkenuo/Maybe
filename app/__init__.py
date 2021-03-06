#
# -*- coding: utf-8 -*-
#
# @Author: Arrack
# @Date:   2020-05-25 18:21:49
# @Last modified by:   Arrack
# @Last Modified time: 2020-06-11 11:25:26
#

import click

from flask import Flask

from app.extensions import db
from app.extensions import lm
from app.models import Role
from app.models import User
from test.fake import Fake

from config import config


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    register_blueprint(app)
    register_extensions(app)
    register_command(app)

    return app


def register_extensions(app):
    db.init_app(app)
    lm.init_app(app)


def register_blueprint(app):
    from app.views import main
    app.register_blueprint(main.bp)
    from app.views import admin
    app.register_blueprint(admin.bp, url_prefix='/admin')


def register_command(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        if drop and click.confirm('This operation will delete the database, do you want to continue?'):
            db.drop_all()
            click.echo('All tables have been dropped.')
        db.create_all()
        click.echo('Initialized database.')
        Role.initRoles()
        click.echo('Initialized Roles.')
        User.initAdmin()
        click.echo('Initialized an Admin.')

    @app.cli.command()
    @click.option('--cates', is_flag=True, help='Fake talks.')
    @click.option('--tags', is_flag=True, help='Fake talks.')
    @click.option('--talks', is_flag=True, help='Fake talks.')
    @click.option('--articles', is_flag=True, help='Fake talks.')
    def fake(cates, tags, talks, articles):
        fake = Fake()
        if cates:
            count = fake.cates()
            click.echo('Initialized %d fake cates.' % count)
        if tags:
            count = fake.tags()
            click.echo('Initialized %d fake tags.' % count)
        if articles:
            count = fake.articles()
            click.echo('Initialized %d fake articles.' % count)
        if talks:
            count = fake.talks()
            click.echo('Initialized %d fake talks.' % count)
        if not any([cates, tags, talks, articles]):
            count = fake.cates()
            click.echo('Initialized %d fake cates.' % count)
            count = fake.tags()
            click.echo('Initialized %d fake tags.' % count)
            count = fake.articles()
            click.echo('Initialized %d fake articles.' % count)
            count = fake.talks()
            click.echo('Initialized %d fake talks.' % count)
