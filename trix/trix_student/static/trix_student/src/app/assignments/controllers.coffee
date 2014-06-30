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
  '$scope',
  ($scope) ->
    $scope.howsolved = null

    $scope.solvedOnMyOwn = ->
      $scope.howsolved = 'bymyself'

    $scope.solvedWithHelp = ->
      $scope.howsolved = 'withhelp'

    $scope.notSolved = ->
      $scope.howsolved = null

])