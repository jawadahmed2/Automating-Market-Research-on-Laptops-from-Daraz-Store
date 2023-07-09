$(document).ready(function () {

    // Function to fetch the total number of laptop data
    function fetchTotalLaptopData() {
        $.ajax({
            url: "http://127.0.0.1:5000/get-total-laptop-data/api",
            type: "GET",
            dataType: "json",
            success: function (data) {
                var totalLaptopData = data.total;
                $("#total_laptop_data").text(totalLaptopData);
            },
            error: function (xhr, status, error) {
                console.log("Error retrieving total laptop data:", error);
            }
        });
    }

    // Call fetchTotalLaptopData function on page load
    fetchTotalLaptopData();
});
