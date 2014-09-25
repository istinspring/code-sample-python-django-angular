angular.module('app', [
    'ngAnimate', 'ngResource', 'ngRoute', 'ui.bootstrap'
])

.config(function ($routeProvider, $locationProvider) {
    $routeProvider
        .when('/', {
            templateUrl: 'tables.html',
            controller: 'TablesCtrl'
        })
        .when('/about', {
            templateUrl: 'about.html',
            controller: 'AboutCtrl'
        })
        .when('/contacts', {
            templateUrl: 'contacts.html',
            controller: 'ContactsCtrl'
        })
        .otherwise({
            redirectTo: '/'
        });

    $locationProvider.html5Mode(true);
    $locationProvider.hashPrefix('!');
})

.config(function($provide){
    // Monkey patch for ui-bootstrap datepicker
    // (lazy fags still can't put new build on bower)
    $provide.decorator('dateParser', function($delegate){

        var oldParse = $delegate.parse;
        $delegate.parse = function(input, format) {
            if ( !angular.isString(input) || !format ) {
                return input;
            }
            return oldParse.apply(this, arguments);
        };

        return $delegate;
    });
})

.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';    }
])

.factory('ModelsListFactory', function($resource) {
    return $resource('/api/models');
})

.factory('ModelDataFactory', function($resource) {
    return $resource(
        '/api/models/:modelName',
        null,
        {
            'get':    {method:'GET'},
            'save':   {method:'POST'},
            'query':  {method:'GET', isArray:true},
        }
    )
})

.factory('ModelDataItemFactory', function($resource) {
    return $resource(
        '/api/models/:modelName/item/:id',
        null,
        {
            'update': {method: 'PUT'},
            'remove': {method:'DELETE'},
            'delete': {method:'DELETE'}
        }
    )
})

/*
.controller('ContentCtrl', function ($scope, $rootScope, $location, $modal, ModelDataFactory) {
    $rootScope.$on("currentModel", function(event, currentModel) {
        $scope.currentModel = currentModel;
        $scope.modelData = ModelDataFactory.get({modelName: $scope.currentModel.name});
    });

    $scope.editingRow = -1
    $scope.editRow = function (row) {
        $scope.editingRow = row.id;
    };

    $scope.isEditEnabled = function (row, col) {
        var by_row = (row.id === $scope.editingRow) ? true : false;
        var by_field = (col === 'id') ? false : true;
        return by_row && by_field;
    };

    $scope.isDateType = function (col) {
        return ($scope.modelData.types[col] === "DateField") ? true : false;
    };

    $scope.open = function($event) {
        $event.preventDefault();
        $event.stopPropagation();

        $scope.opened = true;
    };

    $scope.dateOptions = {
        formatYear: 'yyyy',
        startingDay: 1
    };

})
*/
