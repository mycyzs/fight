services = angular.module('webApiService', ['ngResource', 'utilServices']);

var POST = "POST";
var GET = "GET";

services.factory('sysService', ['$resource', function ($resource) {
    return $resource(site_url + ':actionName/', {},
        {
            search_mail: {method: POST, params: {actionName: 'search_mail'}, isArray: false},
            add_mail: {method: POST, params: {actionName: 'add_mail'}, isArray: false},
            modify_mail: {method: POST, params: {actionName: 'modify_mail'}, isArray: false},
            delete_mail: {method: POST, params: {actionName: 'delete_mail'}, isArray: false},
            get_app_list: {method: POST, params: {actionName: 'get_app_list'}, isArray: false},
            get_server_list: {method: POST, params: {actionName: 'get_server_list'}, isArray: false},
            get_app_topo: {method: POST, params: {actionName: 'get_app_topo'}, isArray: false},
            search_server_list: {method: POST, params: {actionName: 'search_server_list'}, isArray: false},
            get_tree_data: {method: POST, params: {actionName: 'get_tree_data'}, isArray: false},



            // 以下添加路由
            get_all_biz: {method: POST, params: {actionName: 'get_all_biz'}, isArray: false},
            get_sys_info: {method: POST, params: {actionName: 'get_sys_info'}, isArray: false},
            add_sys: {method: POST, params: {actionName: 'add_sys'}, isArray: false},
            modify_sys: {method: POST, params: {actionName: 'modify_sys'}, isArray: false},
            delete_sys: {method: POST, params: {actionName: 'delete_sys'}, isArray: false},
            get_chart_data: {method: POST, params: {actionName: 'get_chart_data'}, isArray: false},
            get_host_attr: {method: POST, params: {actionName: 'get_host_attr'}, isArray: false},
            up_csv: {method: POST, params: {actionName: 'up_csv'}, isArray: false},
            get_host_by_biz: {method: POST, params: {actionName: 'get_host_by_biz'}, isArray: false},
            get_host_data: {method: POST, params: {actionName: 'get_host_data'}, isArray: false},
            check_ip: {method: POST, params: {actionName: 'check_ip'}, isArray: false},
            push_into_book: {method: POST, params: {actionName: 'push_into_book'}, isArray: false},
            delete_from_book: {method: POST, params: {actionName: 'delete_from_book'}, isArray: false},


            // 其他未调用接口
            get_all_user: {method: POST, params: {actionName: 'get_all_user'}, isArray: false},
            get_current_user: {method: POST, params: {actionName: 'get_current_user'}, isArray: false},
            get_host_info: {method: POST, params: {actionName: 'get_host_info'}, isArray: false},
            search_classifications: {method: POST, params: {actionName: 'search_classifications'}, isArray: false},
            search_all_objects: {method: POST, params: {actionName: 'search_all_objects'}, isArray: false},
            search_inst: {method: POST, params: {actionName: 'search_inst'}, isArray: false},
            search_inst_detail: {method: POST, params: {actionName: 'search_inst_detail'}, isArray: false},
            get_agent_status: {method: POST, params: {actionName: 'get_agent_status'}, isArray: false},
            get_job_detail: {method: POST, params: {actionName: 'get_job_detail'}, isArray: false},

        }
    )
}])


;//这是结束符，请勿删除