var positions = document.getElementsByClassName('position');

window.onload = navigator.geolocation.getCurrentPosition(success);

function success(position) {
    var lat2 = position.coords.latitude;
    var lon2 = position.coords.longitude;

    for (let i = 0; i < positions.length; i++) {
        var lat1 = parseFloat(positions[i].dataset.lat);
        var lon1 = parseFloat(positions[i].dataset.lon);
        drawArrow(lat1, lon1, lat2, lon2, i)
        positions[i].innerHTML = getDistanceFromLatLonInKm(lat1, lon1, lat2, lon2) + ' m'
    }
}

function drawArrow(lat1, lon1, lat2, lon2, i) {
    context = document.getElementsByTagName('canvas')[i].getContext('2d');
    context.lineWidth = 5;
    const R = 100;
    const headLen = 20;
    const angle = angleFromCoordinate(lat1, lon1, lat2, lon2);
    const toX = 100 + R * Math.cos(angle)
    const toY = 100 + R * Math.sin(angle)
    const arrowAngle = Math.atan2(toX - 100, toY - 100);

    context.beginPath();
    context.moveTo(100, 100);
    context.lineTo(toX, toY);
    context.moveTo(toX - headLen * Math.sin(arrowAngle - Math.PI / 6), toY - headLen * Math.cos(arrowAngle - Math.PI / 6));
    context.lineTo(toX, toY);
    context.lineTo(toX - headLen * Math.sin(arrowAngle + Math.PI / 6), toY - headLen * Math.cos(arrowAngle + Math.PI / 6));
    context.stroke();
}

function angleFromCoordinate(lat1, lon1, lat2, lon2) {
    const p1 = {
        x: lat1,
        y: lon1
    };
    const p2 = {
        x: lat2,
        y: lon2
    };

    return Math.atan2(p1.y - p2.y, p1.x - p2.x) - Math.PI / 2;
}

function getDistanceFromLatLonInKm(lat1, lon1, lat2, lon2) {
    const R = 6371;
    var dLat = deg2rad(lat2 - lat1);
    var dLon = deg2rad(lon2 - lon1);
    var a = Math.sin(dLat / 2) * Math.sin(dLat / 2) + Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) * Math.sin(dLon / 2) * Math.sin(dLon / 2);
    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    var d = R * c * 1000;
    return Math.round(d)
}

function deg2rad(deg) {
    return deg * (Math.PI / 180);
}