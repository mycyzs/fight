# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns(
    'home_application.views',
    (r'^$', 'home'),
    (r'^api/test$', 'app_detail'),
    (r'^get_all_biz$', 'get_all_biz'),    # 获取所有业务 ，返回[{"id": 2, "text": "蓝鲸"}]
    (r'^get_sys_info$', 'get_sys_info'),
    (r'^add_sys$', 'add_sys'),
    (r'^modify_sys$', 'modify_sys'),
    (r'^delete_sys$', 'delete_sys'),
    (r'^get_chart_data$', 'get_chart_data'),
    (r'^get_host_attr$', 'get_host_attr'),
    (r'^search_server_list$', 'search_server_list'),
    (r'^get_app_topo$', 'get_all_app_topo'),
    (r'^get_host_by_biz$', 'get_host_by_biz'),   # 获取业务下的所有主机 ，返回[{"id": '1.1', "text": "蓝1.1","biz_id": 2,"cloud_id": 0}]
    (r'^get_host_data$', 'get_host_data'),
    (r'^check_ip$', 'check_ip'),
    (r'^push_into_book$', 'push_into_book'),
    (r'^delete_from_book$', 'delete_from_book'),


    # 未调用的接口
    (r'^get_all_user$', 'get_all_user'),
    (r'^get_current_user$', 'get_current_user'),
    (r'^get_host_info$', 'get_host_info'),
    (r'^search_classifications$', 'search_classifications'),
    (r'^search_all_objects$', 'search_all_objects'),
    (r'^search_inst$', 'search_inst'),
    (r'^search_inst_detail$', 'search_inst_detail'),
    (r'^get_agent_status$', 'get_agent_status'),
    (r'^get_job_detail$', 'get_job_detail'),


    # 额外的路由

    # 上传普通文件存入数据库，从数据库读取普通文件下载到本地
    (r'^upload_file/$', 'upload_file'),
    (r'^download_common_file/$', 'download_common_file'),

    # 上传图片
    (r'^upload_pic/$', 'upload_pic'),
    (r'^get_background_img/$', 'get_background_img'),

    # (r'^upload_info/$', 'upload_info'),
    # (r'^down_load_field/$', 'down_load_field'),

    # 导入、导出excel文件
    (r'^up_excel/$', 'up_excel'),
    (r'^down_excel/$', 'down_excel'),

    # 导入、导出csv
    (r'^down_csv/$', 'down_csv'),
    (r'^up_csv$', 'up_csv'),
    # (r'^search_topo$', 'search_topo_by_biz'),
    # (r'^search_host_by_node$', 'search_host_by_node'),
)


# 考试把下面的删除即可
# try:
#     from home_application.tmp.urls import tmp_url
#
#     urlpatterns += tmp_url
# except:
#     pass
