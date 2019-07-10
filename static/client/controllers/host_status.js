controllers.controller("host_status", ["$scope", "loading", "$modal", "confirmModal", "sysService", "errorModal", "msgModal", "$interval",function ($scope, loading, $modal, confirmModal, sysService, errorModal, msgModal, $interval) {

    $scope.args = {
        biz_id: '',
        host_ip: ''
    }
    // 获取所有业务
    $scope.bizList = [];
    $scope.get_all_biz = function () {
        loading.open();
        sysService.get_all_biz({}, {}, function (res) {
            loading.close();
            if(res.result){
                $scope.bizList = res.data
                $scope.args.biz_id = res.data[0]['id']
                $scope.get_host_by_biz();
            }
        })
    };
    $scope.get_all_biz();

    $scope.bizOption = {
        data: "bizList",
        multiple: false,
    };


    // 获取业务下所有主机
    $scope.hostList = [];
    $scope.get_host_by_biz = function () {
        loading.open();
        sysService.get_host_by_biz({}, $scope.args, function (res) {
            loading.close();
            if(res.result){
                $scope.hostList = res.data

            }
        })
    }

    $scope.hostOption = {
        data: "hostList",
        multiple: false,
    };


    $scope.biz_change = function () {
        $scope.get_host_by_biz()
    }

    $scope.host = {}
    $scope.host_change = function () {
        angular.forEach($scope.hostList,function (m) {
            if(m.id == $scope.args.host_ip){
                $scope.host = m
                $scope.check_ip()

            }
        })


    }


    // 检查ip是否在周期表，在：显示移除，否：显示加入
    $scope.check_ip = function(){
        sysService.check_ip({}, $scope.host, function (res) {
            if(res.result){
                $scope.need_poll = 0
                $scope.get_chart_data()
            }else {
                $scope.need_poll = 1
            }
        })
    };


    $scope.linechart = {
        data: "lineList",
        chart: {type: 'line'}, /*常用的线图为：line，柱状图为：column，横向柱状图为：bar，区域图为：area*/
        title: {text: '主机状态', enabled: true},
        xAxis: {
            categories: []
        },
        plotOptions: {
            boxplot: {
                pointPadding: 0
            }
        },
        //提示框位置和显示内容
        tooltip: {
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
            '<td style="padding:0"><b>{point.y:f}</b></td></tr>',
            headerFormat: ""
        }
    };


    $scope.get_chart_data = function () {
        loading.open();
        sysService.get_host_data({}, $scope.host, function (res) {
            loading.close();
            if(res.result){
                $scope.lineList = res.line_list;
                $scope.linechart.xAxis.categories = res.categories;

            }
        })
    }

    // 加入周期
    $scope.push_into_book = function () {
        loading.open();
        sysService.push_into_book({}, $scope.host, function (res) {
            loading.close();
            if(res.result){
                alert('加入周期成功')
                $scope.need_poll = 0
            }else{
                alert('加入周期失败')
            }
        })
    }

    // 移除主机
    $scope.delete_from_book = function () {
        loading.open();
        sysService.delete_from_book({}, $scope.host, function (res) {
            loading.close();
            if(res.result){
                alert('移除主机成功')
                $scope.need_poll = 1
            }else{
                alert('移除主机失败')
            }
        })
    }





}]);