'use strict';

angular.module('dtiApp.controllers', []).
  controller('HomeCtrl', function ($scope) {
    // TODO
  }).
  controller("LineCtrl", ['$scope', function ($scope) {
    $scope.labels = ["January", "February", "March", "April", "May", "June", "July"];
    $scope.series = ['Label']
    $scope.data = [[65, 59, 80, 81, 56, 55, 40]];
  }]).
  controller("PieCtrl", ['$scope', function ($scope) {
    $scope.labels = ["Negative", "Neutral", "Positive"];
    $scope.data = [30, 50, 250];
  }]).
  controller('AboutCtrl', function ($scope) {
    // TODO ... later
  }).
  controller('OverviewCtrl', function($scope) {
    // TODO
  });
