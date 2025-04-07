function deleteItem(id) {
    if (confirm("Are you confirm to delete?")) {
        $.ajax({
            url: "/?id=" + id,
            type: "DELETE",
            success: function (json) {
                location.reload();
            },
            error: function (error) {
                alert(JSON.stringify(error.message));
            }
        });
    }
}