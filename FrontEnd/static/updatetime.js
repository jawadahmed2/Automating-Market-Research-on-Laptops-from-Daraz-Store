$(document).ready(function () {
    // Function to update the date in the dropdown button
    function updateDropdownDate() {
        // Get the dropdown button element
        var dropdownButton = document.getElementById('dropdownMenuDate2');

        // Get the current date
        var currentDate = new Date();

        // Format the date as "DD Month YYYY" (e.g., "06 July 2023")
        var formattedDate = currentDate.toLocaleDateString('en-US', {
            day: '2-digit',
            month: 'long',
            year: 'numeric'
        });

        // Update the date in the dropdown button
        dropdownButton.innerHTML = '<i class="mdi mdi-calendar"></i> Today (' + formattedDate + ')';
    }

    // Call the function to update the date on page reload
    updateDropdownDate();

});
