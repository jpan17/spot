var SpotMap = {
    map: null,
    circles: null,
    popups: null,
    request: null,
    redIcon: null,
    defaultZoom: 15,

    setup: function() {
        SpotMap.defaultZoom = 15;
        SpotMap.redIcon = new L.Icon({
            iconUrl: '/static/img/icon/leaflet/marker-icon-2x-red.png',
            shadowUrl: '/static/img/icon/leaflet/marker-shadow.png',
            iconSize: [25, 41],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34],
            shadowSize: [41, 41]
        });

        SpotMap.map = L.map('map-view');
        SpotMap.map.setMinZoom(3);
        // Center map
        SpotMap.map.on('locationfound', function(e) {
            SpotMap.map.setView(e.latlng, SpotMap.defaultZoom);
            let marker = L.marker(e.latlng, {icon: SpotMap.redIcon}).addTo(SpotMap.map);
            marker.bindTooltip("Your Location");
            marker.fire('mouseover');
        })
        SpotMap.map.on('locationerror', function(e) {
            SpotMap.map.setView([40.343990, -74.651451], SpotMap.defaultZoom); // Princeton University
        });
        SpotMap.map.locate({ maxZoom: 18, enableHighAccuracy: true });
        
        // Set tile layer of map
        // L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{tileSize}/{z}/{x}/{y}?access_token={accessToken}', {
        //     attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        //     maxZoom: 18,
        //     id: 'mapbox/streets-v11',
        //     tileSize: 256,
        //     zoomOffset: 1,
        //     accessToken: 'pk.eyJ1IjoidGVhbXNwb3QiLCJhIjoiY2s5bDJuOGFiMGpxdzNlbWlxYWY3Y2YwbSJ9.5Z_KoMgEzIBWzus_YeuNlQ'
        // }).addTo(SpotMap.map);
        L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(SpotMap.map);

        // Get listings
        SpotMap.circles = [];
        SpotMap.popups = [];
        SpotMap.loadListings();
    },

    loadListings: function() {
        var url = "/api/listings/json?zip_code=";
        $("input[id^=\"pet_type_\"]:checked").each(function() {
            url += "&" + $(this).attr("id") + "=true";
        });
        $("input[id^=\"activity_\"]:checked").each(function() {
            url += "&" + $(this).attr("id") + "=true";
        });

        if(SpotMap.request != null) {
            SpotMap.request.abort();
        }

        SpotMap.request = $.ajax({
            type: "GET",
            url: url,
            success: function(response) {
                SpotMap.popups.forEach(popup => SpotMap.map.removeLayer(popup));
                SpotMap.circles.forEach(circle => SpotMap.map.removeLayer(circle));
                SpotMap.popups = [];
                SpotMap.circles = [];
                // Populate with new listings
                response.forEach(listing => {
                    // For each listing, add a circle, then add a popup for the circle
                    let circle = L.circle([listing.lat, listing.lng], {
                                    color: '#48a4fa',
                                    fillColor: '#4ab5f7',
                                    fillOpacity: 0.3,
                                    radius: 375
                                }).addTo(SpotMap.map);
                    SpotMap.circles.push(circle);
                
                    // Construct popup
                    let content = L.DomUtil.create('div', 'content');
                    let description = listing.pet_name.toUpperCase() + " (" + listing.pet_type + ")<br>" +
                        "<span class=\"time\"><em>START</em>: " + listing.start_time + "&nbsp;&nbsp;</span><br>" + 
                        "<span class=\"time\"><em>END</em>: " + listing.end_time + "&nbsp;&nbsp;</span><br>" + 
                        "<span class=\"activities\"><em>ACTIVITIES</em>: " + listing.activities + "</span>";
                    let image = "";
                    if(listing.pet_image_url) {
                        image = "<div class=\"" + listing.pet_type.toLowerCase() + "-image\"" + 
                        " style=\"background-image: url('" + listing.pet_image_url + "')\"></div>";
                    }else {
                        image = "<img src=\"/static/img/portrait/" + listing.pet_type.toLowerCase() + ".png\"" + 
                        " class=\"" + listing.pet_type.toLowerCase() + "\">";
                    }
                    content.innerHTML = "<div class=\"flex-popup\">" + 
                                            "<div class=\"description\">" + 
                                                description +
                                            "</div>" +
                                            "<div class=\"background\">" +  
                                                image + 
                                            "</div>" +
                                        "</div>";

                    // Create, bind, and store popup
                    let popup = L.popup({
                        maxWidth: 1000
                    }).setContent(content);
                    circle.bindPopup(popup);
                    circle.on('mouseover', function(e){
                        circle.openPopup();
                    });  
                    SpotMap.popups.push(popup);

                    // Catch clicks on popup
                    L.DomEvent.addListener(content, 'click', function(event){
                        Spot.redirect("/listings/" + listing.id);
                    });
                });
            }
        });
    },

    centerMap: function(lat, lng) {
        SpotMap.map.flyTo([lat, lng], SpotMap.defaultZoom);
    }
};

