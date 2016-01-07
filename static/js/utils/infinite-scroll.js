/**
 * Javascripts for news
 */

import $ from "jquery";
import "waypoints/lib/noframework.waypoints.js";
import "waypoints/lib/shortcuts/infinite.js";


$( document ).ready(() => {

    let $container = $( ".infinite-container" );
    let $pagination = $( ".infinite-paginator" );
    $container.data( "infinite", new window.Waypoint.Infinite({
        element: $container.get( 0 ),
        items: ".infinite-item",
        onBeforePageLoad: function() {
            $pagination.hide();
        }
    }));

});
