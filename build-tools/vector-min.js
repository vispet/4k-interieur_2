#!/usr/bin/env node

var Imagemin = require( "imagemin" );

if ( process.argv.length > 3 ) {

    var source = process.argv[ 2 ];
    var dest = process.argv[ 3 ];

    var imagemin = new Imagemin();

    imagemin.src( source + "/**/*.svg" );
    imagemin.dest( dest );
    imagemin.use( Imagemin.svgo() );

    imagemin.run();

}
