# -*- coding: utf-8 -*-

import os
import uuid
import json
import redis
import falcon
import httplib
from Cookie import SimpleCookie
from wsgisession import Session
from falcon.request import Request
from falcon.response import Response
from falcon import DEFAULT_MEDIA_TYPE
from wsgisession import SessionMiddleware


class RedisSessionFactory(object):
    def __init__(self):
        self.r = redis.StrictRedis()

    def load(self, id=None):
        session = Session()
        if id is None:
            id = uuid.uuid1().hex
        try:
            data = self.r.get(id)
            if data is not None:
                session.data = json.loads(data)
            session.id = id
        except Exception as e:
            print(e)
        return session

    def save(self, session):
        if session.id is not None:
            if self.r.set(session.id, json.dumps(session.data)):
                ttl = self.r.ttl(session.id)
                if ttl < 0:
                    self.r.expire(session.id, 300)
        return session.id


class StripSlashMiddleware(object):
    def process_request(self, req, resp):
        if req.path != '/':
            req.path = req.path.rstrip('/')

    def process_resource(self, req, resp, resource):
        pass

    def process_response(self, req, resp, resource):
        pass


class SessionMiddleware(object):
    def __init__(self, factory, env_key='wsgisession',
                 cookie_key='session_id'):
        self.factory = factory
        self.env_key = env_key
        self.cookie_key = cookie_key

    def process_request(self, req, resp):
        cookie = SimpleCookie()
        if 'HTTP_COOKIE' in req.env:
            cookie.load(req.env['HTTP_COOKIE'])
        id = None
        if self.cookie_key in cookie:
            id = cookie[self.cookie_key].value
        req.env[self.env_key] = self.factory.load(id)
        print(req.env[self.env_key].data)
        print('proces_request')

    def process_resource(self, req, resp, resource):
        # id = None
        # print(req.cookies)
        # if self.cookie_key in req.cookies:
        #     id = req.cookies[self.cookie_key]
        # req.env[self.env_key] = self.factory.load(id)
        print('process_resource')

    def process_response(self, req, resp, resource):
        print('saving value')
        print(req.env[self.env_key].id, req.env[self.env_key].data)
        id = self.factory.save(req.env[self.env_key])
        resp.set_cookie(self.cookie_key, id, path='/', secure=False)
        print('process_response')


App = falcon.API(middleware=[StripSlashMiddleware(),
                             SessionMiddleware(RedisSessionFactory(), 'session')])

class AccountHandler(object):
    def on_get(self, req, resp):
        print(req.cookies)
        if 'count' not in req.env['session']:
            print('initializing value')
            req.env['session']['count'] = 0
        else:
            print('setting value')
            req.env['session']['count'] += 1
        print(req.env['session']['count'])
        resp.body = 'Hello Blog!'

# @App.get('/admin')
# def admin():
#     if request.environ['session'].get('user') is None:
#         redirect('/login', httplib.FOUND)


# @App.get('/login')
# @view('login')
# def login():
#     if request.environ['session'].get('user') is not None:
#         redirect('/admin', httplib.FOUND)
#     return {'title': 'Admin Login'}


# @App.post('/login/submit')
# def login_submit():
#     username = request.forms.get('username')
#     password = request.forms.get('password')
#     print(username)
#     print(password)
#     redirect('/login', httplib.FOUND)
