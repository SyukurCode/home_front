function deleteItem(id) {
    swal({
        title: "Are you sure?",
        text: "You won't be able to revert this!",
        type: "warning",
        buttons: {
            confirm: {
                text: "Yes, delete it!",
                className: "btn btn-success",
            },
            cancel: {
                visible: true,
                className: "btn btn-danger",
            },
        },
    }).then((Delete) => {
        if (Delete) {
            $.ajax({
                url: "/?id=" + id,
                type: "DELETE",
                success: function (json) {
                    location.replace("/");
                },
                error: function (error) {
                    swal("Error!", JSON.stringify(error.message || "An unknown error occurred."), {
                        icon: "error",
                        buttons: {
                            confirm: {
                                className: "btn btn-danger",
                            },
                        },
                    });
                }
            });
            swal("Event has been deleted!", {
                icon: "success",
                buttons: {
                    confirm: {
                        className: "btn btn-success",
                    },
                },
            });
        } else {
            swal.close();
        }
    });
}