# -*- coding: utf-8 -*-





"""
------额外的功能函数------------
"""
import StringIO
import base64
import codecs
import csv
import datetime
import json
import os
import sys
import time

import xlrd
import xlsxwriter
from django.http import FileResponse, HttpResponse

from common.log import logger
from common.mymako import render_json
from conf.default import STATIC_URL, PROJECT_ROOT
from home_application.models import Host, File
from home_application.tmp.models import FileObj

"""保存图片到数据库"""
def upload_pic(request):
    try:
        book_id = request.GET.get("book_id", "")
        # if not book_id:
        #     return render_json({'result':False})
        #book = Book.objects.get(id=book_id)
        f = File.objects.get(id=book_id)
        if request.body == "{}":
            img_data = "{}"
        else:
            img_data = base64.b64encode(request.body)
        f.file_content = img_data
        f.save()
        return render_json({"result":True})
    except Exception as e:
        print e

"""从数据库获取图片"""
def get_background_img(request):
    book_id = request.GET.get('id')
    book = File.objects.get(id = book_id)
    if book.file_content:
        background_data = book.file_content.decode('base64')
        response = HttpResponse(background_data, content_type='image/png')
        response['Content-Length'] = len(background_data)
    # else:
    #     photo_data = default_img.decode('base64')
    #     response = HttpResponse(photo_data, content_type='image/png')
    #     response['Content-Length'] = len(photo_data)
    return response


"""第一种方法"""
"""上传普通文件,保存在static目录下，新的名字为test_文件名"""
def upload_info(request):
    try:
        obj_id = int(request.GET.get("obj_id"))
        file_path_name = request.POST.get("file_path")
        upload_info_folder = sys.path[0] + STATIC_URL

        file_one = request.FILES.get('upfile')
        name = file_one.name
        real_name = file_path_name + name
        """可以把文件名保存在数据库对应不同的对象"""
        file_new = open(os.path.join(upload_info_folder, real_name), 'wb')
        file_new.write(file_one.read())
        file_new.close()
        return render_json({"result": True})
    except Exception, e:
        logger.error(e)
        return render_json({"result": False, "data": [u"上传文件失败！"]})


