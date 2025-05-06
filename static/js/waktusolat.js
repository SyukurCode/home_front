
function updateClock() {
    const now = new Date();
    const timeString = now.toLocaleTimeString();
    document.getElementById('time_now').innerHTML = timeString;
    check()
}

function check()
{
    const now = new Date()
    const hijriDateMs = new Intl.DateTimeFormat('ms-MY-u-ca-islamic', {
        day: 'numeric',
        month: 'long',
        year: 'numeric'
      }).format(new Date());
    const current = convertTo24Hour(document.getElementById('time_now').innerHTML)
    const waktu_imsak = convertTo24Hour(document.getElementById("time-imsak").innerHTML)
    const waktu_subuh = convertTo24Hour(document.getElementById("time-subuh").innerHTML)
    const waktu_zohor = convertTo24Hour(document.getElementById("time-zohor").innerHTML)
    const waktu_asar = convertTo24Hour(document.getElementById("time-asar").innerHTML)
    const waktu_maghrib = convertTo24Hour(document.getElementById("time-maghrib").innerHTML)
    const waktu_isyak = convertTo24Hour(document.getElementById("time-isyak").innerHTML)
    const waktu_syuruk = convertTo24Hour(document.getElementById("time-syuruk").innerHTML)
    const waktu_dhuha = convertTo24Hour(document.getElementById("time-dhuha").innerHTML)

    const [hours, minutes, seconds] = current.split(":").map(Number);
    const date_current = new Date(now.getFullYear(), now.getMonth(), now.getDate(), hours, minutes, seconds);
    // const date_current = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 5, 52, seconds);
    const date_imsak = new Date(now.getFullYear(), now.getMonth(), now.getDate(), waktu_imsak.split(":")[0], waktu_imsak.split(":")[1], 0);
    const date_zohor = new Date(now.getFullYear(), now.getMonth(), now.getDate(), waktu_zohor.split(":")[0], waktu_zohor.split(":")[1], 0);
    const date_subuh = new Date(now.getFullYear(), now.getMonth(), now.getDate(), waktu_subuh.split(":")[0], waktu_subuh.split(":")[1], 0);
    const date_asar = new Date(now.getFullYear(), now.getMonth(), now.getDate(), waktu_asar.split(":")[0], waktu_asar.split(":")[1], 0);
    const date_maghrib = new Date(now.getFullYear(), now.getMonth(), now.getDate(), waktu_maghrib.split(":")[0], waktu_maghrib.split(":")[1], 0);
    const date_isyak = new Date(now.getFullYear(), now.getMonth(), now.getDate(), waktu_isyak.split(":")[0], waktu_isyak.split(":")[1], 0);
    const date_syuruk = new Date(now.getFullYear(), now.getMonth(), now.getDate(), waktu_syuruk.split(":")[0], waktu_syuruk.split(":")[1], 0);
    const date_dhuha = new Date(now.getFullYear(), now.getMonth(), now.getDate(), waktu_dhuha.split(":")[0], waktu_dhuha.split(":")[1], 0);
   
    const _Imsak = (date_current - date_imsak);
    const isImsak = Math.floor(_Imsak / 1000 / 60);

    const _Subuh = (date_current - date_subuh);
    const isSubuh = Math.floor(_Subuh / 1000 / 60);

    const _Zohor = (date_current - date_zohor);
    const isZohor = Math.floor(_Zohor / 1000 / 60);

    const _Asar = (date_current - date_asar);
    const isAsar = Math.floor(_Asar / 1000 / 60);

    const _Maghrib = (date_current - date_maghrib);
    const isMaghrib = Math.floor(_Maghrib / 1000 / 60);

    const _Isyak = (date_current - date_isyak);
    const isIsyak = Math.floor(_Isyak / 1000 / 60);

    const _Syuruk = (date_current - date_syuruk);
    const isSyuruk = Math.floor(_Syuruk / 1000 / 60);

    const _Dhuha = (date_current - date_dhuha);
    const isDhuha = Math.floor(_Dhuha / 1000 / 60);

    document.getElementById("date_now").innerHTML = now.toLocaleDateString('ms-MY', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
    document.getElementById("ago").innerHTML = hijriDateMs;

    const sekarang_text =  "<i class='far fa-bell'></i> Sekarang!";
    const akan_text =  "<i class='far fa-bell'></i> @{minute_text} minit lagi";
    
    if( isImsak >= 0 && isImsak <= 5){
        document.getElementById("status-imsak").innerHTML = sekarang_text;
        document.getElementById("card-imsak").classList.add("solat-time-card");
    }
    else{
        document.getElementById("status-imsak").innerHTML = "";
        document.getElementById("card-imsak").classList.remove("solat-time-card");
    }

    if( isSubuh >= 0 && isSubuh <= 10){
        document.getElementById("status-subuh").innerHTML = sekarang_text;
        document.getElementById("card-subuh").classList.add("solat-time-card");
    }
    else if( isSubuh < 0 && isSubuh > -10){
        document.getElementById("status-subuh").innerHTML = akan_text.replace("@{minute_text}", Math.abs(isSubuh));
        document.getElementById("card-subuh").classList.add("solat-time-card");
    }
    else{
        document.getElementById("status-subuh").innerHTML = "";
        document.getElementById("card-subuh").classList.remove("solat-time-card");
    }

    if( isZohor >= 0 && isZohor <= 10){
        document.getElementById("status-zohor").innerHTML = sekarang_text;
        document.getElementById("card-zohor").classList.add("solat-time-card");
    }
    else if( isZohor < -10 && isZohor > 0){
        document.getElementById("status-zohor").innerHTML = akan_text.replace("@{minute_text}", Math.abs(isZohor));
        document.getElementById("card-zohor").classList.add("solat-time-card")
    }
    else{
        document.getElementById("status-zohor").innerHTML = "";
        document.getElementById("card-zohor").classList.remove("solat-time-card");
    }

    if( isAsar >= 0 && isAsar <= 10){
        document.getElementById("status-asar").innerHTML = sekarang_text
        document.getElementById("card-asar").classList.add("solat-time-card");
    }
    else if( isAsar < 0 && isAsar > -10){
        document.getElementById("status-asar").innerHTML = akan_text.replace("@{minute_text}", Math.abs(isAsar));
        document.getElementById("card-asar").classList.add("solat-time-card");
    }
    else{
        document.getElementById("status-asar").innerHTML = "";
        document.getElementById("card-asar").classList.remove("solat-time-card");
    }
    if( isMaghrib >= 0 && isMaghrib <= 10){
        document.getElementById("status-maghrib").innerHTML = sekarang_text;
        document.getElementById("card-maghrib").classList.add("solat-time-card");
    }
    else if( isMaghrib < 0 && isMaghrib > -10){
        document.getElementById("status-maghrib").innerHTML = akan_text.replace("@{minute_text}", Math.abs(isMaghrib))
        document.getElementById("card-maghrib").classList.add("solat-time-card");
    }
    else{
        document.getElementById("status-maghrib").innerHTML = "";
        document.getElementById("card-maghrib").classList.remove("solat-time-card");
    }

    if( isIsyak >= 0 && isIsyak <= 10){
        document.getElementById("status-isyak").innerHTML = sekarang_text;
        document.getElementById("card-isyak").classList.add("solat-time-card");
    }
    else if( isIsyak < 0 && isIsyak > -10){
        document.getElementById("status-isyak").innerHTML = akan_text.replace("@{minute_text}", Math.abs(isIsyak));
        document.getElementById("card-isyak").classList.add("solat-time-card");
    }
    else{
        document.getElementById("status-isyak").innerHTML = ""
        document.getElementById("card-isyak").classList.remove("solat-time-card");
    }

    if( isSyuruk >= 0 && isSyuruk <= 5){
        document.getElementById("status-syuruk").innerHTML = sekarang_text;
        document.getElementById("card-syuruk").classList.add("solat-time-card");
    }
    else{
        document.getElementById("status-syuruk").innerHTML = "";
        document.getElementById("card-syuruk").classList.remove("solat-time-card");
    }   

    if( isDhuha >= 0 && isDhuha <= 5){
        document.getElementById("status-dhuha").innerHTML = sekarang_text;
        document.getElementById("card-dhuha").classList.add("solat-time-card")
    }
    else{
        document.getElementById("status-dhuha").innerHTML = "";
        document.getElementById("card-dhuha").classList.remove("solat-time-card");
    }   

    
}
function convertTo24Hour(time12h) {
    const [time, modifier] = time12h.split(" ");
    let [hours, minutes, seconds] = time.split(":");
  
    hours = parseInt(hours, 10);
  
    if (modifier === "PM" && hours !== 12) {
      hours += 12;
    }
    if (modifier === "AM" && hours === 12) {
      hours = 0;
    }
  
    return `${hours.toString().padStart(2, '0')}:${minutes}:${seconds}`;
  }


setInterval(updateClock, 1000);
updateClock(); // Initial call

