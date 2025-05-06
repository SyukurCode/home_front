$(document).ready(function () {
    var lat = 3.139003;
    var lon = 101.686852;
    apikey = document.getElementById("apikey").value;
    const url = `https://www.google.com/maps/embed/v1/view?key=${apikey}&center=${lat},${lon}&zoom=14&maptype=roadmap`;
    document.getElementById("maps").src = url;
    getLocation() 
    });
