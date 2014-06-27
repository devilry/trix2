(function() {
  angular.module('trixStudent', ['ui.bootstrap', 'trixStudent.assignments.controllers']);

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
      $scope.isVisible = false;
      $scope.solvedOnMyOwn = function() {
        return alert('Coming soon');
      };
      return $scope.solvedWithHelp = function() {
        return alert('Coming soon');
      };
    }
  ]);

}).call(this);

(function() {
  angular.module('trixStudent.assignments.directives', []).directive('trixStudentAddTagSelect', function() {
    return {
      restrict: 'A',
      link: function(scope, element, attrs) {
        element.on('change', function() {
          return console.log(scope.stuff);
        });
      },
      controller: function($scope) {
        return $scope.stuff = '';
      }
    };
  });

}).call(this);
