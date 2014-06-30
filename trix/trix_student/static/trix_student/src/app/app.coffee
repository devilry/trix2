angular.module('trixStudent', [
  'ngCookies'
  'ui.bootstrap'
  'trixStudent.directives'
  'trixStudent.assignments.controllers'
])

.run([
  '$http', '$cookies'
  ($http, $cookies) ->
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken
])