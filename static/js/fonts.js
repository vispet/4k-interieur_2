/**
 * Font loader
 */

import $ from "jquery";
import WebFont from "webfontloader";

WebFont.load({
    active: function() {
        // Trigger a resize when fonts are rendered
        $( window ).resize();
    },
    google: {
        families: [ "Roboto:400,700,700italic,400italic:latin" ]
    }
});
