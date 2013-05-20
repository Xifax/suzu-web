module.exports = function(grunt) {
  grunt.initConfig({
    concat: {
      dist: {
        src: [
            'media/js/jquery-2.0.0.min.js',
            'media/js/furigana.js',
            'media/js/humane.min.js',
            'media/js/cup.of.js',
            'media/js/jquery.tooltipster.min.js'
        ],
        dest: 'media/js/all.in.one.js'
      }
    },
    cssmin: {
      combine: {
          files: {
            'media/css/all.in.one.css': [
                'media/css/loader.css',
                'media/css/style.css',
                'media/css/tooltipster.css',
                'media/css/humane.css',
                'media/css/glyphs.css'
            ]
          }
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-cssmin');

  grunt.registerTask('default', ['cssmin', 'concat']);
};
