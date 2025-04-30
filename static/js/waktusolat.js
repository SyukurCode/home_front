
function updateClock() {
    const now = new Date();
    const timeString = now.toLocaleTimeString();
    document.getElementById('time_now').innerHTML = timeString;
}

function check()
{
    const now = new Date()
    const current = document.getElementById('time_now').innerHTML
    const waktu_imsak = document.getElementById("time-imsak").innerHTML
    const waktu_subuh = document.getElementById("time-subuh").innerHTML
    const waktu_zohor = document.getElementById("time-zohor").innerHTML
    const waktu_asar = document.getElementById("time-asar").innerHTML
    const waktu_maghrib = document.getElementById("time-maghrib").innerHTML
    const waktu_isyak = document.getElementById("time-isyak").innerHTML


    const date_current = new Date(now.getFullYear,now.getMonth,now.getDay,current.split(":")[0],current.split(":")[1]);
    const date_imsak = new Date("1970-01-01T" + waktu_imsak + ":00");
    const date_zohor = new Date("1970-01-01T" + waktu_zohor + ":00");
    const date_subuh = new Date("1970-01-01T" + waktu_subuh + ":00");
    const date_asar = new Date("1970-01-01T" + waktu_asar + ":00");
    const date_maghrib = new Date("1970-01-01T" + waktu_maghrib + ":00");
    const date_isyak = new Date("1970-01-01T" + waktu_isyak + ":00");
   
    const _Imsak = Math.abs(date_current - date_imsak);
    const isImsak = Math.floor(_Imsak / 1000 / 60);

    const _Subuh = Math.abs(date_current - date_subuh);
    const isSubuh = Math.floor(_Subuh / 1000 / 60);

    const _Zohor = Math.abs(date_current - date_zohor);
    const isZohor = Math.floor(_Zohor / 1000 / 60);

    const _Asar = Math.abs(date_current - date_asar);
    const isAsar = Math.floor(_Asar / 1000 / 60);

    const _Maghrib = Math.abs(date_current - date_maghrib);
    const isMaghrib = Math.floor(_Maghrib / 1000 / 60);

    const _Isyak = Math.abs(date_current - date_isyak);
    const isIsyak = Math.floor(_Isyak / 1000 / 60);

    if( isImsak <= 5){
        document.getElementById("status-imsak").innerHTML = "Sekarang"
    }
    if( isSubuh <= 5){
        document.getElementById("status-subuh").innerHTML = "Sekarang"
    }
    if( isZohor <= 5){
        document.getElementById("status-zohor").innerHTML = "Sekarang"
    }
    if( isAsar <= 50){
        document.getElementById("status-asar").innerHTML = "Sekarang"
    }
    if( isMaghrib <= 5){
        document.getElementById("status-maghrib").innerHTML = "Sekarang"
    }
    if( isIsyak <= 5){
        document.getElementById("status-isyak").innerHTML = "Sekarang"
    }
    document.getElementById("ago").innerHTML = date_current
}


setInterval(updateClock, 1000);
updateClock(); // Initial call
check()
