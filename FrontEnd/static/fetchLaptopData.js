$(document).ready(function () {
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


    // Call fetchLaptopData function on page load
    fetchLaptopData();

});