var SpotMapFilters = {
    autoLoad: false, // Determines whether to automatically send AJAX on update of form, or only on submit

    setup: function() {
        SpotMapFilters.update_activities_button();
        SpotMapFilters.update_pet_types_button();

        $("#filter-form").submit(function(e) {
            e.preventDefault();
            let lat = parseFloat($('input#lat').val());
            let lng = parseFloat($('input#lng').val());
            if(!isNaN(lat) && !isNaN(lng)) {
                if(lat >= -90 && lat <= 90 && lng >= -180 && lng <= 180) {
                    SpotMap.centerMap(lat, lng);
                }
            }
            $('input#lat').val("");
            $('input#lng').val("");
            SpotMapAlgolia.setVal("");
            SpotMap.loadListings();
        })
    },

    // Uncheck all pet_types
    clear_pet_types: function() {
        $('#pet_type_filter_button [id^="pet_type_"]:checked').prop("checked", false);
        $('#pet_type_filter_button').removeClass('has-filters');
        if(SpotMapFilters.autoLoad) SpotMap.loadListings();
    },

    // Register click on pet_types_dropdown (including each of the checkboxes)
    pet_types_dropdown_click: function(event) {
        event.stopPropagation();
        SpotMapFilters.update_pet_types_button();
        if(SpotMapFilters.autoLoad) SpotMap.loadListings();
    },

    // Add class if and only if any checked pet_types
    update_pet_types_button: function() {
        if($('#pet_type_filter_button [id^="pet_type_"]:checked').length === 0) {
            $('#pet_type_filter_button').removeClass('has-filters');
        }else {
            $('#pet_type_filter_button').addClass('has-filters');
        }
    },

    // Uncheck all activities
    clear_activities: function() {
        $('#activities_filter_button [id^="activity_"]:checked').prop("checked", false);
        $('#activities_filter_button').removeClass('has-filters');
        if(SpotMapFilters.autoLoad) SpotMap.loadListings();
    },

    // Register click on activities dropdown (including each of the checkboxes)
    activities_dropdown_click: function(event) {
        event.stopPropagation();
        SpotMapFilters.update_activities_button();
        if(SpotMapFilters.autoLoad) SpotMap.loadListings();
    },

    // Add class if and only if any checked activities
    update_activities_button: function() {
        if($('#activities_filter_button [id^="activity_"]:checked').length === 0) {
            $('#activities_filter_button').removeClass('has-filters');
        }else {
            $('#activities_filter_button').addClass('has-filters');
        }
    }
};

var SpotMapAlgolia = {
    autocomplete: null,
    acElement: null,
    acSelector: '#address_input',

    setup: function() {
        SpotMapAlgolia.acElement = document.querySelector(SpotMapAlgolia.acSelector);
        SpotMapAlgolia.autocomplete = places({
            appId: 'plO1SV8YCUC3',
            apiKey: '168cb9867faff5823a430526b0c935df',
            container: SpotMapAlgolia.acElement,
            aroundLatLng: '40.343990,-74.651451', // Princeton University
            useDeviceLocation: true
        });

        // Clear anything that isn't suggested and add ready-to-submit class when a suggestion is chosen
        SpotMapAlgolia.autocomplete.on('change', function(e) {
            $(SpotMapAlgolia.acSelector).removeClass("not-validated");
            $("input#lat").val(e.suggestion.latlng.lat);
            $("input#lng").val(e.suggestion.latlng.lng);
        });

        $(SpotMapAlgolia.acElement).on('input', function(e) {
            $(SpotMapAlgolia.acSelector).addClass("not-validated");
        })
        $(SpotMapAlgolia.acElement).change(function(e) {
            if($(this).hasClass("not-validated")) {
                SpotMapAlgolia.autocomplete.setVal("");
                $("input#lat").val("");
                $("input#lng").val("");
            }
        });
    },

    setVal: function(val) {
        SpotMapAlgolia.autocomplete.setVal(val);
    }
};

$(document).ready(SpotMapFilters.setup);
$(document).ready(SpotMap.setup);
$(document).ready(SpotMapAlgolia.setup);