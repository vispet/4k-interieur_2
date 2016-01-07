#!/usr/bin/env node

var glob = require( "glob" );
var Grunticon = require( "grunticon-lib" );

if ( process.argv.length > 3 ) {
    var files = glob.sync( process.argv[ 2 ] );
    var dest = process.argv[ 3 ];

    if ( files.length ) {

        var grunticonProcess = new Grunticon( files, dest, {
          datasvgcss: "svg.css",
          datapngcss: "png.css",
          urlpngcss: "ref.css",
          customselectors: {
            // Put custom selectors here
            "logo-white": [
                "#main-navigation .navbar-brand",
                "#footer .logo-footer"
            ]
          }
        });

        grunticonProcess.process();
    }

}
