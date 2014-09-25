angular.module('app')

.controller('TablesCtrl', function ($scope, $location, $modal,
                                    ModelsListFactory, ModelDataFactory,
                                    ModelDataItemFactory) {
    // get list of models from api
    $scope.modelsList = ModelsListFactory.query();

    $scope.chooseModel = function (modelName) {
        $scope.currentModel = modelName;
        $scope.modelData = ModelDataFactory.get({modelName: modelName.name});
        if ($scope.modelData) {
            $scope.currentModel.available = true;
        };
    };

    $scope.isActive = function (modelName) {
        var active = $scope.currentModel === modelName;
        return active;
    };

    $scope.deleteItem = function(item) {
        var index = $scope.modelData.data.indexOf(item);
        ModelDataItemFactory.delete(
            {
                modelName: $scope.currentModel.name,
                id: item.id
            }
        );
        console.log(index);
        console.log($scope.modelData.data);
        $scope.modelData.data.splice(index, 1);
    };

    $scope.addItemModal = function () {
        var modalInstance = $modal.open({
            templateUrl: 'additem.html',
            controller: 'AdditemCtrl',
            resolve: {
                table: function () {
                    return $scope.modelData;
                },
                modelName: function() {
                    return $scope.currentModel;
                }
            }
        });
        modalInstance.result.then(function (item) {
            // save new item to database
            var new_item = ModelDataFactory.save(
                {modelName: $scope.currentModel.name},
                item
            );
            $scope.modelData.data.push(new_item);
        }, function () {
            console.log('Cancel');
        });
    };

    $scope.editItemModal = function (row) {
        var modalInstance = $modal.open({
            templateUrl: 'edititem.html',
            controller: 'EdititemCtrl',
            resolve: {
                table: function () {
                    return $scope.modelData;
                },
                modelName: function() {
                    return $scope.currentModel;
                },
                item: function() {
                    return row;
                }
            }
        });
        modalInstance.result.then(function (item) {
            // update item in database
            console.log(item);
            ModelDataItemFactory.update(
                {
                    modelName: $scope.currentModel.name,
                    id: item.id
                },
                item
            );
        }, function () {
            console.log('Cancel');
        });
    };

});
