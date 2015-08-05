#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libs.blog import App
from libs.blog import AccountHandler
from wsgiref.simple_server import make_server

App.add_route('/', AccountHandler())
httpd = make_server('localhost', 8080, App)
httpd.serve_forever()
