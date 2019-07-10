# -*- coding: utf-8 -*-
from django.conf.urls import patterns

tmp_url = patterns(
    'home_application.tmp.views',
    (r'^/api/test/$', 'test'),
    (r'^search_mail$', 'search_mail'),
    (r'^add_mail$', 'add_mail'),
    (r'^modify_mail$', 'modify_mail'),
    (r'^delete_mail$', 'delete_mail'),
    (r'^get_chart_data$', 'get_chart_data'),
    (r'^get_app_list$', 'get_app_list'),
    (r'^get_server_list$', 'get_server_list'),
    (r'^get_app_topo$', 'get_app_topo'),
    (r'^search_server_list$', 'search_server_list'),
    (r'^get_host_attr$', 'get_host_attr'),
    (r'^get_tree_data$', 'get_tree_data'),
    (r'^get_tree_node_data/$', 'get_tree_node_data'),
    (r'^upload_file/$', 'upload_file'),
    (r'^download_temp/$', 'download_temp'),
)
