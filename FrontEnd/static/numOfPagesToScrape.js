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

     // Function to fetch the laptop data and populate the table
     function fetchLaptopData() {
        $.ajax({
            url: "http://127.0.0.1:5000/home/api",
            type: "GET",
            dataType: "json",
            success: function (data) {
                // Process the JSON data and populate the table
                populateTable(data);
            },
            error: function (xhr, status, error) {
                console.log("Error retrieving laptop data:", error);
                $('#errorAlert1').text('Error retrieving laptop data').show();
            }
        });
    }

    // Function to populate the table with laptop data
    function populateTable(laptopData) {
        var tableBody = $("#scraped_table tbody");
        tableBody.empty();

        // Iterate over the laptop data and populate the table rows
        for (var i = 0; i < laptopData.length; i++) {
            var laptop = laptopData[i];

            // Extract the truncated laptop name
            var truncatedName = laptop.laptopName.split(/,|-|\|/)[0].trim();

            var rowHtml = "<tr>" +
                "<td>" + (i + 1) + "</td>" +
                "<td>" + truncatedName + "</td>" +
                "<td>" + laptop.laptopPrice + "</td>" +
                "<td>" + laptop.laptopRating + "</td>" +
                "<td><a href='" + laptop.laptopLink + "' target='_blank'>View</a></td>" +
                "</tr>";
            tableBody.append(rowHtml);
        }
    }


    // Button click event handler
    $("#start-scraping-btn").click(function (event) {
        event.preventDefault();
        startScraping();
    });

});