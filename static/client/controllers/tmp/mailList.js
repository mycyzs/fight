controllers.controller("mailList", function ($scope, errorModal, $modal, loading, confirmModal, sysService, $filter) {
    $scope.data_list = [];
    var dateStart = new Date();
    var dateEnd = new Date();
    $scope.DateStart = dateStart.setDate(dateStart.getDate() - 29);
    $scope.DateEnd = dateEnd.setDate(dateEnd.getDate());
    $scope.args = {
        username: "",
        mailbox: "",
        whenStart: $filter('date')($scope.DateStart, 'yyyy-MM-dd'),
        whenEnd: $filter('date')($scope.DateEnd, 'yyyy-MM-dd HH:mm'),
        created_by: '00'
    };


    $scope.userList = [
        {id: '00', text: '全部'},
        {id: 'kido', text: 'kido'},
        {id: 'hannah', text: 'hannah'},
        {id: 'admin', text: 'admin'}
    ];

    $scope.search_mail = function () {
        loading.open();
        sysService.search_mail({}, $scope.args, function (res) {
            loading.close();
            if (res.result) {
                $scope.data_list = res.data;
                // 查询后更新分页数据
                $scope.pagingOptions.currentPage = 1;
                $scope.getPagedDataAsync($scope.pagingOptions.pageSize, $scope.pagingOptions.currentPage);
            }
            else {
                errorModal.open(res.data);
            }
        })
    };

    // 表格分页用 开始
    $scope.PagingData = [];
    $scope.totalSerItems = 0;

    $scope.pagingOptions = {
        pageSizes: [10, 50, 100],
        pageSize: "10",
        currentPage: 1
    };

    $scope.getPagedDataAsync = function (pageSize, page) {
        $scope.setPagingData($scope.data_list ? $scope.data_list : [], pageSize, page);

    };

    $scope.setPagingData = function (data, pageSize, page) {
        $scope.PagingData = data.slice((page - 1) * pageSize, page * pageSize);
        $scope.totalSerItems = data.length;
        if (!$scope.$$phase) {
            $scope.$apply();
        }
    };

    $scope.$watch('pagingOptions', function (newVal, oldVal) {
        $scope.getPagedDataAsync($scope.pagingOptions.pageSize, $scope.pagingOptions.currentPage);
    }, true);

    // 表格分页用 结束


    $scope.search_mail();
    //表格属性
    $scope.gridOption = {
        data: 'PagingData',
        enablePaging: true,
        showFooter: true,
        pagingOptions: $scope.pagingOptions,
        totalServerItems: 'totalSerItems',
        columnDefs: [
            {field: 'account', displayName: '用户名'},
            {field: 'mailbox', displayName: '邮箱地址'},
            {field: 'when_created', displayName: '添加时间'},
            {
                displayName: '操作', width: 180,
                cellTemplate: '<div style="width:100%;text-align: center;padding-top: 5px;z-index: 1">' +
                '<span ng-click="modify_mail(row)" class="label label-primary button-radius" style="min-width:50px;cursor:pointer;">修改</span>' +
                '<span ng-click="delete_mail(row)" class="label label-danger button-radius" style="min-width:50px;margin-left: 5px;cursor:pointer;">删除</span>' +
                '</div>'
            }

        ]
    };


    $scope.add_mail = function () {
        var modalInstance = $modal.open({
            templateUrl: static_url + 'client/views/tmp/mailAdd.html',
            windowClass: 'dialog_custom',
            controller: 'mailAdd',
            backdrop: 'static'
        });
        modalInstance.result.then(function (res) {
            $scope.search_mail();
        })
    };

    $scope.modify_mail = function (row) {
        var modalInstance = $modal.open({
            templateUrl: static_url + 'client/views/tmp/mailAdd.html',
            windowClass: 'dialog_custom',
            controller: 'mailModify',
            backdrop: 'static',
            resolve: {
                objItem: function () {
                    return angular.copy(row.entity);
                }
            }
        });
        modalInstance.result.then(function (res) {
            $scope.search_mail();
        })
    };

    $scope.delete_mail = function (row) {
        var id = row.entity.id;
        confirmModal.open({
            text: "确认删除该邮箱吗？",
            confirmClick: function () {
                loading.open();
                sysService.delete_mail({id: id}, {}, function (res) {
                    loading.close();
                    if (res.result) {
                        $scope.search_mail();
                    }
                    else {
                        errorModal.open(res.data.split(";"));
                    }
                })
            }
        })
    };


    $scope.openPage = function (rowEntity) {
        window.open('#/hostList?id=' + rowEntity.id);
    }
});



