# -*- coding: utf-8 -*-
from blueking.component.shortcuts import get_client_by_user
from common.mymako import render_mako_context, render_json
from conf.default import APP_ID, APP_TOKEN
from esb_api import *
from sys_info import *
from chart_view import *
from other_helper import *

ERROR_MSG = {
    "result": False,
    "data": [u"系统异常，请联系管理员！"]
}


def home(request):
    """
    首页
    """
    return render_mako_context(request, '/home_application/js_factory.html')


# 简单返回
def test(request):
    try:
        return render_json({'result': True, 'username': request.user.username})
    except Exception as e:
        print e


# 获取当前应用相关信息
def app_detail(request):

    try:
        client = get_client_by_user(request.user.username)
        kwargs = {
            "bk_app_code": APP_ID,
            "bk_app_secret": APP_TOKEN,
            "bk_username": 'admin',
            "target_app_code": APP_ID,
            "fields": 'introduction;creator;developer',


        }
        result = client.bk_paas.get_app_info(kwargs)
        my_dict = {}
        if result["result"]:
            my_dict['message'] = result['message']
            my_dict['code'] = result['code']
            my_dict['data'] = [{'bk_app_code':result['data'][0]['bk_app_code'], "introduction": result['data'][0]['introduction'], "creator": result['data'][0]['creator'],"bk_app_name": result['data'][0]['bk_app_name'],"developer": result['data'][0]['developer']}]
            my_dict['result'] = result['result']
            my_dict['request_id'] = result['request_id']

        return render_json(my_dict)
    except Exception as e:
        print e