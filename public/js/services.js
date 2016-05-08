'use strict';

angular.module('dtiApp.services', []).
  service('CompaniesService', ['$http', function($http) {
    var BASE_URL = "http://127.0.0.1:5000/api/companies";
    var companies = [];

    this.getData = function() {
      companies = $http.get(BASE_URL).data;
      console.log(companies);
    };
  }]);
