module.exports = (grunt) ->

  appfiles = {
    coffeecode: ['src/**/*.coffee', '!src/**/*.spec.coffee']
    less: ['src/less/*.less', 'src/less/**/*.less']
  }

  vendorfiles = {
    fonts: [
      'bower_components/components-font-awesome/webfonts/fa-brands-400.eot'
      'bower_components/components-font-awesome/webfonts/fa-brands-400.svg'
      'bower_components/components-font-awesome/webfonts/fa-brands-400.ttf'
      'bower_components/components-font-awesome/webfonts/fa-brands-400.woff'
      'bower_components/components-font-awesome/webfonts/fa-brands-400.woff2'
      'bower_components/components-font-awesome/webfonts/fa-regular-400.eot'
      'bower_components/components-font-awesome/webfonts/fa-regular-400.svg'
      'bower_components/components-font-awesome/webfonts/fa-regular-400.ttf'
      'bower_components/components-font-awesome/webfonts/fa-regular-400.woff'
      'bower_components/components-font-awesome/webfonts/fa-regular-400.woff2'
      'bower_components/components-font-awesome/webfonts/fa-solid-900.eot'
      'bower_components/components-font-awesome/webfonts/fa-solid-900.svg'
      'bower_components/components-font-awesome/webfonts/fa-solid-900.ttf'
      'bower_components/components-font-awesome/webfonts/fa-solid-900.woff'
      'bower_components/components-font-awesome/webfonts/fa-solid-900.woff2'
    ]
    glyph_fonts: [
      'bower_components/bootstrap/fonts/glyphicons-halflings-regular.eot'
      'bower_components/bootstrap/fonts/glyphicons-halflings-regular.svg'
      'bower_components/bootstrap/fonts/glyphicons-halflings-regular.ttf'
      'bower_components/bootstrap/fonts/glyphicons-halflings-regular.woff'
    ]
    js: [
      'bower_components/jquery/dist/jquery.slim.min.js'
      'bower_components/jquery/dist/jquery.slim.min.map'
      'bower_components/angular/angular.min.js'
      'bower_components/angular/angular.min.js.map'
      'bower_components/angular-cookies/angular-cookies.min.js'
      'bower_components/angular-cookies/angular-cookies.min.js.map'
      'bower_components/angular-route/angular-route.min.js'
      'bower_components/angular-route/angular-route.min.js.map'
      'bower_components/jsurl/url.min.js'
      'bower_components/angular-bootstrap/ui-bootstrap.min.js'
      'bower_components/eonasdan-bootstrap-datetimepicker/build' +
        '/js/bootstrap-datetimepicker.min.js'
      'bower_components/bootstrap/js/alert.js'
    ]
  }

  grunt.loadNpmTasks('grunt-contrib-watch')
  grunt.loadNpmTasks('grunt-contrib-less')
  grunt.loadNpmTasks('grunt-contrib-copy')
  grunt.loadNpmTasks('grunt-contrib-coffee')
  grunt.loadNpmTasks('grunt-coffeelint')
  grunt.loadNpmTasks('grunt-contrib-concat')
  grunt.loadNpmTasks('grunt-contrib-uglify')

  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json')
    delta:
      less:
        files: appfiles.less
        tasks: 'less'
      coffeecode:
        files: appfiles.coffeecode
        tasks: [
          'coffeelint:code', 'coffee:code', 'buildCodeDist']
      gruntfile:
        files: 'Gruntfile.coffee'
        tasks: ['coffeelint:gruntfile']

    less:
      development:
        options:
          paths: ["less", "bower_components"]
        files:
          ["dist/css/styles.css": "src/less/styles.less",
           "dist/css/wcag.css": "src/less/wcag.less"]

    coffeelint:
      code: appfiles.coffeecode
      gruntfile: ['Gruntfile.coffee']

    coffee:
      code:
        expand: true
        cwd: '.'
        src: appfiles.coffeecode
        dest: '.'
        ext: '.js'

    concat:
      trix_student:
        src: ['src/**/*.js', '!src/**/*.spec.js']
        dest: 'dist/js/trix_student.js'

    uglify:
      options:
        mangle: false
        sourceMap: true
      trix_student:
        files:
          'dist/js/trix_student.min.js': ['dist/js/trix_student.js']

    copy:
      vendor:
        files: [{
          expand: true
          flatten: true
          src: vendorfiles.fonts
          dest: 'dist/vendor/fonts/'
        }, {
          expand: true
          flatten: true
          src: vendorfiles.js
          dest: 'dist/vendor/js/'
        }, {
          expand: true
          flatten: true
          src: vendorfiles.glyph_fonts
          dest: 'dist/fonts/'
        }]
  })

  grunt.registerTask('buildCodeDist', [
    'concat:trix_student'
    'uglify:trix_student'
  ])

  grunt.registerTask('build', [
    'coffeelint'
    'less'
    'coffee:code'
    'buildCodeDist',
    'copy:vendor'
  ])

  grunt.registerTask('dist', [
    'build'
  ])

  # Rename the watch task to delta, and make a new watch task that runs
  # build on startup
  grunt.renameTask('watch', 'delta')
  grunt.registerTask('watch', [
    'build'
    'delta'
  ])

  grunt.registerTask('default', ['build'])
