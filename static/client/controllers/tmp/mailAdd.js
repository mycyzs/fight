controllers.controller('mailAdd', function ($scope, sysService, errorModal, $modalInstance, loading) {
    $scope.title = "添加管理员邮箱";
    $scope.appList = [];
    $scope.serverList = [];
    $scope.args = {
        account: '', mailbox: '', app_id: '', app_name: '',
        server_id: '', server_list: ''
    };


    // select2初始用法
    $scope.appOption = {
        data: 'appList',
        multiple: false,
        modelData: 'args.app_id'
    };


    $scope.changeApp = function () {
        sysService.get_server_list({app_id: $scope.args.app_id}, {}, function (res) {
            $scope.serverList = res.data;
        })
    };
    $scope.searchApp = function () {
        sysService.get_app_list({}, {}, function (res) {
            $scope.appList = res.data;
            if (res.data.length > 0) {
                $scope.args.app_id = res.data[0].id;
                $scope.changeApp();
            }
        })
    };


    $scope.searchApp();

    $scope.confirm = function () {
        loading.open();
        sysService.add_mail({}, $scope.args, function (res) {
            loading.close();
            if (res.result) {
                $modalInstance.close(res.data);
            }
            else {
                errorModal.open(res.data);
            }
        })
    };
    $scope.cancel = function () {
        $modalInstance.dismiss("cancel");
    };

    $scope.upload_img = function () {
        var fd = new FormData();
        fd.append("upfile", $("#uploadFile").get(0).files[0]);
        loading.open();
        $.ajax({
            url: site_url + "upload_file/",
            type: "POST",
            processData: false,
            contentType: false,
            data: fd,
            success: function (res) {
                loading.close();
                if (res.result) {
                    msgModal.open("success", "上传成功");
                } else {
                    errorModal.open(res.data);
                }
            }
        });
    };

    $scope.downloadTemp = function () {
        window.open(site_url + 'download_temp/');
    };
});