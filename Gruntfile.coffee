module.exports = (grunt) ->

  # Project configuration
  grunt.initConfig

    # Compile coffeescript to js
    coffee:
        compile:
            files:
                'media/js/cup.of.js': ['media/coffee/*.coffee']

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

    # Compile stylus to css
    stylus:
        compile:
            files:
                'media/css/style.css': ['media/styl/*.styl']

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

    # Monitor scripts for changes
    watch:
        options:
            livereload: true
        coffee:
            files: 'media/coffee/**/*.coffee'
            tasks: ['coffee', 'concat']
        stylus:
            files: 'media/styl/**/*.styl'
            tasks: ['stylus', 'cssmin']

  # Load required npm tasks
  grunt.loadNpmTasks 'grunt-contrib-coffee'
  grunt.loadNpmTasks 'grunt-contrib-stylus'
  grunt.loadNpmTasks 'grunt-contrib-concat'
  grunt.loadNpmTasks 'grunt-contrib-cssmin'
  grunt.loadNpmTasks 'grunt-contrib-watch'

  # Define default task
  grunt.registerTask 'default', ['coffee', 'stylus', 'concat', 'cssmin']
