angular.module('trixStudent', [
  'ngCookies'
  'ngRoute'
  'ui.bootstrap'
  'trixStudent.directives'
  'trixStudent.assignments.controllers'
])

.config([
    '$httpProvider'
    ($httpProvider) ->
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken'
        $httpProvider.defaults.xsrfCookieName = 'csrftoken'
        ])

.run([
  '$http', '$cookies'
  ($http, $cookies) ->
    $http.defaults.headers.common['X-CSRFToken'] = $cookies.csrftoken
])
