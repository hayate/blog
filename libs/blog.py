# -*- coding: utf-8 -*-

import uuid
import json
import redis
import falcon
import ConfigParser
from tenjin.helpers import *


class Config(object):
    __state = {}

    def __init__(self, fp=None):
        """ application wide config object
        fp -- file or file-like object
        """
        self.__dict__ = self.__state
        if 'config' not in self.__dict__:
            self.config = ConfigParser.SafeConfigParser()
            if fp:
                self.config.readfp(fp)

    def __getattr__(self, name):
        return self.config[name]


class Session(object):
    def __init__(self):
        self.id = None
        self.data = {}

    def __setitem__(self, key, value):
        self.data[key] = value

    def __getitem__(self, key):
        return self.data[key]

    def __delitem__(self, key):
        try:
            del self.data[key]
        except KeyError:
            pass

    def __contains__(self, key):
        return key in self.data

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def get(self, key, default=None):
        try:
            return self.data[key]
        except KeyError:
            return default


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
        id = None
        if self.cookie_key in req.cookies:
            id = req.cookies[self.cookie_key]
        req.env[self.env_key] = self.factory.load(id)

    def process_resource(self, req, resp, resource):
        pass

    def process_response(self, req, resp, resource):
        id = self.factory.save(req.env[self.env_key])
        resp.set_cookie(self.cookie_key, id, path='/', secure=False)


class AuthMiddleware(object):
    def process_request(self, req, resp):
        if req.path.startswith('/admin'):
            if req.env['session'].get('user') is None:
                resp.status = falcon.HTTP_302
                resp.location = '/account/login'

    def process_resource(self, req, resp, resource):
        pass

    def process_response(self, req, resp, resource):
        pass


App = falcon.API(media_type='text/html; charset=utf-8',
                 middleware=[StripSlashMiddleware(),
                             SessionMiddleware(RedisSessionFactory(),
                                               'session'),
                             AuthMiddleware()])


class AccountHandler(object):
    def on_post(self, req, resp):
        username = req.get_param('username', True)
        password = req.get_param('password', True)

    def on_get(self, req, resp):
        resp.body = req.options.view.render('login.tpl',
                                            {'title': 'Admin Login'})


class AdminHandler(object):
    def on_get(self, req, resp):
        pass

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
