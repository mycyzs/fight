controllers.controller("body", ["$scope", "loading", "$modal", "confirmModal", "sysService", "errorModal", "msgModal", "$interval",function ($scope, loading, $modal, confirmModal, sysService, errorModal, msgModal, $interval) {

    $scope.args = {
        biz_id: ''
    }


    // 上传图片，展示图片相关
    //$scope.current_url = window.location.href.split('#')[0];

    $scope.choosePicMenu = function() {
                $('#photoBtn').click();
            }

    $scope.up_pic = function () {

        var file = document.getElementById("photoBtn").files[0];
        var xhr = new XMLHttpRequest();
        var url = site_url + 'upload_pic/?book_id=2';
        xhr.open('POST', url, true);
        xhr.setRequestHeader('X-CSRFToken', $("#csrf").val());
        xhr.setRequestHeader("Accept", "*/*");

        xhr.onload = function (e) {
            if (this.status == 200) {
                alert("上传图片成功!!")
                //window.location.reload()
                $scope.make_pic();
            }
        }
        xhr.send(file)
    }


    // 获取图片渲染到img标签
    $scope.make_pic = function(){
        var xmlhttp;
        xmlhttp=new XMLHttpRequest();
        xmlhttp.open("GET","get_background_img/?id=2",true);
        xmlhttp.responseType = "blob";
        xmlhttp.onload = function(){

        if (this.status == 200) {
            var blob = this.response;
            var img = document.getElementById("my_pic");
            img.onload = function(e) {
                window.URL.revokeObjectURL(img.src);
        };
            img.src = window.URL.createObjectURL(blob);
    }
};
        xmlhttp.send();
    };



    // 上传普通文件
    $scope.upload_field = function() {
                $('#uploadInfo').click();
            }
     $scope.uploadItem = function () {
          $scope.file_list = [];
        var fd = new FormData();
        var files = $("#uploadInfo").get(0).files;

        var name_path = "test_";
        fd.append("file_path", name_path);

        if (files[0].size > 10485760) {
                errorModal.open(["文件大小不能超过10M！"]);
                return;
            }
        // 限制上传文件的类型
        var file_name = files[0].name.toLowerCase();
            // if (files[i].name.split(".")[1] != 'txt') {
            //     errorModal.open(["只能上传.txt文件"]);
            //     $scope.file_list = [];
            //     return;
            // }

         fd.append("upfile", files[0]);

        $.ajax({
            url: site_url + "upload_info/?obj_id=1",
            type: "POST",
            processData: false,
            contentType: false,
            data: fd,
            success: function (res) {
                if (res.result) {
                    alert('上传文件成功')
                }
                else {
                    alert("上传文件失败")

                }
            }
        });
     }


     // 从static下载普通文件
    $scope.down_load_field = function () {
        window.open("down_load_field/?obj_id=1")
    }




    // 导入excel文件
    $scope.upload = function () {
        var modalInstance = $modal.open({
            templateUrl: static_url + 'client/views/up_file.html',
            windowClass: 'dialog_custom',
            controller: 'up_file',
            backdrop: 'static',
            resolve: {
                objectItem: function () {
                    return {obj_id: '1'}
                }
            }
        });
        modalInstance.result.then(function (res) {
                //导入成功后的动作，比如刷新页面等
        })
    }


    //导出excel文件
    $scope.down_excel = function () {
        window.open("down_excel/?obj_id=1")
    };




    // 导入csv文件
     $scope.uploadCsv = function () {
            CWApp.uploadCsv("uploadFile", callBack);
        };
        var callBack = function () {
            var content = fr.result;
            content = content.replace(new RegExp("\"", "gm"), "");
            var temp_list = [];
            var content_list = content.substring(0, content.lastIndexOf("\n")).split("\n");
            var column_len = content_list[0].split(",").length;
            var up_cvs = function (data) {
                loading.open();
                // 导入的后台方法
                sysService.up_csv({}, data, function (res) {
                    loading.close();
                    if (res.result) {
                        alert("上传成功")
                    }
                    else {
                        alert('上传失败')
                    }
                })
            }
            for (var i = 1; i < content_list.length; i++) {
                var device_obj = {};
                var columns = content_list[i].replace("\r", "").split(",");
                var a = columns.slice(0,8);
                var b = columns.slice(8);
                var device_obj = {
                    name: a[0],
                    age: a[1],
                    text: a[2]
                };
                temp_list.push(device_obj)
            }
            $scope.csvList = temp_list;
            // 开始请求后台方法
            up_cvs($scope.csvList)
        };


    //导出csv文件
    $scope.down_csv = function () {
        window.open("down_csv/?obj_id=1")
    };





}]);