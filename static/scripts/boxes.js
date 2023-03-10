var positions = document.getElementsByClassName('position');

window.onload =  navigator.geolocation.getCurrentPosition(success, () => {}, { timeout: 30000, enableHighAccuracy: true });

function success(position) {
    var lat2 = position.coords.latitude;
    var lon2 = position.coords.longitude;

    for (let pos of positions) {
        var lat1 = parseFloat(pos.dataset.lat);
        var lon1 = parseFloat(pos.dataset.lon);
        drawArrow(lat1, lon1, lat2, lon2)
    }
}

function drawArrow(lat1, lon1, lat2, lon2) {
    context = document.getElementById('c').getContext('2d');
    context.lineWidth = 5;
    context.clearRect(0, 0, 200, 200);
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
    const p1 = {x: lat1, y: lon1};
    const p2 = {x: lat2, y: lon2};

    return Math.atan2(p1.y - p2.y, p1.x - p2.x) * 180 / Math.PI;
}