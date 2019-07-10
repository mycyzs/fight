controllers.controller("site", ["$scope", function ($scope) {
    $scope.isShowLeft = false;
    $scope.menuList = [
        {
            id: 1, displayName: "首页", iconClass: "fa fa-home fa-lg", url: "#/home"
        },
        {
            id: 2, displayName: "Chart", iconClass: "fa fa-cog fa-lg",
            children: [
                {id: 3, displayName: "图表管理", url: "#/chartList"},
            ]
        },
        {
            id: 4, displayName: "主机资源", iconClass: "fa fa-cog fa-lg", url: "#/hostList"
        },
        {
            id: 5, displayName: "BODY", iconClass: "fa fa-cog fa-lg", url: "#/body"
        },
        {
            id: 5, displayName: "主机状态", iconClass: "fa fa-cog fa-lg", url: "#/host_status"
        }
    ];


    $scope.menuOption = {
        data: 'menuList',
        locationPlaceHolder: '#locationPlaceHolder',
        adaptBodyHeight: CWApp.HeaderHeight + CWApp.FooterHeight
    };

    var url = window.location.href.split("#/");
    $scope.pageUrl = "#/home";
    if (url.length !== 0) {
        $scope.pageUrl = "#/" + url[1];
    }
    $scope.goToUrl = function (i) {
        $scope.pageUrl = i;
    }
}]);