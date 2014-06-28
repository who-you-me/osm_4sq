makeLonLat = (lonLat) ->
    return new OpenLayers.LonLat(lonLat.lon, lonLat.lat)
        .transform(
            new OpenLayers.Projection("EPSG:4326"),
            new OpenLayers.Projection("EPSG:900913")
        )

setPopup = (map, marker, venue) ->
    marker.name = venue.name
    marker.events.register("mouseover", marker, (evt) ->
        this.popup = new OpenLayers.Popup.FramedCloud(venue.id,
            this.lonlat,
            null,
            this.name,
            null,
            false
        )
        map.addPopup(this.popup)
    )
    marker.events.register("mouseout", marker, (evt) ->
        this.popup.hide()
    )

_setMarker = (map, data) ->
    if Object.keys(data).length != 0
        venues = data.items
        center = data.center

        lonLat = makeLonLat(center)
        map.setCenter(lonLat, 8)

        markers = new OpenLayers.Layer.Markers("Markers")
        map.addLayer(markers)

        for key, venue of venues
            lonLat = makeLonLat(venue.location)

            marker = new OpenLayers.Marker(lonLat)
            setPopup(map, marker, venue)
            markers.addMarker(marker)
    else
        lonLat = makeLonLat({lon: 139.76, lat: 35.68})
        map.setCenter(lonLat, 15);

setMarker = (map) ->
    $.get("checkins", (data) -> _setMarker(map, data))

init = () ->
    map = new OpenLayers.Map("canvas")
    mapnik = new OpenLayers.Layer.OSM()
    map.addLayer(mapnik)

    setMarker(map)

