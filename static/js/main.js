
function ValidateRegister() {
    if (document.getElementById("password").value === document.getElementById("re-password").value) {
        document.getElementById('passwordFeedback').innerHTML = '';
        document.getElementById('re-passwordFeedback').innerHTML = '';
        return true;
    }
    document.getElementById('passwordFeedback').innerHTML = 'password not match';
    document.getElementById('re-passwordFeedback').innerHTML = 'password not match';
    return false;

}
function validatePassword() {
    var p = document.getElementById('password').value,
        errors = [];
    if (p.length < 8) {
        errors.push("Your password must be at least 8 characters");
    }
    if (p.search(/[a-z]/i) < 0) {
        errors.push("Your password must contain at least one letter.");
    }
    if (p.search(/[0-9]/) < 0) {
        errors.push("Your password must contain at least one digit.");
    }
    if (errors.length > 0) {
        document.getElementById('passwordFeedback').innerHTML = errors.join("\n");
        return false;
    }
    return true;
}
function changePassword() {
    var current_password = document.getElementById("oldPassword").value;
    var new_password = document.getElementById("password").value;
    var confirm_password = document.getElementById("re-password").value;

    if (validatePassword()) {
        if (new_password == confirm_password) {

            const payload = { 'password': current_password, 'new-password': new_password };
            $.ajax({
                url: "/changepassword",
                type: "POST",
                data: JSON.stringify(payload),
                contentType: "application/json; charset=utf-8",
                traditional: true,
                success: function (json) {

                    current_password = '';
                    new_password = '';
                    confirm_password = '';

                    $("#account").modal("hide");
                    alert(JSON.stringify(json.message));
                },
                error: function (error) {
                    const msg = error.responseJSON.message
                    document.getElementById('oldPasswordFeedback').innerHTML = msg;
                    document.getElementById('passwordFeedback').innerHTML = '';
                    document.getElementById('re-passwordFeedback').innerHTML = '';
                }
            });

        } else {
            document.getElementById('oldPasswordFeedback').innerHTML = '';
            document.getElementById('passwordFeedback').innerHTML = 'password not match';
            document.getElementById('re-passwordFeedback').innerHTML = 'Confirm password not match';
        }
    }

}

function account(type) {
    if (type == "account") {
        document.getElementById("accountTitle").innerHTML = "Account";
    } else {
        document.getElementById("accountTitle").innerHTML = "Register";
    }
    $("#account").modal("show");
}

$(document).ready(function () {
    $("#btnAccount").click(function () {
        $("#account").modal("toggle");
        document.getElementById("accountTitle").innerHTML = "Account";
        document.getElementById("frmPassword").hidden = true;
        document.getElementById("frmRePassword").hidden = true;
        document.getElementById("username").readOnly = true;
        document.getElementById("email").readOnly = true
        document.getElementById("createdBy").hidden = false;
        document.getElementById("createdDate").hidden = false;
        document.getElementById("frmCreatedBy").hidden = false;
        document.getElementById("frmCreatedDate").hidden = false;
        document.getElementById("btnSave").hidden = true
        document.getElementById("btnOk").hidden = true;
        document.getElementById("frmUsername").hidden = false;
        document.getElementById("frmEmail").hidden = false;
        document.getElementById("frmOldPassword").hidden = true;
    });
    $("#btnRegister").click(function () {
        $("#account").modal("toggle");
        document.getElementById("accountTitle").innerHTML = "Register";
        document.getElementById("frmPassword").hidden = false;
        document.getElementById("frmRePassword").hidden = false;
        document.getElementById("username").readOnly = false;
        document.getElementById("email").readOnly = false;
        document.getElementById("createdBy").hidden = true;
        document.getElementById("createdDate").hidden = true;
        document.getElementById("frmCreatedBy").hidden = true;
        document.getElementById("frmCreatedDate").hidden = true;
        document.getElementById("btnSave").hidden = false;
        document.getElementById("btnOk").hidden = true;
        document.getElementById("username").value = '';
        document.getElementById("email").value = '';
        document.getElementById("frmUsername").hidden = false;
        document.getElementById("frmEmail").hidden = false;
        document.getElementById("frmOldPassword").hidden = true;
    });
    $("#btnChangePassword").click(function () {
        $("#account").modal("toggle");
        document.getElementById("accountTitle").innerHTML = "Change Password";
        document.getElementById("frmPassword").hidden = false;
        document.getElementById("frmRePassword").hidden = false;
        document.getElementById("frmUsername").hidden = true;
        document.getElementById("frmEmail").hidden = true;
        document.getElementById("createdBy").hidden = true;
        document.getElementById("createdDate").hidden = true;
        document.getElementById("frmCreatedBy").hidden = true;
        document.getElementById("frmCreatedDate").hidden = true;
        document.getElementById("btnSave").hidden = true;
        document.getElementById("btnOk").hidden = false;
        document.getElementById("username").value = '';
        document.getElementById("email").value = '';
        document.getElementById("frmOldPassword").hidden = false;

    });
});