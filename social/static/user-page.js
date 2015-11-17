$(document).ready(function() {
    $('#profile').onmousedown(function() {
        $('#profile').hide('slow');
    })

    $('#send_friend_request').click(request_friend())
});

function request_friend() {
    $.ajax({
        url: 'friend/',
        type: 'POST',
        data: {
            requested_user: $('#intended_username').val()
        },

        success: function(json) {

        },

        error: function(xhr, message, err) {
            alert(message);
        }
    });
};
