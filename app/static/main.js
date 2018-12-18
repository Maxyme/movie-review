(function () {

  'use strict';

  angular.module('WordcountApp', [])

    .controller('WordcountController', ['$scope', '$log', '$http', '$timeout',
      function ($scope, $log, $http, $timeout) {
        $scope.submitButtonText = 'Submit';
        $scope.loading = false;
        $scope.error_processing = false;
        $scope.error_message = '';
        $scope.getResults = function () {
          $scope.error_processing = false;
          $scope.error_message = '';
          $scope.loading = true;
          $scope.wordcounts = null;
          $scope.submitButtonText = 'Loading...';
          // get the URL from the input and fire the API request
          $http.post('/getcounts', {
            "url": $scope.url
          }).
          success(function (results) {
            $log.log(results);
            $scope.wordcounts = results;
            $scope.loading = false;
            $scope.submitButtonText = "Submit";
          }).
          error(function (error) {
            $log.log(error);
              $scope.loading = false;
              $scope.submitButtonText = "Submit";
              $scope.error_processing = true;
              $scope.error_message = error
          });

        };

      }
    ])
    .directive('wordCountChart', ['$parse', function ($parse) {
      return {
        restrict: 'E',
        replace: true,
        template: '<div id="chart"></div>',
        link: function (scope) {
        scope.$watch('wordcounts', function() {
          var data = scope.wordcounts;
          d3.select('#chart').selectAll('*').remove();
          for (var word in data) {
            d3.select('#chart')
              .append('div')
              .selectAll('div')
              .data(word[0])
              .enter()
              .append('div')
              .style('width', function() {
                return (data[word] * 20) + 'px';
              })
              .text(function(d){
                return word;
              });
          }
        }, true);
        }
      };
    }]);
}());