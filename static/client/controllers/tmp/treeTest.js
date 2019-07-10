controllers.controller('treeTest', function ($scope, sysService) {

    $scope.topoList = [];
    $scope.init = function () {

        sysService.get_tree_data({}, {}, function (res) {
            $scope.topoList = res.data;
        });
    }

    $scope.init();
    $scope.zTreeOptions = {
        check: {
            enable: false
        },
        data: {
            key: {
                name: "display_name", // 树节点显示名字段
                children: "child", // 子节点存储字段
                isParent: "isParent"  // 是否存在子级
            }
        },
        onClick: function (event, treeId, treeNode) {
            //节点点击事件，treeNode代表节点对象，能够获取到整个节点的全部数据
            $scope.test(treeNode);
        },
        // onCheck:function (event, treeId, treeNode) {
        //
        // },
        // 获取子节点调用的接口
        // asyncUrl: site_url + 'get_tree_node_data/',
        // 接口参数，保持这种格式，左边的name是后台request.GET的字段，右边的name是对应要传的treeNode的字段
        // autoParam: ['name=name']
    };
    $scope.test = function (treeNode) {
        console.log(treeNode);
    }

});