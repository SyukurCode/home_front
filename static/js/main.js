
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
function notification() {
    $.ajax({
        url: "/checkeventdue",
        type: "GET",
        contentType: "application/json; charset=utf-8",
        traditional: true,
        success: function (data) {
            var items = JSON.parse(data)
            if(items.length > 0)
            {
                document.getElementById("noticount").style.display = "inline";
                document.getElementById("noticount").innerHTML = items.length;
                document.getElementById("notitotal").innerHTML =  items.length;
                document.getElementById("notiitems").style.display = "inline";
                document.getElementById("see-all").style.display = "inline";
                items.forEach(element => {
                    const notificationItem = `
                        <a href="/detail?id=${element.id}">
                            <div class="notif-icon notif-primary">
                                <i class="fas fa-hand-point-right"></i>
                            </div>
                            <div class="notif-content">
                                <span class="block">${element.Name}</span>
                                <span class="time">${element.Due}</span>
                            </div>
                        </a>`;
                    document.getElementById("notiitem").innerHTML += notificationItem;
                });
            }
            else{
                document.getElementById("noticount").style.display = "none";
                document.getElementById("notiitems").style.display = "none";
                document.getElementById("see-all").style.display = "none";
            }
            
        },
        error: function (xhr, status, data) {
            console.log("error");
        }
    });
}
$(document).ready(function () {
    notification()
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
        document.getElementById("btn-upload").hidden = false;
    });
    $("#btnRegister").click(function () {
        $("#account").modal("toggle");
        document.getElementById("avatarPreview").src = "/static/img/avatar.svg";
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
async function ValidateAvatar(){
    const fileInput = document.getElementById("avatar");
    const filePath = fileInput.value;
    const formData = new FormData();
    // Allowing file type
    var allowedExtensions = /(\.jpg|\.jpeg|\.png|\.gif)$/i;
    if (!allowedExtensions.exec(filePath)) {
        swal("Warning", "Please upload file having extensions .jpeg/.jpg/.png/.gif only.", {
            icon: "warning",
            buttons: {
              confirm: {
                className: "btn btn-warning",
              },
            },
          });
        fileInput.value = '';
        return false;
    } else {
        formData.append('avatar', fileInput.files[0]);
        document.body.style.cursor = 'wait';
        try {
            const response = await fetch('/upload-avatar', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (response.ok) {
                document.getElementById('avatarFeedback').innerText = "Uploaded successfully!";
                document.getElementById('avatarFeedback').classList.remove('text-danger');
                document.getElementById('avatarFeedback').classList.add('text-success');
                try {
                document.getElementById('avatarPreview').src = "data:image/jpeg;base64," + result.data;
                }
                catch (error) {
                    document.getElementById('avatar_img').src = "data:image/jpeg;base64," + result.data;
                }
            } else {
                document.getElementById('avatarFeedback').classList.remove('text-success');
                document.getElementById('avatarFeedback').classList.add('text-danger');
                document.getElementById('avatarFeedback').innerText = result.detail || 'Upload failed!';
            }
        } catch (error) {
            document.getElementById('avatarFeedback').classList.remove('text-success');
            document.getElementById('avatarFeedback').classList.add('text-danger');
            document.getElementById('avatarFeedback').innerText = error || 'Error uploading file!';
        }
        finally {
            document.body.style.cursor = 'default';
        }

        
    }
    return true;
}