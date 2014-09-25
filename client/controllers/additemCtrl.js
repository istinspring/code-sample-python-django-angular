angular.module('app')

.controller('AdditemCtrl', function ($scope, $filter, $modalInstance, table, modelName) {
    $scope.table = table;
    $scope.item = {};

    $scope.dateOptions = {
        formatYear: 'yyyy',
        startingDay: 1
    };

    $scope.dpopen = function($event) {
        $event.preventDefault();
        $event.stopPropagation();
        $scope.dtpopened = true;
    };

    $scope.isEditable = function (field) {
        return (field === "id") ? false : true;
    };

    $scope.isDateType = function (field) {
        return (table.types[field] === "DateField") ? true : false;
    };

    $scope.isIntType = function (field) {
        return (table.types[field] === "IntegerField") ? true : false;
    };

    $scope.ok = function () {
        // issue with ui datepicker, write raw Date() object into model
        angular.forEach($scope.item, function(value, key) {
            if (key === 'date') {
                var new_date = $filter('date')(value, "yyyy-MM-dd");
                $scope.item[key] = new_date;
            };
        });
        $modalInstance.close($scope.item);
    };

    $scope.cancel = function () {
        $modalInstance.dismiss('cancel');
    };
});
