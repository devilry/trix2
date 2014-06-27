module.exports = (grunt) ->

  appfiles = {
    coffeecode: ['src/**/*.coffee', '!src/**/*.spec.coffee']
    less: ['src/less/*.less', 'src/less/**/*.less']
  }

  vendorfiles = {
    fonts: [
      'bower_components/fontawesome/fonts/FontAwesome.otf'
      'bower_components/fontawesome/fonts/fontawesome-webfont.eot'
      'bower_components/fontawesome/fonts/fontawesome-webfont.svg'
      'bower_components/fontawesome/fonts/fontawesome-webfont.ttf'
      'bower_components/fontawesome/fonts/fontawesome-webfont.woff'
    ]
    js: [
      'bower_components/angular/angular.min.js'
      'bower_components/jsurl/url.min.js'
      'bower_components/angular-bootstrap/ui-bootstrap.min.js'
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
          "dist/css/styles.css": "src/less/styles.less"

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
