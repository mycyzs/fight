# -*- coding: utf-8 -*-

import StringIO
import datetime
import json

import xlrd
import xlsxwriter
from django.db.models import Q
from django.http import HttpResponse

from blueking.component.shortcuts import get_client_by_request
from common.mymako import render_json
from home_application.celery_tasks import run_celery
from home_application.decorator import TryException
from home_application.tmp.models import *

ERROR_MSG = {
    "result": False,
    "data": [u"系统异常，请联系管理员！"]
}


def test(request):
    return render_json({'result': True, 'data': request.GET.dict()})


@TryException(u'查询邮箱')
def search_mail(request):
    try:
        args = eval(request.body)
    except:
        args = json.loads(request.body)
    result = MailReceiver.objects.filter(account__icontains=args["username"], mailbox__icontains=args["mailbox"], when_created__range=(args["whenStart"] + " 00:00:00", args["whenEnd"] + ":59"))
    if args["created_by"] != '00':
        result = result.filter(created_by=args["created_by"])
    return_data = [i.to_dic() for i in result.order_by("-when_created")]
    return render_json({"result": True, "data": return_data})


@TryException(u'新增邮箱')
def add_mail(request):
    args = eval(request.body)
    is_exist = MailReceiver.objects.filter(Q(account=args["account"]) | Q(mailbox=args["mailbox"]))
    if is_exist:
        return render_json({"result": False, 'data': u'该账号或邮箱已存在！'})
    args["when_created"] = str(datetime.datetime.now()).split('.')[0]
    args["created_by"] = request.user.username
    # args.pop("created_by")
    MailReceiver.objects.create(**args)
    return render_json({'result': True})


@TryException(u'修改邮箱')
def modify_mail(request):
    args = eval(request.body)
    is_exist = MailReceiver.objects.filter(Q(account=args["account"]) | Q(mailbox=args["mailbox"])).exclude(id=args["id"])
    if is_exist:
        return render_json({"result": False, 'data': u'该账号或邮箱已存在！'})
    MailReceiver.objects.filter(id=args["id"]).update(**args)
    return render_json({'result': True})


@TryException(u'删除邮箱')
def delete_mail(request):
    mail_id = request.GET["id"]
    MailReceiver.objects.get(id=mail_id).delete()
    return render_json({'result': True})


@TryException(u'获取图表数据')
def get_chart_data(request):
    line_list = [
        # 线图一个字典代表一条线，data里面的必须是数字类型或浮点数类型
        {"name": u"线1", "data": [11, 2, 13, 4, 15, 6]},
        {"name": u"线2", "data": [6, 15, 7, 19, 7, 14]},
        {"name": u"线3", "data": [7, 16, 5, 14, 3, 12]},
    ]
    # 横坐标，一般用字符串列表，列表长度和data保持一致即可
    categories = ['a', 'b', 'c', 'd', 'e', 'f']


    pie_list = [
        # 饼图，y为数字，后面的为该饼的颜色显示，color字段可以不要，不要饼图的颜色会随机生成
        {"name": "高", "y": 3, "color": "#ea4335"},
        {"name": "中", "y": 2, "color": "#fbbc05"},
        {"name": "低", "y": 1, "color": "#f5fc88"},
    ]
    return render_json({'result': True, 'line_list': line_list, "pie_list": pie_list, 'categories': categories})


@TryException(u'获取业务列表')
def get_app_list(request):
    client = get_client_by_request(request)
    result = client.cc.search_business({})
    return_data = []
    if result["result"]:
        return_data = [{'id': i["bk_biz_id"], 'text': i["bk_biz_name"]} for i in result["data"]["info"]]
    return render_json({"result": True, 'data': return_data})


@TryException(u'获取业务下的服务器列表')
def get_server_list(request):
    app_id = request.GET['app_id']
    client = get_client_by_request(request)
    kwargs = {
        "condition": [
            {
                "bk_obj_id": "biz",
                "fields": [],
                "condition": [{"field": "bk_biz_id", "operator": "$eq", "value": int(app_id)}]

            },
            {
                "bk_obj_id": "host",
                "fields": [],
                "condition": []
            },
        ]
    }
    res = client.cc.search_host(kwargs)
    return_data = []
    for i in res['data']['info']:
        one_obj = i['host']
        one_obj["app_id"] = i["biz"][0]["bk_biz_id"]
        one_obj['bk_biz_id'] = i["biz"][0]["bk_biz_id"]
        return_data.append({
            'id': i['host']['bk_host_innerip'] + "s" + str(i['host']['bk_cloud_id'][0]['bk_inst_id']),
            'text': i['host']['bk_host_innerip']
        })
    return render_json({"result": True, 'data': return_data})


@TryException(u'获取业务拓扑树')
def get_app_topo(request):
    app_id = request.GET["app_id"]
    client = get_client_by_request(request)
    result = client.cc.search_biz_inst_topo({
        'bk_biz_id': app_id, 'level': -1
    })
    return_data = result["data"]
    for i in return_data:
        set_data = get_set_data(i)
        i["child"] = set_data
        format_is_parent(i)
    return render_json({"result": True, 'data': result["data"]})


def get_set_data(one_obj):
    return_data = []
    for i in one_obj["child"]:
        if i["bk_obj_id"] == 'set':
            return_data.append(i)
            continue
        else:
            return_data.extend(get_set_data(i))
    return return_data


def format_is_parent(i):
    i["isParent"] = len(i["child"]) > 0
    if i["isParent"]:
        for u in i["child"]:
            format_is_parent(u)


@TryException(u'获取主机的全部属性')
def get_host_attr(request):
    client = get_client_by_request(request)
    result = client.cc.search_object_attribute({'bk_obj_id': 'host'})
    return render_json({"result": True, 'data': [{'id': i['bk_property_id'], 'text': i['bk_property_name']} for i in result['data']]
                        })


