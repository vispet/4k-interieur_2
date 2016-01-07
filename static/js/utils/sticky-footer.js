/**
 * Sticky footer utility
 */

import $ from "jquery";


/**
 * Entry point
 */

$( document ).ready(() => {


    let $win = $( window );
    let $content = $( "#main-content" );
    let $footer = $( "#footer" );


    /**
     * Actually sets the footer
     */
    function setFooter() {

        // Remove prop from content
        $content.css( "min-height", "" );

        if ( $win.height() > $content.outerHeight() + $footer.outerHeight() ) {
            // Calculate the desired height
            let targetHeight = $win.height() - $footer.outerHeight();
            $content.css( "min-height", targetHeight + "px" );
        } else {
            // Clear the min height
            $content.css( "min-height", "" );
        }

    }

    $win.resize( setFooter );
    setFooter();

});
