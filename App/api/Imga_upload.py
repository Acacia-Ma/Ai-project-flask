# 前端图像上传保存到本地的upload文件夹下
# 上传的图像文件名为时间戳
import os
import time
from App.models import *
from flask import request, make_response, json
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from App.util.ocr_mix_instig import get_result
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
# 上传文件保存的路径,在当前文件的目录的上一级目录的upload文件夹下
UPLOAD_FOLDER = os.path.join(basedir, 'upload')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'bmp'])


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

class imga_upload(Resource):
    def post(self):
        # 检查文件夹是否存在
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        else:
            print("目录已存在")
        # 检查是否有文件
        if 'file' not in request.files:
            return {"msg": "没有上传文件", "code": 400}
        file = request.files['file']
        # 检查文件名是否为空
        if file.filename == '':
            return {"msg": "文件名不能为空", "code": 400}
        # 检查文件后缀名是否符合要求
        if not allowed_file(file.filename):
            return {"msg": "文件格式不支持，只支持png、jpg、jpeg、bmp", "code": 400}
        # 检查文件大小是否符合要求，限制文件大小为4MB
        if int(request.content_length) > 4 * 1024 * 1024:
            return {"msg": "文件大小超过限制,最大只允许4M", "code": 400}
        # 保存文件
        if file and allowed_file(file.filename):
            # 获取文件名
            filename = file.filename
            # 获取文件后缀名
            ext = filename.rsplit('.', 1)[1]
            # 生成新的文件名
            filename = str(int(time.time())) + '.' + ext
            # 保存文件
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            # 返回文件名
            return {"msg": "上传成功", "code": 0, "data": {"filename": filename}}
        else:
            return {"msg": "上传失败", "code": 400}


# 给前端返回图像文件
# 通过文件名获取文件
class imga_download(Resource):
    def get(self, img_name):
        # 获取文件名
        fire_dir = os.path.join(basedir, 'upload')
        # 获取文件后缀名
        image_data = open(os.path.join(fire_dir, '%s' % img_name), "rb").read()
        # 返回文件
        response = make_response(image_data)
        # 设置响应头，告诉浏览器这是一个图片
        response.headers['Content-Type'] = 'image/png/jpeg/jpg/bmp'
        # 返回响应
        return response

# 给前端返回图像识别结果
class ImageRecognition(Resource):
    # 将图像识别结果保存到数据库，并返回识别结果
    @jwt_required()
    def post(self):
        # 从请求中获取文件名
        data = request.get_json()
        filename = data.get('image_name')
        id = data.get('id')
        username = get_jwt_identity()
        if not filename:
            return {"msg": "文件名不能为空", "code": 400}

        # 检查文件是否存在
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if not os.path.exists(file_path):
            return {"msg": "文件不存在", "code": 404}
        print(file_path)
        # 调用图像识别函数
        try:
            recognition_result = get_result(file_path)
            # 提取识别结果whole_text
            print("识别结果：", recognition_result)
            recognition_result_end = json.loads(recognition_result)
            print("最后的识别结果：",recognition_result_end['whole_text'])
            text = recognition_result_end['whole_text']
            create_time = data.get('create_time')
            # 存储数据到数据库TextImgModel
            new_textimg = TextImgModel(
                img_id=id,
                username=username,
                content=text,
                created_at=create_time,
                name = filename,
            )
            db.session.add(new_textimg)
            db.session.commit()

            return {"msg": "识别成功", "code": 0, "data": {"text": text}}
        except Exception as e:
            return {"msg": str(e), "code": 500}
    # 识别历史记录
    @jwt_required()
    def get(self):
        username = get_jwt_identity()
        print("当前用户:", username)
        # 从数据库中获取识别历史记录
        sessions_img = TextImgModel.query.filter_by(username=username).all()
        session_img = [
            {
                "id": session_img.id,
                "img_id": session_img.img_id,
                "username": session_img.username,
                "content": session_img.content,
                "created_at": session_img.created_at,
                "name": session_img.name,
            }
            for session_img in sessions_img]
        return {"code": 0, "msg": "获取识别历史记录成功", "data": session_img}

# 用户头像修改
class UserImg(Resource):
    @jwt_required()
    def post(self):
        # 从请求中获取文件名
        data = request.json
        filename = data.get('image_name')
        print('用户头像文件名：',filename)
        username = get_jwt_identity()
        if not filename:
            return {"msg": "文件名不能为空", "code": 400}

        # 检查文件是否存在
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if not os.path.exists(file_path):
            return {"msg": "文件不存在", "code": 404}
        print(file_path)
        # 修改用户头像
        try:
            user = User.query.filter(User.username == username).first()
            user.img = filename
            db.session.commit()
            return {"msg": "修改成功", "code": 0}
        except Exception as e:
            return {"msg": str(e), "code": 500}

    # 获取用户头像
    @jwt_required()
    def get(self):
        username = get_jwt_identity()
        print("当前用户:", username)
        # 从数据库中获取用户头像
        user = User.query.filter(User.username == username).first()
        img = user.img
        print(img)
        if img:
            return {"code": 0, "msg": "获取用户头像成功", "data": {"img": img}}
        else:
            return {"msg": "获取用户头像失败，使用默认头像", "code": 400}