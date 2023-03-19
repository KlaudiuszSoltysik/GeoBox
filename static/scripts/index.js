var map;
var userMarker;

var refreshLocation = window.setInterval(() => {
    navigator.geolocation.getCurrentPosition(success, error)
}, 10000);

function success(position) {
    var lat = position.coords.latitude;
    var lon = position.coords.longitude;

    document.getElementById("location").innerHTML = `Latitude: ${lat}<br>Longitude: ${lon}<br>Accuracy: ${Math.round(position.coords.accuracy)} m`;

    updateMap(lat, lon);
}

function error(msg) {
    document.getElementById("location").innerHTML = msg;
}

function initMap() {
    var mapElement = document.getElementById("user-location-map")

    map = new google.maps.Map(mapElement, {
        zoom: 6,
        center: new google.maps.LatLng(52, 21),
        disableDefaultUI: true,
        zoomControl: true,
    });
    userMarker = new google.maps.Marker({
        position: new google.maps.LatLng(0, 0),
        map: map,
    });

    navigator.geolocation.getCurrentPosition((position) => {
        var lat = position.coords.latitude;
        var lon = position.coords.longitude;

        document.getElementById("location").innerHTML = `Latitude: ${lat}<br>Longitude: ${lon}<br>Accuracy: ${Math.round(position.coords.accuracy)}m`;

        var location = new google.maps.LatLng(lat, lon);

        userMarker.setPosition(location);
        map.setCenter(location)
        map.setZoom(10)
    }, error, {
        timeout: 30000,
        enableHighAccuracy: true
    });

    var boxesLat = mapElement.dataset.boxes_lat.replace("[", "").replace("]", "").split(", ");
    var boxesLon = mapElement.dataset.boxes_lon.replace("[", "").replace("]", "").split(", ");
    var boxesImg = mapElement.dataset.boxes_img.replace("[", "").replace("]", "").split(", ");
    var boxesId = mapElement.dataset.boxes_id.replace("[", "").replace("]", "").split(", ");

    for (var i = 0; i < boxesLat.length; i++) {
        var m = new google.maps.Marker({
            position: new google.maps.LatLng(boxesLat[i], boxesLon[i]),
            map: map,
            icon: {url: "./static" + boxesImg[i].replace("<FieldFile: static", "").replace(">", ""), scaledSize: new google.maps.Size(35, 35)},
            id: boxesId[i]
        });

        google.maps.event.addListener(m, "click", ((m) => {
            return () => {
                window.location.href = `/box/${m.id}`;
          }})(m, i));    
    }

    var overlay = new google.maps.OverlayView();
     overlay.draw = function () {
         this.getPanes().markerLayer.id="markerLayer";
     };
     overlay.setMap(map);
}

function updateMap(lat, lon) {
    var location = new google.maps.LatLng(lat, lon);

    userMarker.setPosition(location);
}