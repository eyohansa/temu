$(document).ready(function() {
    autosize(document.querySelectorAll('textarea'));

    $('.commends').click(function() {
        var postId = $(this).attr("data-postid");
        $.get('/commend/', {post_id: postId}, function(data) {
            $('span#' + postId +'-commendation-count').html(data);
            $('#' + postId +'-commends').hide();
        });
    });

    $('.comment-submit').click(function() {
        var postId = $(this).attr("data-postid");
        var commentText = $('#' + postId + '-comment-input').val();
        var url = "/comment/";

        $.ajax(url, {
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'));
                }
            },
            data: {
                post_id: postId,
                comment_text: commentText
            },
            type: 'POST',
            success: function(data) {
                console.table(data);
                $('#' + postId + '-comments').html(data);
            },
            error: function(data) {
                console.log(data)
            }
        });
    });

    $('.add-friend-button').click(function() {
        var username = $(this).attr("data-username");
        var url = $(this).attr("data-href");

        $.ajax(url, {
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'));
                }
            },
            data: {
                user_id: userId
            },
            type: 'POST',
            success: function(data) {
                $(this).hide();
            },
            error: function(data) {
                console.log(data);
            }
        });
    });

    $('.block-button').click(function() {
        var username = $(this).attr('data-username');
        var url = $(this).attr('data-url');

        $.ajax(url, {
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'));
                }
            },
            data: {
                target_username: username
            },
            type: 'POST',
            success: function(data) {
                if(data['result'] == 'success') {
                    console.log(username + " has been blocked.");
                }
            },
            error: function(data) {
                console.log(data);
            }
        })
    });
});

function csrfSafeMethod(method) {
    return (/^(GET|HED|OPTIONS|TRACE)$/.test(method));
}