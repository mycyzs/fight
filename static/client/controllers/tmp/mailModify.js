controllers.controller('mailModify', function ($scope, sysService, errorModal, $modalInstance, loading, objItem) {
    $scope.title = "修改管理员邮箱";
    $scope.serverList = [];
    $scope.appList = [];
    $scope.args = objItem;
    $scope.searchApp = function () {
        sysService.get_app_list({}, {}, function (res) {
            $scope.appList = res.data;
            $scope.changeApp();
        })
    };

    $scope.searchApp();

    $scope.changeApp = function () {
        sysService.get_server_list({app_id: $scope.args.app_id}, {}, function (res) {
            $scope.serverList = res.data;
        })
    }
    $scope.confirm = function () {
        loading.open();
        sysService.modify_mail({}, $scope.args, function (res) {
            loading.close();
            if (res.result) {
                $modalInstance.close($scope.args);
            }
            else {
                errorModal.open(res.data);
            }
        })
    };
    $scope.cancel = function () {
        $modalInstance.dismiss("cancel");
    };
});