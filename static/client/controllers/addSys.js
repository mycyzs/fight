controllers.controller("addSys", ["$scope","loading","$modalInstance","msgModal","sysService","errorModal","$filter",function ( $scope,loading,$modalInstance,msgModal,sysService,errorModal,$filter) {
    $scope.title = "添加系统";
    $scope.args = {
        sys_name: "",
        biz_id:"",
        script:"",
        start_time:"",
        file_id:"",
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


    // 复选框选项

    $scope.ipList = [{id:1, ip: '0.0.0.0'}, {id:2, ip: '1.1.1.1'}];

    // 判断全选或者全不选
    $scope.check = function(){
        var box = document.getElementById("head_check");
        var suns = document.getElementsByName("son_check");
        if(box.checked == false){
            for (var i = 0; i < suns.length; i++) {
                   suns[i].checked = false;
                }
        }else {
           for (var i = 0; i < suns.length; i++) {
                   suns[i].checked = true;
                }
        }
    };

    // 每选择一个子节点检查 全选或全不选要不要打勾
    $scope.check_sum = function(){
        var box = document.getElementById("head_check");
        var suns = document.getElementsByName("son_check");
        var checked_host = [];
        for(var i = 0;i < suns.length; i++){
            if(suns[i].checked == true){
                checked_host.push(suns[i].value)
            }
        }
        if(suns.length == checked_host.length){
            box.checked = true
        }else {
            box.checked = false
        }
    };

    // 获取选择的复选框的value
     $scope.get_checked_ip = function () {
         var suns = document.getElementsByName("son_check");
         var checked_ip = [];
         for(var i = 0;i < suns.length; i++){
            if(suns[i].checked == true){
                checked_ip.push(suns[i].value)
            }
        }
     }


     // 时间控件
    var dateNow = new Date();
    var effective_time = dateNow.setDate(dateNow.getDate() + 365);
    // 把时间转成普通格式
    $scope.args.start_time = $filter('date')(effective_time, 'yyyy-MM-dd HH:mm');



     // 上传文件存入数据库
     $scope.upload_file = function () {

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
                    $scope.args.file_id = res.file_id;
                    msgModal.open("success", "上传成功");
                } else {
                    errorModal.open(res.data);
                }
            }
        });
    };


     // 从数据库读取文件下载到本地
    $scope.download_common_file = function () {
        window.open(site_url + 'download_common_file/');
    };



    // 确认提交
    $scope.confirm = function () {


        if ($scope.args.sys_name == '') {
            msgModal.open("error", "请输入系统名！");
            return
        }

        //请求后台函数存入数据
        loading.open();
        sysService.add_sys({}, $scope.args, function (res) {
            loading.close();
            if (res.result) {
                msgModal.open("success", "添加系统成功！！");
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