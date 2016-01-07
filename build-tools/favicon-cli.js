#!/usr/bin/env node

var favicons = require( "favicons" );
var fs = require( "fs" );
var path = require( "path" );
var mkdirp = require( "mkdirp" );

if ( process.argv.length <= 4 ) {
    console.log( "Wrong usage" );
    process.exit( 1 );
}

// Map variables
var source = process.argv[ 2 ];
var dest = process.argv[ 3 ];
var htmlPath = process.argv[ 4 ];

/**
 * Write html
 */
function writeHtml( html ) {
    var result = "{% load static from staticfiles %}\n";
    for ( var i in html ) {
        result += html[ i ].replace( "STATIC_ROOT/", "{% static \"\" %}" );
        result += "\n";
    }
    console.log( "Writing html to :\"" + htmlPath + "\"" );

    mkdirp.sync( path.dirname( htmlPath ) );
    fs.writeFileSync( htmlPath, result );
}

function writeFiles( files ) {

    console.log( "Writing files to :\"" + dest + "\"" );

    mkdirp.sync( dest );
    for ( var i in files ) {
        fs.writeFileSync( path.join( dest, files[ i ].name ),
                          files[ i ].contents.replace( /STATIC_ROOT/g, "" ) );
    }
}

function writeImages( images ) {

    console.log( "Writing images to :\"" + dest + "\"" );

    mkdirp.sync( dest );
    for ( var i in images ) {
        fs.writeFileSync( path.join( dest, images[ i ].name ),
                          images[ i ].contents );
    }

}

favicons( source, {
    background: "#fff",
    path: "STATIC_ROOT/img/favicons",
    icons: {
        twitter: false,
        opengraph: false
    }
}, function (error, response) {
    if ( error ) {
        console.log( "ERROR:"  + error.name + " =>\n" + error.message );
    }
    writeHtml( response.html );
    writeFiles( response.files );
    writeImages( response.images );
});
