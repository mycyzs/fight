# -*- coding: utf-8 -*-
import json

from common.mymako import render_json
from home_application.esb_api import excute_by_script
from home_application.helper import to_datetime, get_categories_days, get_categories_minutes


# 查询系统信息
from home_application.models import Book, Log


def get_sys_info(request):
    try:
        req_data = json.loads(request.body)
        start_time = to_datetime(req_data['start_time'])
        return_data = []
        data = {
            "id": 1,
            "sys_name": "test",
            "sys_code": "te",
            "owners": "dd",
            "is_control": "否",
            "department": "dd",
            "comment": "dja",
        }
        return_data.append(data)
        return render_json({"result": True, "data": return_data})
    except Exception as e:
        return render_json({"result": False, "msg": [u"查询系统信息失败!!"]})


# 新增系统信息
def add_sys(request):
    try:
        req_data = json.loads(request.body)
        start_time = to_datetime(req_data['start_time'])

        # 存入数据库

        data = {
            "id": 2,
            "sys_name": "新增系统",
            "sys_code": "www",
            "owners": "wwwww",
            "is_control": "是",
            "department": "www",
            "comment": "wwwww",
        }

        return render_json({"result": True, "data": data})
    except Exception as e:
        return render_json({"result": False, "msg": [u"新增系统信息失败!!"]})


# 修改系统信息
def modify_sys(request):
    try:
        req_data = json.loads(request.body)
        id = req_data['id']

        # 存入数据库

        data = {
            "sys_name": "修改系统",
            "sys_code": "gggg",
            "owners": "gggg",
            "is_control": "是",
            "department": "gggg",
            "comment": "ggg",
        }

        return render_json({"result": True, "data": data})
    except Exception as e:
        return render_json({"result": False, "msg": [u"修改系统信息失败!!"]})


# 删除系统信息
def delete_sys(request):
    try:
        req_data = json.loads(request.body)
        id = req_data['id']

        # 从数据库中删除

        return render_json({"result": True, "data": {}})
    except Exception as e:
        return render_json({"result": False, "msg": [u"修改系统信息失败!!"]})


# 执行脚本获取主机mem、disk、cpu
def get_host_data(request):
    try:
        req_data = json.loads(request.body)
        host_id = req_data['text']
        host = Book.objects.filter(ip=host_id).first()
        SER = Log.objects.filter(host=host)
        CAT = []
        MEM = []
        DISK = []
        CPU = []
        for s in SER:
            dk = eval(s.date_time)
            aa = eval(s.mem)
            bb = eval(s.disk)
            cc = eval(s.cpu)
            CAT.append(dk[0])
            dd = float(aa[0].split("%")[0])
            MEM.append(dd)
            DISK.append(float(bb[0].split("%")[0]))
            CPU.append(float(cc[0].split("%")[0]))
        install_list = [
            {"name": u"mem", "data": MEM},
            {"name": u"disk", "data": DISK},
            {"name": u"cpu", "data": CPU}
        ]
        return render_json({'result': True, 'line_list': install_list, 'categories': CAT})
    except Exception as e:
        return render_json({"result": False, "msg": [u"修改系统信息失败!!"]})


# 检查主机是否已经在周期表
def check_ip(request):
    try:
        req_data = json.loads(request.body)
        username = request.user.username
        ip = req_data['text']
        if Book.objects.filter(ip=ip).exists():
            return render_json({"result": True, "data": {}})
        else:
            return render_json({"result": False, "data": {}})
    except Exception as e:
        return render_json({"result": False, "msg": [u"修改系统信息失败!!"]})


# 加入周期
def push_into_book(request):
    try:
        req_data = json.loads(request.body)
        username = request.user.username
        ip = req_data['text']
        bk_cloud_id = int(req_data['bk_cloud_id'])
        biz_id = int(req_data['biz_id'])
        Book.objects.create(ip=ip, biz=biz_id, bk_cloud_id=bk_cloud_id)

        return render_json({"result": True, "data": {}})

    except Exception as e:
        return render_json({"result": False, "msg": [u"修改系统信息失败!!"]})


# 加入周期
def delete_from_book(request):
    try:
        req_data = json.loads(request.body)
        username = request.user.username
        ip = req_data['text']
        bk_cloud_id = int(req_data['bk_cloud_id'])
        biz_id = int(req_data['biz_id'])
        Book.objects.filter(ip=ip).delete()

        return render_json({"result": True, "data": {}})

    except Exception as e:
        return render_json({"result": False, "msg": [u"修改系统信息失败!!"]})



"""异步立即执行和定时执行"""
# def add_task(request):
#     try:
#         username = request.user.username
#         request_data = json.loads(request.body)
#         biz_list = request_data['biz_l']
#         tem = Host.objects.get(id=request_data['template'])
#         etra = {}
#         if request_data['task_type'] == 'set_time':
#             etra['time'] = request_data['time']
#             etra['late_time'] = request_data['late_time']
#
#         data = {
#             "task_name": request_data['task_name'],
#             "host": request_data['host'].split("@")[0],
#             "task_type": request_data['task_type'],
#             "create_time": datetime.datetime.now(),
#             "etra": etra,
#             "tem": tem,
#             "cloud_id": int(request_data["host"].split("@")[1]),
#             "default_area": request_data["host"].split("@")[2]
#         }
#         task = Task.objects.create(**data)
#         script = tem.script
#         #执行脚本
#         #可以选择异步执行
#         data_obj = {
#             "username": username,
#             "id": task.id,
#             "tem_id": tem.id,
#             "biz": int(request_data['biz'])
#         }
#         if request_data['task_type'] == 'now':
#             # 异步立即执行
#             exute_script.delay(data_obj)
#         else:
#             # 异步定时执行
#             set_time_exute_script.apply_async(kwargs=data_obj, eta=datetime.datetime.strptime("2019-06-25 16:57:00", "%Y-%m-%d %H:%M:%S"))
#         del data['tem']
#         data['id'] = task.id
#         data['create_time'] = task.create_time.strftime("%Y-%m-%d %H:%M:%S")
#         data['template'] = task.tem.name
#         data['task_type'] = u'立即' if task.task_type == 'now' else u"周期"
#         return render_json({"result": True, "data": data})
#     except Exception as e:
#         logger.error(e)
#         return render_json({"result": False, "msg": [u"新增任务失败!!"]})