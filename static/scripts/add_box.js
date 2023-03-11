var findMeBtn = document.getElementById('find-me-btn');

findMeBtn.addEventListener('click', () => {
    navigator.geolocation.getCurrentPosition(success, error, {
        timeout: 30000,
        enableHighAccuracy: true
    });
});

function success(position) {
    var lat = position.coords.latitude;
    var lon = position.coords.longitude;

    document.getElementById('id_lat').value = lat;
    document.getElementById('id_lon').value = lon;
}

function error(msg) {
    findMeBtn.innerHTML = msg;
}

document.getElementById('id_description').addEventListener("input", () => {
    document.getElementById('length-counter').textContent = 5000 - this.value.length + "/5000";
});