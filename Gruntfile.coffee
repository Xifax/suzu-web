module.exports = (grunt) ->

  # Project configuration
  grunt.initConfig
    # TODO: Compile coffeescript to js
    #coffee:
      #app:
        #expand: true
        #cwd: 'src'
        #src: ['**/*.coffee']
        #dest: 'lib'
        #ext: '.js'
    # Concatenate all js files
    concat:
        dist:
            src: [
                'media/js/jquery-2.0.0.min.js',
                'media/js/furigana.js',
                'media/js/humane.min.js',
                'media/js/cup.of.js',
                'media/js/jquery.tooltipster.min.js'
            ],
            dest: 'media/js/all.in.one.js'
    # TODO: Compile stylus to css
    # Concatenate all css files
    cssmin:
        combine:
            files:
                'media/css/all.in.one.css': [
                    'media/css/loader.css',
                    'media/css/style.css',
                    'media/css/tooltipster.css',
                    'media/css/humane.css',
                    'media/css/glyphs.css'
                ]

    #watch:
      #app:
        #files: '**/*.coffee'
        #tasks: ['coffee']

  # These plugins provide necessary tasks.
  #grunt.loadNpmTasks 'grunt-contrib-coffee'
  #grunt.loadNpmTasks 'grunt-contrib-watch'
  grunt.loadNpmTasks 'grunt-contrib-concat'
  grunt.loadNpmTasks 'grunt-contrib-cssmin'

  # Define default task
  grunt.registerTask 'default', ['cssmin', 'concat']
