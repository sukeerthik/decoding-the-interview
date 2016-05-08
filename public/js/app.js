'use strict';

angular.module('dtiApp', [
  'ngRoute',
  'chart.js',
  'dtiApp.services',
  'dtiApp.directives',
  'dtiApp.controllers'
]).
config(function ($routeProvider, $locationProvider) {
  $routeProvider.
    when('/', {
      templateUrl: './public/partials/home.html',
      controller: 'HomeCtrl'
    }).
    when('/about', {
      templateUrl: './public/partials/about.html',
      controller: 'AboutCtrl'
    }).
    when('/overview/:id', {
      templateUrl: './public/partials/overview.html',
      controller: 'OverviewCtrl'
    }).
    otherwise({redirectTo: '/'});

  // $locationProvider.html5Mode(true);
}).
config(['ChartJsProvider', function (ChartJsProvider) {
  // Configure all line charts
  ChartJsProvider.setOptions({
    datasetFill: false
  });
  ChartJsProvider.setOptions('doughnut', {
    chartColors: ['#ef5350', '#d4e157', '#66bb6a']
  });
  // $locationProvider.html5Mode(true);
}]);
