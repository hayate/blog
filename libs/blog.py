# -*- coding: utf-8 -*-

import os
import uuid
import json
import redis
import bottle
import httplib
from bottle import view
from bottle import Bottle
from bottle import request
from bottle import redirect
from wsgisession import Session
from wsgisession import SessionMiddleware


class RedisSessionFactory(object):
    def __init__(self):
        self.r = redis.StrictRedis()

    def load(self, id=None):
        session = Session()
        if id is None:
            id = uuid.uuid1()
        try:
            data = self.r.get(id)
            if data is not None:
                session.data = json.loads(data)
            session.id = id
        except:
            pass
        return session

    def save(self, session):
        if session.id is not None:
            if self.r.set(session.id, json.dumps(session.data)):
                ttl = self.r.ttl(session.id)
                if ttl < 0:
                    self.r.expire(session.id, 300)
        return session.id


class Blog(Bottle):
    def __init__(self, catchall=True, autojson=True):
        super(Blog, self).__init__(catchall, autojson)
        for path in bottle.TEMPLATE_PATH:
            print(os.path.abspath(path))
        self.app = SessionMiddleware(self.wsgi,
                                     RedisSessionFactory(),
                                     'session')

    def __call__(self, environ, start_response):
        # strip trailing slashes
        environ['PATH_INFO'] = environ['PATH_INFO'].rstrip('/')
        return self.app(environ, start_response)

App = Blog()


@App.get('/admin')
def admin():
    if request.environ['session'].get('user') is None:
        redirect('/login', httplib.FOUND)


@App.get('/login')
@view('login')
def login():
    if request.environ['session'].get('user') is not None:
        redirect('/admin', httplib.FOUND)
    return {'title': 'Admin Login'}


@App.post('/login/submit')
def login_submit():
    username = request.forms.get('username')
    password = request.forms.get('password')
    print(username)
    print(password)
    redirect('/login', httplib.FOUND)
