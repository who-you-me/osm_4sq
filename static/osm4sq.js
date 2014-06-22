function init() {
    var map = new OpenLayers.Map("canvas");
    var mapnik = new OpenLayers.Layer.OSM();
    map.addLayer(mapnik);

    setMarker(map);
}

function getVenues(data) {
    var nItems = data.items.length;
    var venues = new Array();
    var center = [0, 0];

    for (var i = 0; i < nItems; i++) {
        var venue = data.items[i].venue;
        center[0] += venue.location.lng;
        center[1] += venue.location.lat;

        if (typeof venues[venue.id] === "undefined") {
            venues[venue.id] = {"value": venue, "count": 1};
        } else {
            venues[venue.id]["count"] += 1;
        }
    }

    center[0] /= nItems;
    center[1] /= nItems;

    return [venues, center];
}

function makeLonLat(lonLat) {
    return new OpenLayers.LonLat(lonLat[0], lonLat[1])
        .transform(
            new OpenLayers.Projection("EPSG:4326"),
            new OpenLayers.Projection("EPSG:900913")
        );
}

function setPopup(map, marker, name) {
    marker.name = name;
    marker.events.register("mouseover", marker, function(evt) {
        popup = new OpenLayers.Popup.FramedCloud("Popup",
            this.lonlat,
            null,
            this.name,
            null,
            false
        );
        map.addPopup(popup);
    });
    marker.events.register("mouseout", marker, function(evt) {
        popup.hide();
    });
}

function _setMarker(map, data) {
    if (Object.keys(data).length !== 0) {
        var result = getVenues(data);
        var venues = result[0];
        var center = result[1];

        var lonLat = makeLonLat(center);
        map.setCenter(lonLat, 8);

        var markers = new OpenLayers.Layer.Markers("Markers");
        map.addLayer(markers);

        for (var key in venues) {
            var venue = venues[key];
            var lon = venue.value.location.lng;
            var lat = venue.value.location.lat;
            var lonLat = makeLonLat([lon, lat]);

            var marker = new OpenLayers.Marker(lonLat);
            setPopup(map, marker, venue.value.name);
            markers.addMarker(marker);
        }
    } else {
        var lonLat = makeLonLat([139.76, 35.68])
        map.setCenter(lonLat, 15);
    }
}

function setMarker(map) {
    $.get("checkins", function(data) {
        _setMarker(map, data);
    });
}

