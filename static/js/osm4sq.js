// Generated by CoffeeScript 1.7.1
var init, makeLonLat, setMarker, setPopup, _setMarker;

makeLonLat = function(lonLat) {
  return new OpenLayers.LonLat(lonLat.lon, lonLat.lat).transform(new OpenLayers.Projection("EPSG:4326"), new OpenLayers.Projection("EPSG:900913"));
};

setPopup = function(map, marker, venue) {
  marker.name = venue.name;
  marker.events.register("mouseover", marker, function(evt) {
    this.popup = new OpenLayers.Popup.FramedCloud(venue.id, this.lonlat, null, this.name, null, false);
    return map.addPopup(this.popup);
  });
  return marker.events.register("mouseout", marker, function(evt) {
    return this.popup.hide();
  });
};

_setMarker = function(map, data) {
  var center, key, lonLat, marker, markers, venue, venues, _results;
  if (Object.keys(data).length !== 0) {
    venues = data.items;
    center = data.center;
    lonLat = makeLonLat(center);
    map.setCenter(lonLat, 8);
    markers = new OpenLayers.Layer.Markers("Markers");
    map.addLayer(markers);
    _results = [];
    for (key in venues) {
      venue = venues[key];
      lonLat = makeLonLat(venue.location);
      marker = new OpenLayers.Marker(lonLat);
      setPopup(map, marker, venue);
      _results.push(markers.addMarker(marker));
    }
    return _results;
  } else {
    lonLat = makeLonLat({
      lon: 139.76,
      lat: 35.68
    });
    return map.setCenter(lonLat, 15);
  }
};

setMarker = function(map) {
  return $.get("checkins", function(data) {
    return _setMarker(map, data);
  });
};

init = function() {
  var map, mapnik;
  map = new OpenLayers.Map("canvas");
  mapnik = new OpenLayers.Layer.OSM();
  map.addLayer(mapnik);
  return setMarker(map);
};