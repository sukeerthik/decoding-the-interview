'use strict';

angular.module('dtiApp.controllers', []).
  service('CompaniesService', ['$http', function($http) {
    var BASE_URL = "http://127.0.0.1:5000/api/companies/";

    this.getData = function(id, callback) {
      $http({
        method: 'GET',
        url: BASE_URL + id
      }).
      success(function (res) {
        callback(res.data);
      });
    };
  }]).
  service('AnalysisService', ['$http', function($http) {
    var BASE_URL = "http://127.0.0.1:5000/api/analysis/";

    this.getData = function(id, callback) {
      $http({
        method: 'GET',
        url: BASE_URL + id
      }).
      success(function (res) {
        callback(res.data);
      });
    };
  }]).
  service('ReviewsService', ['$http', function($http) {
    var BASE_URL = "http://127.0.0.1:5000/api/reviews/";

    this.getData = function(id, callback) {
      $http({
        method: 'GET',
        url: BASE_URL
        // params: { "companyId": { "$oid" : "5729a2445dc5711e246a87b5"}}
      }).
      success(function (res) {
        callback(res.data);
      });
    };
  }]).
  controller('HomeCtrl', ['$scope', 'CompaniesService', function ($scope, CompaniesService) {
    $scope.companies = [];
    CompaniesService.getData("", function(res) {
      for (var i = 0; i < res.length; i++) {
        $scope.companies.push(JSON.parse(res[i]));

        // Short term fix for Glassdoor API giving us the wrong name of Epic Systems
        if ($scope.companies[i].name == "EPIC Systems (Egypt)") {
          $scope.companies[i].name = "Epic Systems";
        }
      }
      console.log($scope.companies);
    });
  }]).
  controller("LineCtrl", ['$scope', function ($scope) {
    $scope.labels = ["1/2015", "2/2015", "3/2015", "4/2015", "5/2015", "6/2015", "7/2015", "8/2015", "9/2015", "10/2015", "11/2015", "12/2015"];
    $scope.series = ['Label']
    $scope.data = [[0.4, 0.3, 0.2, -0.2, -0.1, 0.3, 0.4, 0.5, 0.3, -0.3, -0.5, -0.6]];
  }]).
  controller("PieCtrl", ['$scope', function ($scope) {
    $scope.labels = ["Negative", "Neutral", "Positive"];
    $scope.data = [300, 220, 470];
  }]).
  controller('AboutCtrl', function ($scope) {
    // TODO
  }).
  controller('OverviewCtrl', ['$scope', '$routeParams', 'CompaniesService', 'AnalysisService', 'ReviewsService', function($scope, $routeParams, CompaniesService, AnalysisService, ReviewsService) {
    $scope.id = $routeParams.id;
    $scope.company = [];
    $scope.analysis = [];
    $scope.reviews = [];
    CompaniesService.getData($scope.id, function(res) {
      $scope.company = JSON.parse(res);
      // Short term fix for Glassdoor API giving us the wrong name of Epic Systems
      if ($scope.company.name == "EPIC Systems (Egypt)") {
        $scope.company.name = "Epic Systems";
      }
      // console.log($scope.company);
    });
    AnalysisService.getData($scope.id, function(res) {
      $scope.analysis = JSON.parse(res);
      // console.log($scope.analysis);
    });
    ReviewsService.getData($scope.id, function(res) {
      for (var i = 0; i < res.length; i++) {
        $scope.reviews.push(JSON.parse(res[i]));
      }
      // console.log($scope.reviews);
    })

    $scope.percent = function(rating) {
      var num = (parseFloat(rating)/5.0)*100;
      return num.toString() + "%"
    }

    $scope.ratingStyle = function(rating) {
      var styleObj = {}
      var percent = $scope.percent(rating);
      var num = (parseFloat(rating)/5.0)*100;
      var bg_color = "#4caf50"; // green
      styleObj["width"] = percent;
      if (num < 30) {
        bg_color = "#f44336"; // red
      }
      else if (num < 60) {
        bg_color = "#ffeb3b"; // yellow
      }
      styleObj["background-color"] = bg_color;
      return styleObj;
    }

    $scope.ratingStyleRec = function(rating) {
      var styleObj = {};
      var num = parseFloat(rating)*100;
      var percent = num + "%";
      var bg_color = "#4caf50"; // green
      styleObj["width"] = percent;
      if (num < 33) {
        bg_color = "#f44336"; // red
      }
      else if (num < 67) {
        bg_color = "#ffeb3b"; // yellow
      }
      styleObj["background-color"] = bg_color;
      return styleObj;
    }

    $scope.ratingCEO = function(rating) {
      var styleObj = {}
      styleObj["width"] = rating + "%";
      styleObj["background-color"] = "#4caf50";
      return styleObj;
    }

    $scope.ratingReview = function(rating) {
      var styleObj = {}
      var num = ((parseFloat(rating) + 1.0)/2.0)*100;
      var bg_color = "#4caf50"; // green
      styleObj["width"] = num.toString() + "%";
      styleObj["background-color"] = bg_color;
      return styleObj;
    }

    $scope.ratingSentiment = function(rating) {
      if (rating < -0.66) {
        return "Mostly Negative";
      }
      if (rating < -0.33) {
        return "Negative";
      }
      if (rating < 0) {
        return "Slightly Negative";
      }
      if (rating < 0.33) {
        return "Slightly Positive";
      }
      if (rating < 0.66) {
        return "Positive";
      }
      return "Mostly Positive";
    }

    $scope.ratingSubjectivity = function(rating) {
      if (rating < 0.05) {
        return "Neutral";
      }
      if (rating < 0.2) {
        return "Somewhat Neutral";
      }
      if (rating < 0.5) {
        return "Somewhat Subjective";
      }
      return "Subjective";
    }
  }]);
