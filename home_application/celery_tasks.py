# -*- coding: utf-8 -*-
"""
celery 任务示例

本地启动celery命令: python  manage.py  celery  worker  --settings=settings
周期性任务还需要启动celery调度命令：python  manage.py  celerybeat --settings=settings
"""
import datetime

from celery import task
from celery.schedules import crontab
from celery.task import periodic_task

from common.log import logger

from blueking.component.shortcuts import get_client_by_user
from home_application.esb_api import excute_by_script
from home_application.esb_helper import *
from home_application.models import Book, Log


@task()
def async_task(x, y):
    """
    定义一个 celery 异步任务
    """
    logger.error(u"celery 定时任务执行成功，执行结果：{:0>2}:{:0>2}".format(x, y))
    return x + y


def execute_task():
    """
    执行 celery 异步任务

    调用celery任务方法:
        task.delay(arg1, arg2, kwarg1='x', kwarg2='y')
        task.apply_async(args=[arg1, arg2], kwargs={'kwarg1': 'x', 'kwarg2': 'y'})
        delay(): 简便方法，类似调用普通函数
        apply_async(): 设置celery的额外执行选项时必须使用该方法，如定时（eta）等
                      详见 ：http://celery.readthedocs.org/en/latest/userguide/calling.html
    """
    now = datetime.datetime.now()
    logger.error(u"celery 定时任务启动，将在60s后执行，当前时间：{}".format(now))
    # 调用定时任务
    async_task.apply_async(args=[now.hour, now.minute], eta=now + datetime.timedelta(seconds=60))


@periodic_task(run_every=crontab(minute='*/5', hour='*', day_of_week="*"))
def get_time():
    """
    celery 周期任务示例

    run_every=crontab(minute='*/5', hour='*', day_of_week="*")：每 5 分钟执行一次任务
    periodic_task：程序运行时自动触发周期任务
    """
    execute_task()
    now = datetime.datetime.now()
    logger.error(u"celery 周期任务调用成功，当前时间：{}".format(now))


@task()
def run_celery(username):
    client = get_client_by_user(username)
    check_app = {
        'bk_biz_id': 3,
        'ip_list': [{
            'ip': '192.168.165.11',
            'bk_cloud_id': 0
        }]
    }
    execute_account = 'root'
    script_content = 'echo 123'
    result = fast_execute_script(check_app, client, execute_account, script_content)
    log_result = get_task_ip_log(client, check_app["bk_biz_id"], result['data'])
    return log_result



"""两分钟执行一次book表的主机，执行脚本获取mem、disk、cpu"""
# @periodic_task(run_every=crontab(minute='*/2', hour='*', day_of_week="*"))
# def get_host_data():
#     try:
#         hosts = Book.objects.all()
#         for host in hosts:
#             username = 'admin'
#             app_id = host.biz
#             app_list = [{'ip': host.ip, 'bk_cloud_id': host.bk_cloud_id}]
#             script_content = """
#                     #!/bin/bash
#                     MEMORY=$(free -m | awk 'NR==2{printf "%.2f%%", $3*100/$2 }')
#                     DISK=$(df -h | awk '$NF=="/"{printf "%s", $5}')
#                     CPU=$(top -bn1 | grep load | awk '{printf "%.2f%%", $(NF-2)}')
#                     DATE=$(date "+%Y-%m-%d %H:%M:%S")
#                     echo -e "$DATE|$MEMORY|$DISK|$CPU"
#                     """
#             result = excute_by_script(username, app_id, app_list, script_content)
#             if result['result']:
#                 data = result['data'][0]['log_content']
#                 data_list = data.split('|')
#                 date_time = data_list[0],
#                 mem = data_list[1],
#                 disk = data_list[2],
#                 cpu = data_list[3],
#
#                 Log.objects.create(host=host, mem=mem, disk=disk, cpu=cpu, date_time=date_time)
#     except Exception as e:
#         print e


"""异步立即执行、定时执行相关"""
# @task()
# def exute_script(request_data):
#     try:
#         username = request_data['username']
#         task = Task.objects.get(id=request_data['id'])
#         tem = Host.objects.get(id=request_data['tem_id'])
#         ip_list = [{"ip": task.host, "bk_cloud_id": task.cloud_id}]
#         result = install_mysql_by_script(username, int(request_data['biz']), ip_list, tem.script)
#         task_detail = TaskDetail.objects.create(task=task, act_time=datetime.datetime.now(), check_host=task.host, describe=u"脚本执行异常")
#
#         if result["result"]:
#             success = 0
#             for re in result['data']:
#                 data = re["log_content"].split("=")[1]
#                 load = data.split("%")[0]
#                 if float(load) < float(task.tem.max_num):
#                     Export.objects.create(task_obj=task_detail, task_name=task.task_name, default_area=task.default_area,
#                                       host_ip=re['ip'], script=task.tem.script, max_num=task.tem.max_num,
#                                       result=load, is_normal=True)
#                     success += 1
#                 else:
#                     Export.objects.create(task_obj=task_detail, task_name=task.task_name,
#                                           default_area=task.default_area,
#                                           host_ip=re['ip'], script=task.tem.script, max_num=task.tem.max_num,
#                                           result=load)
#
#             task_detail.describe = u"本次共巡检%d台服务器，%d台存在异常"%(len(result['data']), len(result['data'])-success)
#             task_detail.save()
#
#         else:
#             for ip in ip_list:
#                 Export.objects.create(task_obj=task_detail, task_name=task.task_name,
#                                       default_area=task.default_area,
#                                       host_ip=ip['ip'], script=task.tem.script, max_num=task.tem.max_num,
#                                       result=u"异常")
#         return True
#     except Exception as e:
#         logger.error(e)
#
#
# @task()
# def set_time_exute_script(**kwargs):
#     try:
#         username = kwargs['username']
#         task = Task.objects.get(id=kwargs['id'])
#         tem = Host.objects.get(id=kwargs['tem_id'])
#         ip_list = [{"ip": task.host, "bk_cloud_id": task.cloud_id}]
#         result = install_mysql_by_script(username, int(kwargs['biz']), ip_list, tem.script)
#         now = datetime.datetime.now()
#         task_detail = TaskDetail.objects.create(task=task, act_time=now, check_host=task.host, describe=u"脚本执行异常")
#
#         if result["result"]:
#             success = 0
#             for re in result['data']:
#                 data = re["log_content"].split("=")[1]
#                 load = data.split("%")[0]
#                 if float(load) < float(task.tem.max_num):
#                     Export.objects.create(task_obj=task_detail, task_name=task.task_name, default_area=task.default_area,
#                                       host_ip=re['ip'], script=task.tem.script, max_num=task.tem.max_num,
#                                       result=load, is_normal=True)
#                     success += 1
#                 else:
#                     Export.objects.create(task_obj=task_detail, task_name=task.task_name,
#                                           default_area=task.default_area,
#                                           host_ip=re['ip'], script=task.tem.script, max_num=task.tem.max_num,
#                                           result=load)
#
#             task_detail.describe = u"本次共巡检%d台服务器，%d台存在异常"%(len(result['data']), len(result['data'])-success)
#             task_detail.save()
#
#         else:
#             for ip in ip_list:
#                 Export.objects.create(task_obj=task_detail, task_name=task.task_name,
#                                       default_area=task.default_area,
#                                       host_ip=ip['ip'], script=task.tem.script, max_num=task.tem.max_num,
#                                       result=u"异常")
#         return set_time_exute_script.apply_async(kwargs=kwargs, eta=now + datetime.timedelta(minutes=2))
#     except Exception as e:
#         logger.error(e)
#         return False