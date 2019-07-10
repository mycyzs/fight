controllers.controller('serverDetail', function ($scope, $modalInstance, objItem) {
    $scope.title = "主机详情";
    $scope.hostObj = objItem.host;
    $scope.filterList = objItem.attrList;
    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    }
});