$(document).ready(function () {
    // $('#registerAlert').text('User Successfully Registered Kindly Login').show();

    $("#login_btn").click(function (event) {

        $.ajax({

            url: 'http://127.0.0.1:5000/login/api',
            type: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            contentType: 'application/JSON; charset= utf-8',
            data: JSON.stringify({

                email: $('#email').val(),
                password: $('#password').val(),
            }),
        }).done(function (data) {

            if (data.error) {

                $('#successAlert').hide();
                // $('#registerAlert').text('User Successfully Registered Kindly Login').hide();
                $('#errorAlert').text(data.error).show();
            }
            else {
                $('#successAlert').text(data.name).show();
                $('#errorAlert').hide();
                if (data.user == 'user'){
                window.location.href = 'User_Dashboard/userDashboard.html'
                }
                else {
                    window.location.href = 'Admin_Dashboard/adminDashboard.html'
                }
            }

        });

        event.preventDefault();

    });

});
