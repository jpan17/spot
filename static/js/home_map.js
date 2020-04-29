var SpotMap = {
    map: null,
    circles: null,
    popups: null,

    setup: function() {
        SpotMap.map = L.map('map-view');
        SpotMap.map.setMinZoom(3);
        // Center map
        SpotMap.map.on('locationfound', function(e) {
            SpotMap.map.setView(e.latlng, 15);
        })
        SpotMap.map.on('locationerror', function(e) {
            SpotMap.map.setView([40.343990, -74.651451], 15); // Princeton University
        })
        SpotMap.map.locate({setView: true, maxZoom: 18, enableHighAccuracy: true });
        
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
        var url = "/api/listings/json";
        $.ajax({
            type: "GET",
            url: url,
            success: function(response) {
                SpotMap.circles = [];
                SpotMap.popups = [];
                response.forEach(listing => {
                    // For each listing, add a circle, then add a popup for the circle
                    SpotMap.circles.push(
                        L.circle([listing.lat, listing.lng], {
                            color: '#48a4fa',
                            fillColor: '#4ab5f7',
                            fillOpacity: 0.3,
                            radius: 375
                        }).addTo(SpotMap.map));
                
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
                        image = "<img src=\"/static/img/portrait/" + listing.pet_type.toLowerCase() + ".png\">";
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
                    SpotMap.circles[SpotMap.circles.length - 1].bindPopup(popup);
                    SpotMap.popups.push(popup);

                    // Catch clicks on popup
                    L.DomEvent.addListener(content, 'click', function(event){
                        Spot.redirect("/listings/" + listing.id);
                    });
                });
            }
        });
    },

}

$(document).ready(SpotMap.setup);