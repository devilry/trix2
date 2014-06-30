(function() {
  angular.module('trixStudent', ['ngCookies', 'ui.bootstrap', 'trixStudent.directives', 'trixStudent.assignments.controllers']).run([
    '$http', '$cookies', function($http, $cookies) {
      return $http.defaults.headers.common['X-CSRFToken'] = $cookies.csrftoken;
    }
  ]);

}).call(this);

(function() {
  angular.module('trixStudent.assignments.controllers', []).controller('AddTagCtrl', [
    '$scope', '$window', function($scope, $window) {
      $scope.tagToAdd = '';
      $scope.addTag = function() {
        var currentUrl, tags;
        currentUrl = new Url();
        tags = currentUrl.query.tags;
        if ((tags != null) && tags !== '') {
          tags = "" + tags + "," + $scope.tagToAdd;
        } else {
          tags = $scope.tagToAdd;
        }
        currentUrl.query.tags = tags;
        return $window.location.href = currentUrl.toString();
      };
    }
  ]).controller('RemoveTagCtrl', [
    '$scope', '$window', function($scope, $window) {
      return $scope.removeTag = function(tagToRemove) {
        var currentUrl, index, tags, tagsArray;
        currentUrl = new Url();
        tags = currentUrl.query.tags;
        tagsArray = tags.split(',');
        index = tagsArray.indexOf(tagToRemove);
        tagsArray.splice(index, 1);
        tags = tagsArray.join(',');
        currentUrl.query.tags = tags;
        return $window.location.href = currentUrl.toString();
      };
    }
  ]).controller('SolutionCtrl', [
    '$scope', function($scope) {
      return $scope.isVisible = false;
    }
  ]).controller('HowSolvedCtrl', [
    '$scope', '$http', function($scope, $http) {
      $scope.howsolved = null;
      $scope.saving = false;
      $scope.buttonClass = 'btn-default';
      $scope.boxClass = '';
      $scope.$watch('howsolved', function(newValue) {
        if (newValue === 'bymyself') {
          $scope.buttonClass = 'btn-success';
          $scope.boxClass = 'alert alert-success';
        } else if (newValue === 'withhelp') {
          $scope.buttonClass = 'btn-warning';
          $scope.boxClass = 'alert alert-warning';
        } else {
          $scope.buttonClass = 'btn-default';
          $scope.boxClass = '';
        }
      });
      $scope._getApiUrl = function() {
        return "/assignment/howsolved/" + $scope.assignment_id;
      };
      $scope._showError = function(message) {
        $scope.saving = false;
        return alert(message);
      };
      $scope._updateHowSolved = function(howsolved) {
        var data;
        $scope.saving = true;
        data = {
          howsolved: howsolved
        };
        return $http.post($scope._getApiUrl(), data).success(function(data) {
          $scope.saving = false;
          return $scope.howsolved = data.howsolved;
        }).error(function(data) {
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
        return $http["delete"]($scope._getApiUrl()).success(function(data) {
          $scope.saving = false;
          return $scope.howsolved = null;
        }).error(function(data) {
          return $scope._showError('An error occurred!');
        });
      };
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
