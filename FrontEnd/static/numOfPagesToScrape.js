$(document).ready(function () {
    // Function to start the scraping process
    function startScraping() {
        var numPages = parseInt($('#pages-input').val());
        if (isNaN(numPages) || numPages < 1) {
            alert('Invalid number of pages. Please enter a positive integer.');
            return;
        }

        $('#scraped_table tbody').empty();
        $('#successAlert1').hide();
        $('#errorAlert1').hide();
        $('#waitAlert1').text('Wait Product Is Scraping').show();

        $.ajax({
            url: "http://127.0.0.1:5000/startsraping/api",
            type: "POST",
            data: { numPages: numPages },
            success: function (response) {
                console.log(response);
                // After starting the scraping, fetch and display the laptop data
                fetchLaptopData();
                $('#waitAlert1').text('Wait Product Is Scraping').hide();
                $('#successAlert1').text('Laptop Data Scraped Successfully').show();
            },
            error: function (xhr, status, error) {
                console.log("Error starting the scraping process:", error);
                $('#errorAlert1').text('Error starting the scraping process').show();
                $('#waitAlert1').text('Wait Product Is Scraping').hide();
                $('#successAlert1').text('Laptop Data Scraped Successfully').hide();
            }
        });
    }
    // Button click event handler
    $("#start-scraping-btn").click(function (event) {
        event.preventDefault();
        startScraping();
    });

});