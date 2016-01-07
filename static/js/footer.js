/**
 * Script the footer
 */

import $ from "jquery";
import "./utils/equalizer.js";
import "./utils/sticky-footer.js";


/**
 * Entry point
 */
$( document ).ready(() => {
    $( "#footer .footer-col" ).equalizer( 767 );
});
