function deleteItem(id) {
    if (confirm("Are you confirm to delete?")) {
        $.ajax({
            url: "/?id=" + id,
            type: "DELETE",
            success: function (json) {
                location.replace("/");
            },
            error: function (error) {
                alert(JSON.stringify(error.message));
            }
        });
    }
}
function typeSelect(value) {
    document.getElementById("wish").style.display = "none";
    document.getElementById("play").style.display = "none";
    if (value == 1) document.getElementById("wish").style.display = "flex";
    if (value == 3) document.getElementById("play").style.display = "flex";
}
function repeatSelect(value) {
    var onece = document.getElementById("once");
    var time = document.getElementById("time");
    var allday = document.getElementById("allday");
    var daily = document.getElementById("daily");
    var day = document.getElementById("day");
    var monthly = document.getElementById("monthly");
    var nota = document.getElementById("nota");
    var notice = document.getElementById("notice");
    allday.style.display = "none";
    time.style.display = "none";
    daily.style.display = "none";
    onece.style.display = "none";
    day.style.display = "none";
    monthly.style.display = "none";
    notice.style.display = "none";
    if (value == 1) {
        if (onece.style.display === "none") {
            onece.style.display = "flex";
        }
        if (notice.style.display === "none") {
            notice.style.display = "flex";
            nota.innerHTML = "This event will execute only one time."
        }
    }
    // allday
    if (value == 2) {

        if (allday.style.display === "none") {
            allday.style.display = "flex";
        }
        if (notice.style.display === "none") {
            notice.style.display = "flex";
            nota.innerHTML = "This event will execute every hours on that date."
        }
    }
    // daily
    if (value == 3) {
        if (daily.style.display === "none") {
            daily.style.display = "flex";
        }
        if (time.style.display === "none") {
            time.style.display = "flex";
        }
        if (notice.style.display === "none") {
            notice.style.display = "flex";
            nota.innerHTML = "This event will be held on every weekday and time that has been set."
        }

    }
    // monthly 
    if (value == 4) {
        var today = new Date();
        if (day.style.display === "none") {
            day.style.display = "flex";
        }
        var selectday = document.getElementById("eday");
        selectday.options.length = 0;
        for (let i = 0; i < 31; i++) {
            var option = document.createElement("option");
            option.text = i + 1;
            option.value = i + 1;
            selectday.add(option);
        }
        if (notice.style.display === "none") {
            notice.style.display = "flex";
            nota.innerHTML = "This event will be held every month on the day that has been set and every hour."
        }
        selectday.value = today.getDate();
    }
    // yearly
    if (value == 5) {
        if (monthly.style.display === "none") {
            monthly.style.display = "flex";
        }
        if (day.style.display === "none") {
            day.style.display = "flex";
        }
        if (notice.style.display === "none") {
            notice.style.display = "flex";
            nota.innerHTML = "This event will be held on every year on month and day that has been set."
        }
    }
}
function monthSelect(value) {
    var today = new Date();
    var lastDayOfMonth = getDaysInMonth(value, today.getFullYear());
    var selectday = document.getElementById("eday");
    selectday.options.length = 0;
    for (let i = 0; i < lastDayOfMonth; i++) {
        var option = document.createElement("option");
        option.text = i + 1;
        option.value = i + 1;
        selectday.add(option);
    }
    selectday.value = today.getDate();

}
function getDaysInMonth(m, y) {
    lastday = new Date(y, m, 0).getDate();
    return new Date(y, m, 0).getDate();
}
function getMedia() {
    $.getJSON("/getmedia", function (data, status) {
        if (status == 'success') {
            var select = document.getElementById("media");
            var option = document.createElement("option");
            select.options.length = 0;
            option.text = "Choose";
            option.value = "";
            select.add(option);
            try {
                data.forEach((obj) => {
                    Object.entries(obj).forEach(([key, value]) => {
                        const option = document.createElement("option");
                        option.text = key
                        option.value = value
                        select.add(option)
                    });
                });
            }
            catch (error) {
                alert(error.toString);
            }
        }
    }).fail(function (jqxhr, textStatus, error) {
        // Error remove play option
        $("#type option[value='3']").remove();
    });
}
function getTypenRepeat() {
    $.getJSON("/getrepeat", function (data, status) {
        if (status == 'success') {
            var select = document.getElementById("repeat");
            select.options.length = 0;
            var option = document.createElement("option");
            option.text = "Choose..";
            option.value = "";
            select.add(option);
            try {
                for (let t = 0; t < data.data.length; t++) {
                    var option = document.createElement("option");
                    option.text = data.data[t].name;
                    option.value = data.data[t].id;
                    select.add(option);
                }
            }
            catch (error) {
                alert(error.toString());
            }
        }
        else {
            alert(data.message);
        }
    })
}
function getTypenType() {
    $.getJSON("/gettype", function (data, status) {
        if (status == 'success') {
            var select = document.getElementById("type");
            select.options.length = 0;
            var option = document.createElement("option");
            option.text = "Choose..";
            option.value = "";
            select.add(option);
            try {
                for (let t = 0; t < data.data.length; t++) {
                    var option = document.createElement("option");
                    if (data.data[t].id != 2) {
                        option.text = data.data[t].name;
                        option.value = data.data[t].id;
                        select.add(option);
                    }
                }
                select.value = "1";
                // select.disabled = true;
            }
            catch (error) {
                alert(error.toString());
            }
        }
        else {
            alert(data.message);
        }
    })
}
function Validate() {
    // <!--name-->
    if (document.getElementById('ename').value == "") {
        document.getElementById('nameFeedback').innerHTML = 'Pleace enter event name.';
        return false;
    }
    document.getElementById('nameFeedback').innerHTML = '';

    // <!--text-->
    if (document.getElementById('type').value == 1 && document.getElementById('etext').value == "") {
        document.getElementById('textFeedback').innerHTML = 'Pleace enter event text.';
        return false;
    }
    document.getElementById('textFeedback').innerHTML = '';

    // <!--media-->
    if (document.getElementById('type').value == 3 && document.getElementById('media').value == "") {
        document.getElementById('mediaFeedback').innerHTML = 'Pleace select media.';
        return false;
    }
    document.getElementById('mediaFeedback').innerHTML = '';

    // <!--type-->
    if (document.getElementById('type').value == "") {
        document.getElementById('repeatFeedback').innerHTML = 'Pleace select type field.';
        return false;
    }
    document.getElementById('repeatFeedback').innerHTML = '';

    // <!--repeate-->
    if (document.getElementById('repeat').value == "") {
        document.getElementById('repeatFeedback').innerHTML = 'Pleace select repeat field.';
        return false;
    }
    document.getElementById('repeatFeedback').innerHTML = '';

    // <!--weekday-->
    if (document.getElementById("repeat").value == 3) {
        var checkboxes = document.getElementsByName('weekday');
        var isChecked = false;
        for (var i = 0; i < checkboxes.length; i++) {
            if (checkboxes[i].checked) {
                isChecked = true;
                break;
            }
        }
        if (!isChecked) {
            document.getElementById('weekdayFeedback').innerHTML = 'Please select at least one weekday.';
            return false;
        }
    }
    document.getElementById('weekdayFeedback').innerHTML = '';

    return true;
}
function delete_group() {
    $("input:checkbox[name=eventId]:checked").each(function () {
        $.ajax({
            url: "/?id=" + $(this).val(),
            type: "DELETE",
            success: function (json) {
                location.replace("/");
            },
            error: function (error) {
                alert(JSON.stringify(error.error.message));
            }
        });
    });
}
function check() {
    var isChecked = false;
    $("input:checkbox[name=eventId]:checked").each(function () {
        isChecked = true;
    });
    btnDeleteGroup.hidden = !isChecked;
}
window.addEventListener("load", function () {
    var now = new Date();
    var utcString = now.toISOString().substring(0, 19);
    var year = now.getFullYear();
    var month = now.getMonth() + 1;
    var day = now.getDate();
    var hour = now.getHours();
    var minute = now.getMinutes();
    var second = now.getSeconds();
    var localDate = (day < 10 ? "0" + day.toString() : day) + "/" + (month < 10 ? "0" + month.toString() : month) + "/" + year;
    var localDatetime = year + "-" +
        (month < 10 ? "0" + month.toString() : month) + "-" +
        (day < 10 ? "0" + day.toString() : day) + "T" +
        (hour < 10 ? "0" + hour.toString() : hour) + ":" +
        (minute < 10 ? "0" + minute.toString() : minute) +
        utcString.substring(16, 19);
    var localTime = (hour < 10 ? "0" + hour.toString() : hour) + ":" +
        (minute < 10 ? "0" + minute.toString() : minute);

    var dtpic1 = document.getElementById("datetimepicker");
    dtpic1.value = localDatetime;
    var tpic1 = document.getElementById("timepicker");
    tpic1.value = localTime;
    var mon = document.getElementById("emonth");
    mon.value = month;
    monthSelect(month);

    getTypenType();
    getTypenRepeat();
    getMedia();

    var today = new Date().toISOString().slice(0, 16);
    document.getElementsByName("datetimepicker")[0].min = today;

    var thisdate = new Date().toISOString().split('T')[0];
    document.getElementById("datepicker").setAttribute('min', thisdate);
    document.getElementById("datepicker").setAttribute('value', thisdate);
});


