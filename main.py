#!/usr/bin/env python
# -*- coding: utf-8 -*-

from libs.blog import App
from libs.bottle import run

run(App, host='localhost', port=8080, debug=True, reloader=True)
