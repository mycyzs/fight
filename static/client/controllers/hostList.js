controllers.controller('hostList', function ($scope, sysService, loading, $filter, $modal) {
    $scope.appList = [];
    $scope.args = {
        app_id: ''
    };
    $scope.allServer = [];
    $scope.serverList = [];
    $scope.filterObj = {value: ''};
    $scope.attrList = [];
    $scope.select_attr = {value: ''};

    $scope.get_all_biz = function () {
        sysService.get_all_biz({}, {}, function (res) {
            $scope.appList = res.data;
            // 默认选取第一个业务
            $scope.args.app_id = res.data[0].id;
            $scope.changeApp();
        })
    };
    $scope.get_all_biz();

    $scope.businessTopo = [];

    // 切换业务查询主机，以及topo树
    $scope.changeApp = function () {
        $scope.searchServer({bk_obj_id: 'biz', bk_inst_id: $scope.args.app_id});
        sysService.get_app_topo({app_id: $scope.args.app_id}, {}, function (res) {
            $scope.businessTopo = res.data;
        })
    };

    // 查询主机所有属性
    $scope.searchAttr = function () {
        sysService.get_host_attr({}, {}, function (res) {
            $scope.attrList = res.data;
        })
    };
    $scope.searchAttr();


    // 树形topo组件
    $scope.zTreeOptions = {
        check: {
            enable: false
        },
        data: {
            key: {
                // 显示的字段
                name: "bk_inst_name",
                children: "child",
                isParent: "isParent"
            }
        },
        onClick: function (event, treeId, treeNode) {
            $scope.searchServer(treeNode)
        }
    };


    // 根据点击树形节点或者切换业务查询所有的主机
    $scope.searchServer = function (treeNode) {
        sysService.search_server_list({
            bk_biz_id: $scope.args.app_id
        }, {
            bk_obj_id: treeNode.bk_obj_id,
            value: treeNode.bk_inst_id
        }, function (res) {
            $scope.allServer = angular.copy(res.data);
            $scope.filterServer();
        })
    };

    // 根据属性过滤主机，不重新查询接口 ，$filter
    $scope.filterServer = function () {
        if ($scope.select_attr.value === '') {
            $scope.serverList = angular.copy($scope.allServer)
        }
        else {
            // 循环主机列表，有该属性值的主机则返回
            $scope.serverList = $filter('filter')($scope.allServer, function (i) {
                if (i[$scope.select_attr.value] == undefined || i[$scope.select_attr.value] == null)
                    return false;
                return i[$scope.select_attr.value].indexOf($scope.filterObj.value) > -1
            })
        }
    };

    $scope.openDetail = function (rowEntity) {
        var modalInstance = $modal.open({
            templateUrl: static_url + 'client/views/serverDetail.html',
            windowClass: 'dialog_custom',
            controller: 'serverDetail',
            backdrop: 'static',
            resolve: {
                objItem: function () {
                    return {
                        host: angular.copy(rowEntity),
                        attrList: $scope.attrList
                    };
                }
            }
        });
    }


    // ServerList
    $scope.gridOption = {
        data: 'serverList',
        columnDefs: [
            {field: 'bk_host_innerip', displayName: 'IP'},
            {field: 'bk_os_type', displayName: '操作系统类型'},
            {field: 'bk_os_version', displayName: '操作系统版本'},
            {
                displayName: '操作', width: 180,
                cellTemplate: '<div style="width:100%;text-align: center;padding-top: 5px;z-index: 1">' +
                '<span ng-click="openDetail(row.entity)" class="label label-primary button-radius" style="min-width:50px;cursor:pointer;">详情</span>' +
                '</div>'
            }
        ]
    };
});