# -*- coding: utf-8 -*-
from common.mymako import render_json


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