module.exports = function(grunt) {
  grunt.initConfig({
    jsResources: [],
    cssResources: [],
    pkg: grunt.file.readJSON('package.json'),
    clean: ['build/', 'dist/'],
    replace: {
      gather: {
        files: [
            {
              cwd: 'src',
              dest: 'build/',
              expand: true,
              src: [ 'index.html' ]
            }
        ],
        options: {
          patterns: [
            {
              match: /<script .*\/script\>/g,
              replacement: function ( matchedString ) {
                var resourceTarget = matchedString.match( /(src\s?\=\s?[\'\"])([^\'\"]*)([\'\"])/ )[2];
                targetConfig = grunt.config( 'jsResources' );
                targetConfig.push( resourceTarget );
                grunt.config( 'jsResources', targetConfig );
              }
            },
            {
              match: /<link .*\>/g,
              replacement: function ( matchedString ) {
                var resourceTarget = matchedString.match( /(href\s?\=\s?[\'\"])([^\'\"]*)([\'\"])/ )[2];
                targetConfig = grunt.config( 'cssResources' );
                targetConfig.push( resourceTarget );
                grunt.config( 'cssResources', targetConfig );
              }
            }
          ]
        }
      }
    },
    copy: {
      build: {
        files: [
          // includes files within path
          {expand: true, cwd: 'src', src: [ '<%= jsResources %>' ], dest: 'build/', filter: 'isFile'},
          {expand: true, cwd: 'src', src: [ '<%= cssResources %>' ], dest: 'build/', filter: 'isFile'},
        ],
      }
    },
    jshint: {
      task: {
        src: ['Gruntfile.js', 'build/app/**/*.js']
      },
      options: {
        'globals': null,
        'force': false,
        'reporter': null,
        'reporterOutput': null
      }
    },
    concat: {
      task: {
        src: ['build/app/**/*.js'],
        dest: 'dist/app.js'
      },
      options: {
        'separator': grunt.util.linefeed,
        'banner': '',
        'footer': '',
        'stripBanners': false,
        'process': false,
        'sourceMap': false,
        'sourceMapName': undefined,
        'sourceMapStyle': 'embed'
      }
    },
    uglify: {
      task: {
        src: ['dist/app.js'],
        dest: 'dist/app.min.js'
      },
      options: {
        'mangle': {},
        'compress': {},
        'beautify': false,
        'expression': false,
        'report': 'min',
        'sourceMap': false,
        'sourceMapName': undefined,
        'sourceMapIn': undefined,
        'sourceMapIncludeSources': false,
        'enclose': undefined,
        'wrap': undefined,
        'exportAll': false,
        'preserveComments': undefined,
        'banner': '/*\n <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> \n*/\n',
        'footer': ''
      }
    },
    cssmin: {
      task: {
        src: ['build/assets/styles/css/*.css'],
        dest: 'dist/app.min.css'
      },
      options: {
        'banner': null,
        'keepSpecialComments': '*',
        'report': 'min'
      }
    },
    compass: {
      dist: {
        options: {
          sassDir: 'src/assets/styles/scss',
          cssDir:  'src/assets/styles/css'
        }
      }
    },
    htmlmin: {
      build: {
        // options: {
        //   removeComments: true,
        //   collapseWhitespace: true
        // },
        files: [{
          expand: true,
          cwd:'src',
          src: ['*.html', 'app/**/*.html'],
          dest: 'build'
        }]
      }
    }
  });

  /* files */
  grunt.loadNpmTasks('grunt-replace');
  grunt.loadNpmTasks('grunt-contrib-clean');
  grunt.loadNpmTasks('grunt-contrib-copy');

  /* js */
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-uglify');

  /* style */
  grunt.loadNpmTasks('grunt-contrib-compass');
  grunt.loadNpmTasks('grunt-contrib-cssmin');

  /* html */
  grunt.loadNpmTasks('grunt-contrib-htmlmin');

  grunt.registerTask('default', ['clean', 'replace', 'copy', 'jshint', 'compass', 'concat', 'uglify', 'cssmin', 'htmlmin']);
};
