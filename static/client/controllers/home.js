controllers.controller("home", ["$scope", "loading", "$modal", "confirmModal", "sysService", "errorModal", "msgModal","$filter", function ($scope, loading, $modal, confirmModal, sysService, errorModal, msgModal, $filter) {

    // 初始变量
    $scope.args = {
        sys_name: "",
        sys_code: "",
        biz_id: "",
        start_time: "",
    };


    //表格设置，内容显示页数和数量
    $scope.PagingData = [];
    $scope.totalSerItems = 0;

    $scope.pagingOptions = {
        pageSizes: [10, 50, 100],
        pageSize: "10",
        currentPage: 1
    };



    // 所有业务
    $scope.bizList = [];
    $scope.get_all_biz = function () {
        loading.open();
        sysService.get_all_biz({}, {}, function (res) {
            loading.close();
            if(res.result){
                $scope.bizList = res.data
            }
        })
    };
    $scope.get_all_biz();

    $scope.bizOption = {
        data: "bizList",
        multiple: false,
    };


     // 时间控件
    var dateNow = new Date();
    var effective_time = dateNow.setDate(dateNow.getDate() + 365);
    // 把时间转成普通格式
    $scope.args.start_time = $filter('date')(effective_time, 'yyyy-MM-dd HH:mm:ss');



    // 表格方法
    $scope.setPagingData = function (data, pageSize, page) {
        $scope.PagingData = data.slice((page - 1) * pageSize, page * pageSize);
        $scope.totalSerItems = data.length;
        if (!$scope.$$phase) {
            $scope.$apply();
        }
    };
    $scope.getPagedDataAsync = function (pageSize, page) {
        $scope.setPagingData($scope.hostList ? $scope.hostList : [], pageSize, page);
    };

    //查询系统表
    $scope.hostList = [];
    $scope.get_sys_info = function () {
        loading.open();
        sysService.get_sys_info({}, $scope.args, function (res) {
            loading.close();
            if (res.result) {
                $scope.hostList = res.data;
                $scope.pagingOptions.currentPage = 1;
                $scope.getPagedDataAsync($scope.pagingOptions.pageSize, $scope.pagingOptions.currentPage);
            } else {
                errorModal.open(res.msg);
            }
        })
    };
    $scope.get_sys_info();


    $scope.$watch('pagingOptions', function (newVal, oldVal) {
        $scope.getPagedDataAsync($scope.pagingOptions.pageSize, $scope.pagingOptions.currentPage);
    }, true);


    // 添加系统信息
    $scope.add_sys = function () {
        var modalInstance = $modal.open({
            templateUrl: static_url + 'client/views/addsys.html',
            windowClass: 'dialog_custom',
            controller: 'addSys',
            backdrop: 'static'
        });
        modalInstance.result.then(function (res) {
            $scope.hostList.unshift(res);
            $scope.getPagedDataAsync($scope.pagingOptions.pageSize, $scope.pagingOptions.currentPage);
        })
    };


    //修改系统信息
    $scope.modify_sys = function (row) {
        var modalInstance = $modal.open({
            templateUrl: static_url + 'client/views/addsys.html',
            windowClass: 'dialog_custom',
            controller: 'modifySys',
            backdrop: 'static',
            resolve: {
                objectItem: function () {
                    return row.entity;
                }
            }
        });
        modalInstance.result.then(function (res) {
            row.entity.sys_name = res.sys_name;
            row.entity.sys_code = res.sys_code;
            row.entity.owners = res.owners;
            row.entity.is_control = res.is_control;
            row.entity.department = res.department;
            row.entity.comment = res.comment;
        })
    };


    //删除系统
    $scope.delete_sys = function (row) {
        //根据id删除系统
        var id = row.entity.id;
        confirmModal.open({
            text: "确定删除该系统吗？",
            confirmClick: function () {
                loading.open();
                sysService.delete_sys({}, {id: id}, function (res) {
                    loading.close();
                    if (res.result) {
                        $scope.hostList.splice(row.rowIndex, 1);

                        //更新这一行的信息
                        //$scope.hostList[row.rowIndex] = res.data

                        msgModal.open("success", "删除系统成功！");
                        $scope.getPagedDataAsync($scope.pagingOptions.pageSize, $scope.pagingOptions.currentPage);
                    }
                    else {
                        errorModal.open(res.message);
                    }
                })
            }
        });

    };


    // 表格控件
    $scope.gridOption = {
        data: "PagingData",
        enablePaging: true,
        enableColumnResize: true,
        showFooter: true,
        pagingOptions: $scope.pagingOptions,
        totalServerItems: 'totalSerItems',
        columnDefs: [
            {field: "sys_name", displayName: "系统名", width: 160},
            {field: "sys_code", displayName: "系统简称", width: 140},
            {field: "owners", displayName: "负责人", width: 180},
            {field: "is_control", displayName: "是否权限控制", width: 160},
            {field: "department", displayName: "所属产品线", width: 160},
            {field: "comment", displayName: "备注", width: 180},
            {
                displayName: "操作",
                cellTemplate: '<div style="width:100%;padding-top:5px;text-align: center">' +
                '<span style="cursor: pointer" class="btn btn-xs btn-primary" ng-click="modify_sys(row)">修改</span>' +
                '<span style="cursor: pointer;margin-left: 5px" class="btn btn-xs btn-danger" ng-click="delete_sys(row)">删除</span>' +
                '<span ng-if="row.entity.id == 1" style="cursor: pointer;margin-left: 5px" class="btn btn-xs btn-danger" ui-sref="host_detail({id:row.entity.id})">详情跳转1</span>' +
                '<span ng-if="row.entity.id == 2" style="cursor: pointer;margin-left: 5px" class="btn btn-xs btn-danger" ui-sref="host_detail({id:row.entity.id})">详情跳转2</span>' +
                '</div>'
            }
        ]
    };

}]);