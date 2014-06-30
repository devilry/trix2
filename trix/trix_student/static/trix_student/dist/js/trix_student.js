(function() {
  angular.module('trixStudent', ['ui.bootstrap', 'trixStudent.directives', 'trixStudent.assignments.controllers']);

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
      var apiurl;
      $scope.howsolved = null;
      $scope.saving = false;
      apiurl = '/assignment/howsolved';
      $scope._updateHowSolved = function(howsolved) {
        var data;
        $scope.saving = true;
        data = {
          howsolved: howsolved,
          assignment_id: $scope.assignment_id
        };
        return $http.post(apiurl, data).success(function(data) {
          $scope.saving = false;
          return console.log('Success!', data);
        }).error(function() {
          $scope.saving = false;
          return alert('An error occurred!');
        });
      };
      $scope.solvedOnMyOwn = function() {
        return $scope._updateHowSolved('bymyself');
      };
      $scope.solvedWithHelp = function() {
        return $scope._updateHowSolved('withhelp');
      };
      return $scope.notSolved = function() {
        return $scope.howsolved = null;
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
