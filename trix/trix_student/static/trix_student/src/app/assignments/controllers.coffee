angular.module('trixStudent.assignments.controllers', [])

.controller('AddTagCtrl', [
  '$scope', '$window',
  ($scope, $window) ->
    $scope.tagToAdd = ''
    $scope.addTag = ->
      currentUrl = new Url()
      tags = currentUrl.query.tags
      if tags? and tags != ''
        tags = "#{tags},#{$scope.tagToAdd}"
      else
        tags = $scope.tagToAdd
      currentUrl.query.tags = tags
      $window.location.href = currentUrl.toString()
    return
])

.controller('RemoveTagCtrl', [
  '$scope', '$window',
  ($scope, $window) ->
    $scope.removeTag = (tagToRemove) ->
      currentUrl = new Url()
      tags = currentUrl.query.tags
      tagsArray = tags.split(',')
      index = tagsArray.indexOf(tagToRemove)
      tagsArray.splice(index, 1)
      tags = tagsArray.join(',')
      currentUrl.query.tags = tags
      $window.location.href = currentUrl.toString()
])

.controller('SolutionCtrl', [
  '$scope',
  ($scope) ->
    $scope.isVisible = false
])

.controller('HowSolvedCtrl', [
  '$scope', '$http',
  ($scope, $http) ->
    $scope.howsolved = null
    $scope.saving = false
    $scope.buttonClass = 'btn-success'

    $scope.$watch 'howsolved', (newValue) ->
      if newValue == 'bymyself'
        $scope.buttonClass = 'btn-success'
      else if newValue == 'withhelp'
        $scope.buttonClass = 'btn-warning'
      else
        $scope.buttonClass = 'btn-default'
      return

    $scope._getApiUrl = ->
      return "/assignment/howsolved/#{$scope.assignment_id}"

    $scope._showError = (message) ->
      # TODO: Use bootstrap modal and a scope variable
      $scope.saving = false
      alert(message)

    $scope._updateHowSolved = (howsolved) ->
      $scope.saving = true
      data = {
        howsolved: howsolved
      }
      $http.post($scope._getApiUrl(), data)
        .success (data) ->
          $scope.saving = false
          $scope.howsolved = data.howsolved
        .error (data) ->
          $scope._showError('An error occurred!')

    $scope.solvedOnMyOwn = ->
      $scope._updateHowSolved('bymyself')
      # $scope.howsolved = 'bymyself'

    $scope.solvedWithHelp = ->
      $scope._updateHowSolved('withhelp')
      # $scope.howsolved = 'withhelp'

    $scope.notSolved = ->
      $scope.saving = true
      $http.delete($scope._getApiUrl())
        .success (data) ->
          $scope.saving = false
          $scope.howsolved = null
        .error (data) ->
          $scope._showError('An error occurred!')
])