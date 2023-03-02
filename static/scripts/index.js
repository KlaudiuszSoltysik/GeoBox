var map;
var marker;

var refreshLocation = window.setInterval(() => {
    navigator.geolocation.getCurrentPosition(success, error, { timeout: 30000, enableHighAccuracy: true })
}, 5000);

function success(position) {
    var lat = Math.round(position.coords.latitude * 1000000) / 1000000;
    var lon = Math.round(position.coords.longitude * 1000000) / 1000000;

    document.getElementById('location').innerHTML = `Latitude: ${lat}<br>Longitude: ${lon}<br>Accuracy: ${Math.round(position.coords.accuracy)}m`;

    updateMap(lat, lon);
}

function error(msg) {
    document.getElementById('location').innerHTML = msg;
}

function initMap() {
    map = new google.maps.Map(document.getElementById('user-location-map'), {
        zoom: 6,
        center: new google.maps.LatLng(52, 21),
        disableDefaultUI: true,
        zoomControl: true,
    });
    marker = new google.maps.Marker({
        position: new google.maps.LatLng(0, 0),
        map: map,
    });

    navigator.geolocation.getCurrentPosition((position) => {
        var lat = Math.round(position.coords.latitude * 1000000) / 1000000;
        var lon = Math.round(position.coords.longitude * 1000000) / 1000000;
    
        document.getElementById('location').innerHTML = `Latitude: ${lat}<br>Longitude: ${lon}<br>Accuracy: ${Math.round(position.coords.accuracy)}m`;
    
        var location = new google.maps.LatLng(lat, lon);

        marker.setPosition(location);
        map.setCenter(location)
        map.setZoom(18)
    }, error, { timeout: 30000, enableHighAccuracy: true });
}

function updateMap(lat, lon) {
    var location = new google.maps.LatLng(lat, lon);

    marker.setPosition(location);
}