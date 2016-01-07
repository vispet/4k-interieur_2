#!/usr/bin/env node

var Imagemin = require( "imagemin" );

if ( process.argv.length > 4 ) {

    var source = process.argv[ 2 ];
    var dest = process.argv[ 3 ];
    var optimization = process.argv[ 4 ];

    var imagemin = new Imagemin();

    imagemin.src( source + "/**/*.{jpg,png,gif}" );
    imagemin.dest( dest );
    imagemin.use( Imagemin.jpegtran() );
    imagemin.use( Imagemin.gifsicle() );
    imagemin.use( Imagemin.optipng({
        optimizationLevel: optimization
    }) );

    imagemin.run();

}
