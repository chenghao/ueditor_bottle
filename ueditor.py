# coding:utf-8
__author__ = 'chenghao'
from bottle import Bottle, request, static_file
import os, re, json
from datetime import datetime

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
	res = dispatch(action, files)
	return res


@ueditor_bottle.get('/upload/<filename:path>')
def static(filename):
	""" Serve static files """
	return static_file(filename, root='./upload/')


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


def get_full_name(path_format):
	now = datetime.now()
	d = now.strftime("%Y-%y-%m-%d-%H-%M-%S").split("-")
	path_format = path_format.replace("{yyyy}", d[0])
	path_format = path_format.replace("{yy}", d[1])
	path_format = path_format.replace("{mm}", d[2])
	path_format = path_format.replace("{dd}", d[3])
	path_format = path_format.replace("{hh}", d[4])
	path_format = path_format.replace("{ii}", d[5])
	path_format = path_format.replace("{ss}", d[6])
	return path_format


def create_directory(path):
	if not os.path.exists(path):
		os.makedirs(path)


def get_path_format(action, obj):
	if action == "uploadimage":
		return obj.get("imagePathFormat")
	elif action == "uploadscrawl":
		return obj.get("scrawlPathFormat")
	elif action == "catchimage":
		return obj.get("catcherPathFormat")
	elif action == "uploadvideo":
		return obj.get("videoPathFormat")
	elif action == "uploadfile":
		return obj.get("filePathFormat")
	elif action == "uploadsnapscreen":
		return obj.get("snapscreenPathFormat")
	else:
		return "/ueditor/py/upload/custom"


def get_file_path(path_s):
	return os.getcwd() + path_s


def dispatch(action, files):
	"""
	任务分发
	:param action: uploadimage 上传图片, uploadscrawl 上传涂鸦图片, catchimage 上传远程图片, uploadvideo 上传视频,
					uploadfile 上传文件, uploadsnapscreen 上传屏幕截图
	:return:
	"""
	obj = json.loads(config_json)
	absolute_path = obj["absolutePath"]  # 绝对路经
	if absolute_path:  # 使用绝对路经保存
		create_directory(absolute_path)
		file_path = absolute_path
	else:  # 使用相对路经保存
		path_format = get_full_name(get_path_format(action, obj))
		path = get_file_path(path_format)
		create_directory(path)
		file_path = path

	if action == "uploadimage":
		res = upload_image(files, obj["imageFieldName"], obj["imageMaxSize"], obj["imageAllowFiles"], file_path,
						   path_format)
	elif action == "uploadscrawl":
		pass
	elif action == "catchimage":
		pass
	elif action == "uploadvideo":
		pass
	elif action == "uploadfile":
		pass
	elif action == "uploadsnapscreen":
		pass
	elif action == "listimage":
		pass
	elif action == "listfile":
		pass
	else:
		pass

	return res


def upload_image(files, max_size, allow_files, file_path, path_format):
	res = {}
	for f in files:
		file_name = f.filename
		file_size = os.path.getsize(f.file.name)

		name, ext = os.path.splitext(file_name)
		if ext not in allow_files:  # 上传的图片格式不正确
			res['state'] = "上传的图片格式不正确"

		if long(max_size) < file_size:  # 图片太大
			res['state'] = "图片太大"

		if not res:  # 判断该dict是否为空
			f.save(file_path, overwrite=True)
			res["state"] = "SUCCESS"
			res["url"] = path_format + "/" + file_name

		return res

