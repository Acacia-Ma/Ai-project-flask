from flask_jwt_extended import jwt_required
from flask_restful import Resource
from flask import request
from App.models import *
from App.util.department import *
from App.models import *


# 获取部门信息
class GetDepartment(Resource):
    # 作用：获取部门信息
    def post(self):
        departs_infos = DepartmentModel.query.all()
        print(departs_infos)
        parent_infos = getParentLisDate(departs_infos)
        print(parent_infos)
        treedate = dataTreeData(departs_infos, parent_infos)
        print(treedate)
        return {"data": treedate, "code": 0, "msg": "获取部门信息成功"}


# 获取子部门信息
class SubDepart(Resource):
    # 作用：获取子部门信息
    def post(self):
        department_id = request.json.get('department_id', None)
        print(f'department_id:{department_id}')
        list = DepartmentModel.query.filter_by(parent_id=department_id).all()
        data_list = []
        for item in list:
            data_list.append({
                "department": item.department,
                "department_id": item.department_id,
                "parent_id": item.parent_id,
            })
        return {"code": 0, "msg": "获取子部门信息成功", "data": data_list, }


# 获取部门中的人员信息
class GetPerson(Resource):
    # 作用：获取部门人员信息
    def post(self):
        department_id = request.json.get('department_id', None)
        print(''.center(100, '-'))
        print("这里是获取部门人员信息")
        print(f'department_id:{department_id}')
        print(''.center(100, '-'))
        list = User.query.filter_by(department_id=department_id).all()
        data_list = []
        for item in list:
            data_list.append({
                "userid": item.job_number,
                "username": item.realname,
                "department_id": item.department_id,
                "phone": item.phone,
                "position": item.position,
            })
        print(data_list)
        return {"code": 0, "msg": "获取部门人员信息成功", "data": data_list}

# 添加部门人员信息
class AddDepartment(Resource):
    # 作用：添加部门
    def post(self):
        department_id = request.json.get('department_id', None)
        username = request.json.get('username', None)
        userid = request.json.get('userid', None)
        mobile = request.json.get('mobile', None)
        if department_id is None or username is None or userid is None or mobile is None:
            return {"code": 400, "msg": "信息不完整"}
        password = '123456'
        chat = User(username=userid, realname=username, password=password, img=None, department_id=department_id,
                    permission=1, position='用户', job_number=userid, phone=mobile)
        db.session.add(chat)
        db.session.commit()
        return {"code": 0, "msg": "添加部门成功","data":'用户'}
# 添加部门，并生成部门ID（department_id）
class AddDepart(Resource):
    # 作用：添加部门，并生成部门ID（department_id）
    def post(self):
        parent_id = request.json.get('parent_id', None)
        depart_name = request.json.get('depart_name', None)
        print(''.center(100, '-'))
        print(f'parent_id:{parent_id}, depart_name:{depart_name}')
        print(''.center(100, '-'))

        try:
            depart = DepartmentModel.query.filter_by(parent_id=parent_id).all()
            print(f'depart: {depart}')

            # 判断是否有子部门,如果有子部门，部门ID为最后一个部门ID+1，else部门ID为父部门ID*100+1
            if depart:
                # 确保 depart[-1].department_id 是整数
                last_department_id = int(depart[-1].department_id)
                department_id = last_department_id + 1
            else:
                department_id = (int(parent_id) * 100 + 1)

            print(f'department_id: {department_id}')

            # 添加部门
            depart = DepartmentModel(department_id=department_id, department=depart_name, parent_id=parent_id)
            db.session.add(depart)
            db.session.commit()
            return {"code": 0, "msg": "添加部门成功", "data": department_id}
        except Exception as e:
            print(f"Exception: {e}")
            return {"code": 400, "msg": "添加部门失败"}


# 编辑部门名称(修改部门名称)
class EditDepart(Resource):
    # 作用：编辑部门名称
    def post(self):
        department_id = request.json.get('department_id', None)
        depart_name = request.json.get('depart_name', None)
        try:
            depart = DepartmentModel.query.filter_by(department_id=department_id).first()
            depart.department = depart_name
            db.session.commit()
            return {"code": 0, "msg": "修改部门名称成功"}
        except Exception as e:
            return {"code": 400, "msg": "修改部门名称失败"}

# 删除部门，数据库里有parent_id字段，和department_id字段，需要判断是否有子部门
class DelDepart(Resource):
    # 作用：删除部门
   def post(self):
        department_id = request.json.get('department_id', None)
        try:
            depart = DepartmentModel.query.filter_by(parent_id=department_id).all()
            # 判断是否有子部门
            if depart:
                return {"code": 400, "msg": "删除失败，该部门下有子部门"}
            else:
                depart = DepartmentModel.query.filter_by(department_id=department_id).first()
                db.session.delete(depart)
                db.session.commit()
                return {"code": 0, "msg": "删除部门成功"}
        except Exception as e:
            return {"code": 400, "msg": "删除部门失败"}

# 批量删除部门成员信息，使用department_id和userid字段
class DelPerson(Resource):
    # 作用：删除部门成员信息
    def post(self):
        department_id = request.json.get('department_id', None)
        userid = request.json.get('userid', None)
        try:
            user = User.query.filter_by(department_id=department_id, job_number=userid).first()
            db.session.delete(user)
            db.session.commit()
            return {"code": 0, "msg": "删除部门成员信息成功"}
        except Exception as e:
            return {"code": 400, "msg": "删除部门成员信息失败"}