"""从static下载对应名字的文件"""
def down_load_field(request):

    obj_id = request.GET.get('obj_id')
    #获取对象对应的文件
    # field_name = Host.objects.get(id=obj_id).field_name
    field_name = 'test_linux.txt'
    #目录
    upload_info_folder = sys.path[0] + STATIC_URL
    file = open(os.path.join(upload_info_folder, field_name), 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/*'
    response['Content-Disposition'] = 'attachment;filename=' + field_name
    return response


"""第二种方法"""
"""上传普通文件存入数据库"""
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

        file = File.objects.create(file_name=name, file_content=content)
        return render_json({"result": True, 'file_id': file.id})
    except Exception as e:
        return render_json({'result': False})


"""从数据库读取普通文件下载到本地"""
def download_common_file(request):
    file_obj = File.objects.filter(id=2).first()
    if not file_obj:
        return render_json({"result": False, 'data': u"无模板"})
    file_content = file_obj.file_content
    file_name = file_obj.file_name
    response = HttpResponse(file_content, content_type='APPLICATION/OCTET-STREAM')
    response['Content-Disposition'] = 'attachment; filename=' + file_name.encode("utf8")
    response['Content-Length'] = len(file_content)
    return response



"""导入excel文件，写入数据库"""
def up_excel(request):
    try:
        obj_id = request.GET.get('obj_id')
        name = 'ali%s.xlsx' % (time.time())
        file = open(name, 'wb')
        file.write(request.FILES['files'].read())
        file.close()
        data = xlrd.open_workbook(name)
        table = data.sheets()[0]
        nrows = table.nrows
        #对应数据库的字段
        index_list = ['name', 'age', 'text']
        data_list = []
        #从excel文件第几行开始读取数据
        for i in range(1, nrows):
            data_dict = {}
            table_row_value = table.row_values(i)
            for g in range(table_row_value.__len__()):
                data_dict[index_list[g]] = table_row_value[g]
            data_list.append(data_dict)
        error_list = []
        try:
            for g in data_list:
                try:
                    # excel_demo = Excel_Demo.objects.filter(InstanceId=g['InstanceId'])
                    # if excel_demo:
                    #     excel_demo.update(**g)
                    # else:
                    g['when_created'] = datetime.datetime.now()
                    Host.objects.create(**g)
                except Exception,e:
                    print e
                    error_list.append(g['PrivateIpAddress'])
        except Exception, e:
            print e
        os.remove(name)
        if error_list.__len__() == 0:
            return render_json({'result': True})
        else:
            return render_json({'result': False, 'error': '、'.join(error_list)})
    except Exception,e:
        print e
        return render_json({'result': False})



"""导出excel文件"""
def down_excel(request):
    #获取数据库数据
    obj_id = request.GET.get('obj_id')
    ecs_info = Host.objects.get(id=obj_id)
    data = [{'name':u'名字', 'age': u'年龄', 'text': u'内容', 'when_created': u'时间'
             }]
    data.append({
        'name': ecs_info.name,
        'age': ecs_info.age,
        'text': ecs_info.text,
        'when_created': ecs_info.when_created.strftime("%Y-%m-%d %H:%M:%S")
    })
    data_key = ['name', 'age', 'text', 'when_created']
    return make_excel(data, data_key, 'ECS')


# 生成Excel文件
def make_excel(get_data, data_key, get_file_name):
    sio = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(sio)
    worksheet = workbook.add_worksheet()
    header_format = workbook.add_format({
        'num_format': '@',
        'text_wrap': True,
        'valign': 'vcenter',
        'indent': 1,
    })
    cols_num = get_data.__len__()
    rows_num = get_data[0].keys().__len__()
    itemlist = data_key
    for col in range(cols_num):
        for row in range(rows_num):
            data = get_data[col][itemlist[row]]
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
    response = HttpResponse(sio.getvalue(), content_type='APPLICATION/OCTET-STREAM')
    file_name = 'attachment; filename=%s.xlsx'%(get_file_name)
    response['Content-Disposition'] = file_name
    return response



"""导出csv"""
def down_csv(request):
    try:
        obj_id = request.GET.get("obj_id")
        data_list = []
        host = Host.objects.get(id=obj_id)

        data_list.append([
            host.name, host.age, host.text, host.when_created.strftime("%Y-%m-%d %H:%M:%S")
        ])
        f = codecs.open('Host-Info.csv', 'wb', "gbk")
        writer = csv.writer(f)
        writer.writerow([u"姓名",u"年龄", u"内容",u"时间"])
        writer.writerows(data_list)
        f.close()
        file_path = "{0}/Host-Info.csv".format(PROJECT_ROOT).replace("\\", "/")
        file_name = "Host-Info.csv"
        return download_file(file_path, file_name)

    except Exception as e:
        logger.exception('download cvs file error:{0}'.format(e.message))
        return HttpResponse('导出失败！')


def download_file(file_path, file_name):
    try:
        file_path = file_path
        file_buffer = open(file_path, 'rb').read()
        response = HttpResponse(file_buffer, content_type='APPLICATION/OCTET-STREAM')
        response['Content-Disposition'] = 'attachment; filename=' + file_name
        response['Content-Length'] = os.path.getsize(file_path)
        return response
    except Exception as e:
        logger.exception("download file error:{0}".format(e.message))



"""导入csv"""
def up_csv(request):
    try:
        username = request.user.username
        up_data = json.loads(request.body)
        # kaoshi_id = up_data[0]['kaoshi_id']
        # host = Host.objects.get(id=kaoshi_id)
        for data in up_data:
            Host.objects.create(name=data['name'], text=data['text'], age=data['age'], when_created=datetime.datetime.now())
        return render_json({"result": True})
    except Exception as e:
        return render_json({'result': False})
