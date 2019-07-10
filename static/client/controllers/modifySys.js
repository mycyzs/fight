controllers.controller("modifySys", ["$scope","loading","$modalInstance","msgModal","objectItem","sysService","errorModal",function ( $scope,loading,$modalInstance,msgModal,objectItem,sysService,errorModal) {
    $scope.title = "修改系统信息";
    $scope.args = {
        id:objectItem.id,
        sys_name: objectItem.sys_name,
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

    // multiple为true则是多选
    $scope.bizOption = {
        data: "bizList",
        multiple: false,
        modelData: ""
    };

    $scope.confirm = function () {
        if ($scope.args.sys_name == '') {
            msgModal.open("error", "请输入系统名！");
            return
        }

        //请求后台函数存入数据
         loading.open();
         sysService.modify_sys({}, $scope.args, function (res) {
             loading.close();
             if (res.result) {
                 msgModal.open("success", "修改成功！！");
                 $modalInstance.close(res.data);
             }
             else {
                 errorModal.open(res.msg);
             }
         })
    };

    $scope.cancel = function () {
        $modalInstance.dismiss("cancel");
    };








}]);