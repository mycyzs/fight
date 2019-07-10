controllers.controller("chartList", function ($scope, loading, confirmModal, msgModal, sysService) {
    $scope.lineList = [];
    $scope.pieList = [];

    $scope.linechart = {
        data: "lineList",
        chart: {type: 'line'}, /*常用的线图为：line，柱状图为：column，横向柱状图为：bar，区域图为：area*/
        title: {text: '测试线图', enabled: true},
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

    $scope.piechart = {
        data: "pieList",
        title: {text: '问题严重程度统计', enabled: true},
        unit: "",
        size: "200px"
    };


    $scope.init = function () {
        sysService.get_chart_data({}, {}, function (res) {
            $scope.lineList = res.line_list;
            $scope.linechart.xAxis.categories = res.categories;
            $scope.pieList = res.pie_list;
        })
    }
    $scope.init();

    $scope.funModules = [
        {moduleName: '折线图', id: 1},
        {moduleName: '饼图', id: 2},
    ];
    $scope.moduleIndex = 1;
    $scope.changeFunModule = function (m) {
        $scope.moduleIndex = m.id;
    }


    // 多个线型图
    // $scope.dict={};
    // $scope.searchReport = function () {
    //     sysService.search_report({}, $scope.filter_args, function (res) {
    //         $scope.chart_list = [];
    //         if (res.result){
    //             $scope.data_list = res.data;
    //             for (var i=0;i<$scope.data_list.length;i++){
    //                 $scope.dict['abc' + i] = $scope.data_list[i].data;
    //                 $scope.list2.data = "dict.abc"+i;
    //                 $scope.list2.xAxis.categories = $scope.data_list[i].categories;
    //                 $scope.list2.title.text = $scope.data_list[i].data[0].name;
    //                 $scope.chart_list.push({"chart": angular.copy($scope.list2)})
    //             }




});
