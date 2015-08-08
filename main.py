#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import tenjin
import falcon
from libs.blog import App
from libs.blog import Config
from libs.blog import AdminHandler
from libs.blog import AccountHandler
from wsgiref.simple_server import make_server


class Context(falcon.RequestOptions):
    def __init__(self):
        self.__dict__['data'] = {}
        super(Context, self).__init__()

    def __getattr__(self, name):
        try:
            return self.data[name]
        except KeyError:
            return None

    def __setattr__(self, name, value):
        self.__dict__['data'][name] = value


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("usage: {0} /path/to/config.ini".format(sys.argv[0]))
        sys.exit(1)

    # initialize config file
    with open(sys.argv[1]) as fp:
        Config(fp)

    # initialize template engine
    view = tenjin.Engine(path=['views'])

    App.add_route('/account/login', AccountHandler())
    App.req_options = Context()
    App.req_options.view = view
    App.add_route('/admin', AdminHandler())
    httpd = make_server('localhost', 8080, App)
    httpd.serve_forever()
