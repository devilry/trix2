angular.module('trixStudent.directives', [])

.directive 'trixAriaChecked', ->
  return {
    restrict: 'A'
    scope: {
      'checked': '=trixAriaChecked'
    }
    controller: ($scope) ->

    link: (scope, element, attrs) ->
      updateAriaChecked = ->
        if scope.checked
          element.attr('aria-checked', 'true')
        else
          element.attr('aria-checked', 'false')

      updateAriaChecked()
      scope.$watch attrs.trixAriaChecked, (newValue, oldValue) ->
        updateAriaChecked()

      return
  }
