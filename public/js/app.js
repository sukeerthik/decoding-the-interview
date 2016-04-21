'use strict';

angular.module('dtiApp', [
  'ngRoute',
  'dtiApp.controllers',
  'dtiApp.services',
  'dtiApp.directives'
])
.config(function ($routeProvider) {
  $routeProvider
    .when('/', {
      templateUrl: '/partials/home.html',
      controller: 'homeCtrl'
    })
});
