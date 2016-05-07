'use strict';

angular.module('dtiApp', [
  'ngRoute',
  'chart.js',
  'dtiApp.controllers',
  'dtiApp.services',
  'dtiApp.directives'
])
.config(function ($routeProvider, $locationProvider) {
  $routeProvider.
    when('/', {
      templateUrl: './public/partials/home.html',
      controller: 'HomeCtrl'
    }).
    when('/about', {
      templateUrl: './public/partials/about.html',
      controller: 'AboutCtrl'
    }).
    when('/overview', {
      templateUrl: './public/partials/overview.html',
      controller: 'OverviewCtrl'
    }).
    otherwise({redirectTo: '/'});

  // $locationProvider.html5Mode(true);
});
