//handle the selenium Bot
$(document).ready(function () {
    // Handle form submission
    $("#scraping-form").submit(function (event) {
        event.preventDefault();
        scheduleBot();
    });

    // Function to schedule the Selenium bot scraping
    function scheduleBot() {
        var numDays = parseInt($("#days-input").val());

        $('#successAlert2').hide();
        $('#errorAlert2').hide();
        $('#waitAlert2').text(`Selenium Bot is successfully set to scrape after ${numDays} days`).show();

        $.ajax({
            url: "http://127.0.0.1:5000/schedulebot/api",
            type: "POST",
            data: { numDays: numDays },
            success: function (response) {
                console.log(response);
                $('#waitAlert2').hide();
                $('#successAlert2').text('Selenium Bot Scraping Scheduled Successfully').show();
            },
            error: function (xhr, status, error) {
                console.log("Error scheduling the Selenium bot scraping:", error);
                $('#errorAlert2').text('Error scheduling the Selenium bot scraping').show();
                $('#waitAlert2').hide();
            }
        });
    }
});