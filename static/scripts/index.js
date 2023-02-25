window.addEventListener('load', () => {
    navigator.geolocation.getCurrentPosition(success, error, {timeout: 10000, enableHighAccuracy: true});
});

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
    var location = new google.maps.LatLng(52, 21)

    var map = new google.maps.Map(document.getElementById('user-location-map'), {
        zoom: 6,
        center: location,
    });
    var marker = new google.maps.Marker({
        position: location,
        map: map,
    });
}

function updateMap(lat, lon) {
    var location = new google.maps.LatLng(lat, lon)

    map = new google.maps.Map(document.getElementById('user-location-map'), {
        zoom: 17,
        center: location,
    });
    marker = new google.maps.Marker({
        position: location,
        map: map,
    });
}