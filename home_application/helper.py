# -*- coding: utf-8 -*-
import datetime

from django.utils import timezone


# 把时间转成datetime格式
from home_application.models import Host


def to_datetime(str_date):
    str_date = str_date.replace("/", "-").strip()
    m_c = str_date.count(":")
    h_c = str_date.count("-")
    if m_c == 2:
        return datetime.datetime.strptime(str_date, '%Y-%m-%d %H:%M:%S')
    elif m_c == 1:
        return datetime.datetime.strptime(str_date, '%Y-%m-%d %H:%M')
    elif str_date.strip().count(" ") == 1:
        return datetime.datetime.strptime(str_date, '%Y-%m-%d %H')
    elif h_c == 2:
        return datetime.datetime.strptime(str_date, '%Y-%m-%d')
    elif h_c == 1:
        return datetime.datetime.strptime(str_date, '%Y-%m')
    else:
        return datetime.datetime.strptime(str_date, '%Y')


def to_str(datetime_code):
    return str(datetime_code).split(".")[0]


def time_now():
    return datetime.datetime.now()


def time_now_str():
    return time_now().strftime("%Y-%m-%d %H:%M:%S")


# 获取n分钟列表, ['15:44','15:45']
def get_categories_minutes(n):
    categories = []
    for i in xrange(0, n):
        categories.append((timezone.now() - datetime.timedelta(minutes=i)).strftime('%H:%M'))
    categories.reverse()
    return categories


# 获取n天列表, ['2019-03-04','2019-03-05']
def get_categories_days(n):
    categories = []
    for i in xrange(0, n):
        categories.append((timezone.now() - datetime.timedelta(days=i)).strftime('%Y-%m-%d'))
    categories.reverse()
    return categories


# 统计最近7天，每天的数目
def get_count():
    count = []
    for d in get_categories_days(7):
        start_time = d + " 00:00:00"
        end_time = d + " 23:59:59"
        #count.append(Host.objects.filter(when_created__gte=start_time, when_created__lte=end_time).count())

    return count






def get_create_operate_params(username, create_params):
    params = {
        'create_by': username,
        'modify_by': username,
        'create_time': time_now_str(),
        'modify_time': time_now_str()
    }
    create_params.update(params)
    return create_params


def get_modify_operate_params(username, update_params):
    params = {
        'modify_time': time_now_str(),
        'modify_by': username
    }
    update_params.update(params)
    return update_params






