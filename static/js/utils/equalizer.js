/**
 * Install jQuery plugin, receives a query and makes all other elements the
 * height of the highest element
 */

import $ from "jquery";

import "imagesloaded";

$.fn.equalizer = function( breakingPoint, delayedRetrigger ) {

    if ( $.type( breakingPoint ) === "undefined" ) {
        breakingPoint = false;
    }

    if ( $.type( delayedRetrigger ) === "undefined" ) {
        delayedRetrigger = false;
    }

    // Store for later
    var $elementsToEqualize = this,
        $win = $( window ),
        timeoutId = false;

    /**
     * Fake Resize
     *
     * Fake a resize so other plugins can pickup
     */
    function fakeResize() {
        $win.resize();
    }

    /**
     * Do the actual equalisation
     */
    function equalize() {

        // Clear all min-height props
        $elementsToEqualize.css( "height", "" );

        // Only proceed when breakingpoint is not passed
        if ( $win.width() <= breakingPoint ) {
            return;
        }

        // Get all heights
        var allHeights = $elementsToEqualize.map(function() {
            return $( this ).height();
        });

        // Calculate target height
        var targetHeight = Math.max.apply( null, allHeights );


        // Set the min-height on all
        $elementsToEqualize.height( targetHeight - 1 );

        // Set timeout to retrigger resize
        if ( delayedRetrigger ) {
            if ( timeoutId ) {
                window.clearTimeout( timeoutId );
            }
            timeoutId = window.setTimeout( fakeResize, 150 );
        }
    }

    // On resize
    $win.resize( equalize );
    // On images loaded
    $elementsToEqualize.imagesLoaded( equalize );
    $elementsToEqualize.imagesLoaded(function() {
        window.setTimeout(function() {
            fakeResize();
        }, 150 );
        $win.resize();
    });

    // First run
    equalize();

};
