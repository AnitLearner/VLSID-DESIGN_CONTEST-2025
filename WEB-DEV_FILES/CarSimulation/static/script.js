
$(document).ready(function () {
    $(".knob").knob();

    $("#submit").click(function () {
        const data = {
            speed: $("#speed").val(),
            distance: $("#distance").val(),
            degree: $("#degree").val(),
            status: $("#status").val(),
        };

        $.ajax({
            url: "/save",
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify(data),
            success: function (response) {
                alert(response.message);
            },
            error: function () {
                alert("Error saving data to Excel.");
            },
        });
    });
     // Stop Transmission functionality
     $("#stop").click(function () {
        $.ajax({
            url: "/stop",
            method: "POST",
            success: function (response) {
                alert(response.message);
            },
            error: function () {
                alert("Error stopping transmission.");
            },
        });
    });
});
