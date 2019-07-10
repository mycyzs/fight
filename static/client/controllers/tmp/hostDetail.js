controllers.controller('hostDetail', function ($scope, $modalInstance, objItem) {
    $scope.hostObj = objItem.host;
    $scope.filterList = objItem.attrList;
    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    }
});