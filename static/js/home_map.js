var SpotMap = {
    map: null,

    setup: function() {
        SpotMap.map = L.map('map-view');
        SpotMap.map.on('locationfound', function(e) {
            SpotMap.map.setView(e.latlng, 16);
        })
        SpotMap.map.on('locationerror', function(e) {
            SpotMap.map.setView([40.343990, -74.651451], 16); // Princeton University
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
    },

}

$(document).ready(SpotMap.setup);