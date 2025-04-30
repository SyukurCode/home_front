
function updateClock() {
    const now = new Date();
    const timeString = now.toLocaleTimeString();
    document.getElementById('time_now').innerHTML = timeString;
}

setInterval(updateClock, 1000);
updateClock(); // Initial call
