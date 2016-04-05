# coding:utf-8
__author__ = 'chenghao'
from bottle import Bottle, request
import os, re

ueditor_bottle = Bottle()
config_json = {}


@ueditor_bottle.get("/ueditor")
def ueditor_get():
	action = request.query.get("action")
	data = get_json_data(action)
	return data


@ueditor_bottle.post("/ueditor")
def ueditor_post():
	action = request.query.get("action")
	files = request.files.getall("upfile")
	dispatch(action, files)


def get_json_data(action):
	"""
	获取json内容
	:param action:
	:return:
	"""
	global config_json
	path = os.path.join(os.path.dirname(__file__), "static/ueditor1_4_3_1-utf8-py/")
	# 获取json文件的内容, 并把注释替换掉
	with open(path + "/" + action + ".json", "r") as f:
		r = re.compile(r"(\/\*[\s\S]+?\*\/)")
		config_json = r.sub('', f.read())
	return config_json


def dispatch(action, files):
	"""
	任务分发
	:param action: uploadimage上传图片, uploadscrawl上传涂鸦图片, catchimage上传远程图片, uploadvideo上传视频,
					uploadfile上传文件
	:return:
	"""
	print config_json