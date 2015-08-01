# -*- coding: utf-8 -*-

import redis
from bottle import Bottle
from wsgisession import Session
from wsgisession import SessionMiddleware


class RedisSessionFactory(object):
    def __init__(self):
        self.r = redis.StrictRedis()

    def load(self, id=None):
        print('load')
        session = Session()
        try:
            data = self.r.get(id)
            if data is not None:
                session.data = data
                session.id = id
        except:
            pass
        return session

    def save(self, session):
        print('save')
        if session.id is not None:
            self.r.set(session.id, session.data)
        return session.id


class Blog(Bottle):
    def __init__(self, catchall=True, autojson=True):
        super(Blog, self).__init__(catchall, autojson)
        self.app = SessionMiddleware(self.wsgi, RedisSessionFactory())

    def __call__(self, environ, start_response):
        return self.app(environ, start_response)

App = Blog()


@App.get('/hello')
def hello():
    return "Hello Blog!"
