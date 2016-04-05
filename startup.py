# coding:utf-8
__author__ = 'chenghao'
from gevent import monkey

monkey.patch_all()

from bottle import run, Bottle, GeventServer as server, static_file, view
from ueditor import ueditor_bottle

bottle = Bottle()


@bottle.get("/", apply=[view("./index")])
def index():
	pass


@bottle.get('/static/<filename:path>')
def static(filename):
	""" Serve static files """
	return static_file(filename, root='./static/')


bottle.merge(ueditor_bottle)

run(server=server, app=bottle, host='0.0.0.0', port=8000, reloader=True, debug=True)