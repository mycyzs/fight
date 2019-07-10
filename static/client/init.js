var app = angular.module("myApp", ['myController', 'utilServices', 'myDirective', 'ui.bootstrap', 'ui.router', 'webApiService','cwLeftMenu','ngGrid']);
var controllers = angular.module("myController", []);
var directives = angular.module("myDirective", []);


app.config(["$stateProvider", "$urlRouterProvider", "$httpProvider", function ($stateProvider, $urlRouterProvider, $httpProvider) {
    $httpProvider.defaults.headers.post['X-CSRFToken'] = $("#csrf").val();
    $urlRouterProvider.otherwise("/home");//默认展示页面
    $stateProvider.state('home', {
        url: "/home",
        controller: "home",
        templateUrl: static_url + "client/views/home.html"
    })
    .state('chartList', {
        url: "/chartList",
        controller: "chartList",
        templateUrl: static_url + "client/views/chartList.html"
    })
    .state('host_detail', {
            url: "/host_detail?id",
            controller: "host_detail",
            templateUrl: static_url + "client/views/host_detail.html"
        })

    .state('hostList', {
        url: "/hostList",
        controller: "hostList",
        templateUrl: static_url + "client/views/hostList.html"
    })
    .state('body', {
        url: "/body",
        controller: "body",
        templateUrl: static_url + "client/views/body.html"
    })
    .state('host_status', {
        url: "/host_status",
        controller: "host_status",
        templateUrl: static_url + "client/views/host_status.html"
    })
}]);