@TryException(u'根据业务、集群、模块或其他节点ID获取服务器列表')
def search_server_list(request):
    filter_obj = eval(request.body)
    bk_biz_id = request.GET["bk_biz_id"]
    client = get_client_by_request(request)
    if filter_obj["bk_obj_id"] not in ['biz', 'module', 'set']:
        filter_obj["bk_obj_id"] = 'object'
        condition = [{"field": "bk_inst_id", "operator": "$eq", "value": int(filter_obj["value"])}]
    else:
        condition = [{"field": "bk_%s_id" % filter_obj["bk_obj_id"], "operator": "$eq", "value": int(filter_obj["value"])}]
    kwargs = {
        'bk_biz_id': bk_biz_id,
        "condition": [
            {
                "bk_obj_id": filter_obj["bk_obj_id"],
                "fields": [],
                "condition": condition
            },
            {
                "bk_obj_id": "host",
                "fields": [],
                "condition": []
            }
        ]
    }
    result = client.cc.search_host(kwargs)
    return render_json({"result": True, 'data': [i['host'] for i in result["data"]["info"]]})


@TryException(u'获取树形拓扑数据')
def get_tree_data(request):
    return_data = [
        # 注意，只有display_name，isParent，child这三个字段是必须的，其它字段看需求
        # 我这边加多一个name，为了获取子节点用
        {'display_name': '树1', 'isParent': True, 'name': '1', 'child': [
            # 此次两条数据的isParent不同，如果为False，此节点不会有+号
            # 如果为True，此节点会有+号，且点击+号会加载节点数据
            {'display_name': '树1节点1', 'isParent': False, 'child': [], 'name': '11'},
            {'display_name': '树1节点2', 'isParent': True, 'child': [], 'name': '12'},
        ]}
    ]

    return render_json({"result": True, 'data': return_data})


@TryException('获取子节点数据')
def get_tree_node_data(request):
    name = request.GET.get("name", '')
    if not name:
        return render_json([])
    real_name = str(int(name) + 1)
    return_data = [
        {'display_name': '树1节点1' + real_name, 'isParent': False, 'child': [], 'name': real_name},
    ]
    return render_json(return_data)


@TryException(u"测试Celery")
def test_celery(request):
    run_celery.delay(request.user.username)
    return render_json({"result": True})


# 上传文件
def upload_file(request):
    try:
        file_obj = request.FILES.get('upfile', '')
        name = file_obj.name
        content = file_obj.read()
        # # excel解析
        # biaotou = ['id', 'name', 'age']
        # is_excel = True
        # if is_excel:
        #     data = parse_excel(biaotou, file_contents=content)
        # 文件直接存数据库

        file = FileObj.objects.create(file_name=name, file_content=content)
        return render_json({"result": True, 'file_id': file.id})
    except Exception as e:
        return render_json({'result': False})


def download_temp(request):
    file_obj = FileObj.objects.filter(id=1).first()
    if not file_obj:
        return render_json({"result": False, 'data': u"无模板"})
    return download_file(file_obj.file_content, file_obj.file_name)


# 下载文件
def download_file(file_buffer, file_name):
    response = HttpResponse(file_buffer, content_type='APPLICATION/OCTET-STREAM')
    response['Content-Disposition'] = 'attachment; filename=' + file_name.encode("utf8")
    response['Content-Length'] = len(file_buffer)
    return response


# 生成Excel文件
"""
data_detail = [
    {'id': u'序号', 'name': u'姓名', 'addr': u'地址', 'score': u'分数'}, # excel表头
    {'id': '1', 'name': 'zhang', 'addr': 'hubei', 'score': 100},
    {'id': '2', 'name': 'liu', 'addr': 'hubei', 'score': 120},
    {'id': '3', 'name': 'wu', 'addr': 'hubei', 'score': 130},
]
data_key = data_detail[0].keys()
filename = "学生分数.excel"
"""


def make_excel(data_detail, data_key):
    sio = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(sio)
    worksheet = workbook.add_worksheet()
    header_format = workbook.add_format({
        'num_format': '@',
        'text_wrap': True,
        'valign': 'vcenter',
        'indent': 1,
    })
    cols_num = data_detail.__len__()
    rows_num = data_detail[0].keys().__len__()
    itemlist = data_key
    for col in range(cols_num):
        for row in range(rows_num):
            data = data_detail[col][itemlist[row]]
            if row == 0:
                with_op = 10
            else:
                with_op = 20
            worksheet.set_column(col, row, with_op)
            if type(data) == dict:
                worksheet.write(col, row, data['name'], header_format)
                worksheet.data_validation(col, row, col, row, {'validate': 'list', 'source': data['list']})
            else:
                if itemlist[row] == 'vm_expired_time':
                    if data == '0':
                        worksheet.write(col, row, '', header_format)
                    else:
                        worksheet.write(col, row, data, header_format)
                else:
                    worksheet.write(col, row, data, header_format)
    workbook.close()
    sio.seek(0)
    file_data = sio.getvalue()
    return file_data


# 解析excel, data_key是表头的意思，filename:文件完整路径，file_contents文件内容，二进制读取后的
def parse_excel(data_key, filename=None, file_contents=None):
    data = xlrd.open_workbook(filename=filename, file_contents=file_contents)
    table = data.sheets()[0]
    nrows = table.nrows
    data_list = []
    for i in range(1, nrows):
        data_dict = {}
        table_row_value = table.row_values(i)
        for g in range(table_row_value.__len__()):
            data_dict[data_key[g]] = table_row_value[g]
        data_list.append(data_dict)
    return data_list
