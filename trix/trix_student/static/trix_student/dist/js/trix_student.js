(function() {
  angular.module('trixStudent', ['ngCookies', 'ngRoute', 'ui.bootstrap', 'trixStudent.directives', 'trixStudent.assignments.controllers']).config([
    '$httpProvider',
    function($httpProvider) {
      $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
      return $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    }
  ]).run([
    '$http',
    '$cookies',
    function($http,
    $cookies) {
      return $http.defaults.headers.common['X-CSRFToken'] = $cookies.csrftoken;
    }
  ]);

}).call(this);

(function() {
  angular.module('trixStudent.assignments.controllers', ['ngRoute']).controller('AddTagCtrl', [
    '$scope',
    '$window',
    function($scope,
    $window) {
      $scope.tagToAdd = '';
      $scope.negative = false;
      $scope.addTag = function() {
        var currentUrl,
    tags;
        currentUrl = new Url();
        tags = currentUrl.query.tags;
        if ($scope.negative) {
          $scope.tagToAdd = '-' + $scope.tagToAdd;
        }
        if ((tags != null) && tags !== '') {
          tags = tags + ',' + $scope.tagToAdd;
        } else {
          tags = $scope.tagToAdd;
        }
        currentUrl.query.tags = tags;
        delete currentUrl.query['page'];
        return $window.location.href = currentUrl.toString();
      };
    }
  ]).controller('RemoveTagCtrl', [
    '$scope',
    '$window',
    function($scope,
    $window) {
      return $scope.removeTag = function(tagToRemove) {
        var currentUrl,
    index,
    tags,
    tagsArray;
        currentUrl = new Url();
        tags = currentUrl.query.tags;
        tagsArray = tags.split(',');
        index = tagsArray.indexOf(tagToRemove);
        tagsArray.splice(index,
    1);
        tags = tagsArray.join(',');
        currentUrl.query.tags = tags;
        delete currentUrl.query['page'];
        return $window.location.href = currentUrl.toString();
      };
    }
  ]).controller('SolutionCtrl', [
    '$scope',
    function($scope) {
      return $scope.isVisible = false;
    }
  ]).controller('MenuCtrl', [
    '$scope',
    function($scope) {
      return $scope.menuVisible = false;
    }
  ]).controller('CourseCtrl', [
    '$scope',
    function($scope) {
      $scope.footerVisible = false;
      return $scope.showFooter = function() {
        return $scope.footerVisible = !$scope.footerVisible;
      };
    }
  ]).controller('AssignmentCtrl', [
    '$scope',
    '$http',
    '$rootScope',
    function($scope,
    $http,
    $rootScope) {
      $scope.howsolved = null;
      $scope.saving = false;
      $scope.buttonClass = 'btn-default';
      $scope.boxClass = '';
      $scope.$watch('howsolved',
    function(newValue) {
        if (newValue === 'bymyself') {
          $scope.buttonClass = 'btn-success';
          $scope.boxClass = 'trix-assignment-solvedbymyself';
        } else if (newValue === 'withhelp') {
          $scope.buttonClass = 'btn-warning';
          $scope.boxClass = 'trix-assignment-solvedwithhelp';
        } else {
          $scope.buttonClass = 'btn-default';
          $scope.boxClass = 'trix-assignment-notsolved';
        }
        // Tell AssignmentListProgressController to reload
        $rootScope.$emit('assignments.progressChanged');
      });
      $scope._getApiUrl = function() {
        return '/assignment/howsolved/' + $scope.assignment_id;
      };
      $scope._showError = function(message) {
        // TODO: Use bootstrap modal and a scope variable
        $scope.saving = false;
        return alert(message);
      };
      $scope._updateHowSolved = function(howsolved) {
        var data;
        $scope.saving = true;
        data = {
          howsolved: howsolved
        };
        return $http.post($scope._getApiUrl(),
    data).then(function(response) {
          $scope.saving = false;
          return $scope.howsolved = response.data.howsolved;
        }).catch(function(response) {
          console.log(response);
          return $scope._showError('An error occurred!');
        });
      };
      $scope.solvedOnMyOwn = function() {
        return $scope._updateHowSolved('bymyself');
      };
      $scope.solvedWithHelp = function() {
        return $scope._updateHowSolved('withhelp');
      };
      return $scope.notSolved = function() {
        $scope.saving = true;
        return $http.delete($scope._getApiUrl()).then(function(response) {
          $scope.saving = false;
          return $scope.howsolved = null;
        }).catch(function(response) {
          if (response.status === 404) { // Handle 404 just like 200
            $scope.saving = false;
            return $scope.howsolved = null;
          } else {
            return $scope._showError('An error occurred!');
          }
        });
      };
    }
  ]).controller('AssignmentListProgressController', [
    '$scope',
    '$http',
    '$rootScope',
    function($scope,
    $http,
    $rootScope) {
      var apiUrl,
    unbindProgressChanged;
      $scope.loading = true;
      apiUrl = new Url();
      apiUrl.query.progressjson = '1';
      $scope._loadProgress = function() {
        $scope.loading = true;
        return $http.get(apiUrl.toString()).then(function(response) {
          $scope.loading = false;
          $scope.solvedPercentage = response.data.percent;
          if ($scope.solvedPercentage > 1 && $scope.solvedPercentage < 20) {
            return $scope.progressBarClass = 'progress-bar-danger';
          } else if ($scope.solvedPercentage < 45) {
            return $scope.progressBarClass = 'progress-bar-warning';
          } else if ($scope.solvedPercentage === 100) {
            return $scope.progressBarClass = 'progress-bar-success';
          } else {
            return $scope.progressBarClass = '';
          }
        }).catch(function(response) {
          return console.error('Failed to load progress:',
    response.statusText);
        });
      };
      unbindProgressChanged = $rootScope.$on('assignments.progressChanged',
    function() {
        return $scope._loadProgress();
      });
      return $scope.$on('$destroy',
    unbindProgressChanged);
    }
  ]);

}).call(this);

(function() {
  angular.module('trixStudent.directives', []).directive('trixAriaChecked', function() {
    return {
      restrict: 'A',
      scope: {
        'checked': '=trixAriaChecked'
      },
      controller: function($scope) {},
      link: function(scope, element, attrs) {
        var updateAriaChecked;
        updateAriaChecked = function() {
          if (scope.checked) {
            return element.attr('aria-checked', 'true');
          } else {
            return element.attr('aria-checked', 'false');
          }
        };
        updateAriaChecked();
        scope.$watch(attrs.trixAriaChecked, function(newValue, oldValue) {
          return updateAriaChecked();
        });
      }
    };
  });

}).call(this);
