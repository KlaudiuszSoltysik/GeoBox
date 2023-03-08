var findMeBtn = document.getElementById('find-me-btn');

findMeBtn.addEventListener('click', () => {
    navigator.geolocation.getCurrentPosition(success, error, { timeout: 30000, enableHighAccuracy: true });
});

function success(position) {
    var lat = Math.round(position.coords.latitude * 1000000) / 1000000;
    var lon = Math.round(position.coords.longitude * 1000000) / 1000000;

    document.getElementById('id_lat').value = lat;
    document.getElementById('id_lon').value = lon;
}

function error(msg) {
    findMeBtn.innerHTML = msg;
}