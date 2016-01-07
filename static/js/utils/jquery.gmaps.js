/*
 * jquery.maps.js
 * A jQuery wrapper for google maps.
 * Just to keep things cached.
 * By Tom Van Damme for rotorgroup.be
 * Copyright 2013
 */

/* global google */

import jQuery from "jquery";

(function( document, window, $ ) {

    "use strict";

    var _API_LOADING_ = false;
    var _API_LOADED_ = false;
    var _API_AUTOLOAD_ = true;
    var _MAPS_QUEUE_ = [];
    var _LOADED_CB_ = [];
    var _JQ_MAP_ = "_gmap_obj_";
    var _D_CONF_ = "config";
    var _D_MARKERS_ = "markers";

    var defaultOptions = {
        markers: [],
        clusterStyles: false,
        markerDefault: {
            position: {
                lat: 0,
                lng: 0
            },
            title: false,
            data: false,
            clustered: true,
            extra: {}
        },
        config: {
            zoom: 13,
            center: {
                lat: 0,
                lng: 0
            },
            clustered: false,
            extra: {}
        }
    };

    function loadscript(){
        if ( _API_LOADING_ || _API_LOADED_ ) {
            return;
        }

        _API_LOADING_ = true;

        var script = document.createElement("script");
        script.type = "text/javascript";
        script.src = "http://maps.googleapis.com/maps/api/js?" +
                     "sensor=false&callback=gmapsInitialize";
        document.body.appendChild(script);
    }

    function initialize() {
        _API_LOADING_ = false;
        _API_LOADED_ = true;

        while ( _MAPS_QUEUE_.length ) {
            _MAPS_QUEUE_.shift().init();
        }

        while ( _LOADED_CB_.length ) {
            _LOADED_CB_.shift()();
        }
    }
    window.gmapsInitialize = initialize;

    function GMap( $element, options ) {
        this.$element = $element;
        this.options = $.extend( true, defaultOptions, options || {} );

        var config = $( $element ).data( _D_CONF_ );
        var markers = $( $element ).data( _D_MARKERS_ );

        if ( config ) {
            this.options.config = $.extend( this.options.config, config );
        }

        if ( markers ) {
            this.options.markers = this.options.markers.concat( markers );
        }

        if ( _API_LOADED_ ) {
            this.init();
        } else {
            _MAPS_QUEUE_.push( this );
        }
    }

    GMap.prototype.init = function(){
        var config = this.options.config;

        var mapConfig = $.extend( config.extra, {
            zoom: config.zoom,
            center: new google.maps.LatLng( config.center.lat,
                                            config.center.lng ),
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            mapTypeControlOptions: {
                position: google.maps.ControlPosition.TOP_CENTER
            }
        } );

        var markers = this.options.markers;

        this.map = new google.maps.Map( this.$element[0], mapConfig );

        this.markers = [];

        if ( this.options.config.clustered ) {
            /* global MarkerClusterer */
            this.clusterer = new MarkerClusterer( this.map );

            if ( this.options.clusterStyles ) {
                this.clusterer.setStyles( this.options.clusterStyles );
            }
        }

        for(var i = 0; i < markers.length; i++){
            var marker = markers[ i ];
            marker.object = this.createMarker(
                $.extend( this.options.markerDefault, markers[ i ] ) );
            this.markers.push( marker );
        }
    };

    GMap.prototype.createMarker = function( markerData ) {
        var options = $.extend( this.options.markerDefault.extra, {
            position: new google.maps.LatLng( markerData.position.lat,
                                              markerData.position.lng ),
            map: this.map
        } );

        if ( markerData.title ) {
            options.title = markerData.title;
        }

        var marker = new google.maps.Marker(options);

        if ( this.options.config.clustered && markerData.clustered ) {
            this.clusterer.addMarker( marker );
        }

        return marker;
    };

    /**
     * jQuery selector to create gmaps or get google.maps.Map objects.
     */
    $.fn.gmap = function( options ) {

        if ( options === "getMap" ) {
            return this.data( _JQ_MAP_ );
        }

        this.each(function(){
            if ( $.type( $( this ).data( _JQ_MAP_ ) ) !== "undefined") {
                return;
            }
            $( this ).data( _JQ_MAP_, new GMap( $( this ), options ));
        });

        return this;
    };

    /**
     * Callback that ensures calling but only if the google maps API is
     * loaded.
     *
     * If autoload is enabled, the api is loaded if not already loading or
     * loaded.
     * Autoload is enabled by default.
     */
    $.gmapAPILoaded = function( callback ) {
        if ( _API_LOADED_ ) {
            callback();
        } else {
            _LOADED_CB_.push( callback );
            if ( _API_AUTOLOAD_ ) {
                loadscript();
            }
        }
    };

    /**
     * A public wrapper of the loadscript function.
     *
     * Loads the api manually. This function must be used in every script
     * that disables autoload.
     */
    $.gmapAPILoad = loadscript;

    /**
     * Enables/disables the autoloading mechanism or acts as a getter.
     */
    $.gmapAPIAutoLoad = function( bool ) {
        if ( $.type( bool ) === "undefined" ) {
            return _API_AUTOLOAD_;
        } else {
            _API_AUTOLOAD_ = !!bool;
        }
    };

})( document, window, jQuery );
