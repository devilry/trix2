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
    apiurl = '/assignment/howsolved'

    $scope._updateHowSolved = (howsolved) ->
      $scope.saving = true
      data = {
        howsolved: howsolved
        assignment_id: $scope.assignment_id
      }
      $http.post(apiurl, data)
        .success (data) ->
          $scope.saving = false
          console.log('Success!', data)
        .error ->
          # TODO: Use bootstrap modal and a scope variable
          $scope.saving = false
          alert('An error occurred!')

    $scope.solvedOnMyOwn = ->
      $scope._updateHowSolved('bymyself')
      # $scope.howsolved = 'bymyself'

    $scope.solvedWithHelp = ->
      $scope._updateHowSolved('withhelp')
      # $scope.howsolved = 'withhelp'

    $scope.notSolved = ->
      $scope.howsolved = null

])