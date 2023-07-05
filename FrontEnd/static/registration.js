$(document).ready(function () {

    $("#register_btn").click(function (event) {


        $.ajax({

            url: 'http://127.0.0.1:5000/registration/api',
            type: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            contentType: 'application/JSON; charset= utf-8',
            data: JSON.stringify({
                fname: $('#fname').val(),
                lname: $('#lname').val(),
                username: $('#username').val(),
                email: $('#email').val(),
                password: $('#password').val(),
            }),

        }).done(function (data) {

                if (data.error) {
                    $('#errorAlert').text(data.error).show();
                    $('#successAlert').hide();
                }
                else {
                    $('#successAlert').text(data.name).show();
                    $('#errorAlert').hide();
                    window.location.href = 'login.html'

                }

            });

        event.preventDefault();

    });

});
