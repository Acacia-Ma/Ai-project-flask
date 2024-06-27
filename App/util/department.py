from ..models import DepartmentModel, ChatModels

# 获取部门信息
def getParentLisDate(departs_infos):
    # 获取所有的父部门
    parent_infos = []
    # 获取所有的父部门
    for item in departs_infos:
        # 如果是父部门 则添加到父部门列表中
        if int(item.parent_id) == 0:
            # 添加到父部门列表中
            val = {
                "id": item.department_id,
                "parent_id": item.parent_id,
                "department_id": item.department_id,
                "label": item.department,
                "is_depart": True,
            }
            # 添加到父部门列表中
            parent_infos.append(val)
            # print("parent_infos:", parent_infos)
    return parent_infos

# 获取部门信息
def dataTreeData(departs_infos, parent_infos):
    # 获取所有的父部门
    for value in parent_infos:
        # 获取所有的子部门
        childrenArray = []
        # 获取所有的子部门
        for d_value in departs_infos:
            depart_id = value["department_id"]
            if d_value.parent_id == depart_id:
               t_depart = {
                   "id": d_value.department_id,
                   "parent_id": d_value.parent_id,
                   "department_id": d_value.department_id,
                   "label": d_value.department,
                   "is_depart": True,
               }
               childrenArray.append(t_depart)
                # print("childrenArray:", childrenArray)
            # 添加到父部门列表中
            value["children"] = childrenArray
            # 如果有子部门 则递归调用
            if len(childrenArray) > 0:
                dataTreeData(departs_infos, childrenArray)
    return parent_infos