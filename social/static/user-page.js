$(document).ready(function() {
    $('.commends').click(function() {
        var postId = $(this).attr("data-postid");
        $.get('/commend/', {post_id: postId}, function(data) {
            $('span#' + postId +'-commendation-count').html(data);
            $('#' + postId +'-commends').hide();
        });
    });

    $('.comment-submit').click(function() {
        var postId = $(this).attr("data-postid");
        var csrfToken = $(this).attr("data-csrftoken");
        var commentText = $('#' + postId + '-comment-input').val();
        var url = "/comment/";

        $.ajax(url, {
            data: {
                csrfmiddlewaretoken: csrfToken,
                post_id: postId,
                comment_text: commentText
            },
            type: 'POST',
            success: function(data) {
                $('#'+postId+'comments').html(data);
            },
            error: function(data) {
                console.log(data)
            }
        });
    });

    $('#add-friend-button').click(function() {
        var userId = $(this).attr("data-userid");
        var csrfToken = $(this).attr("data-csrftoken");
        var url = "/friend/add/";

        $.ajax(url, {
            data: {
                csrfmiddlewaretoken: csrfToken,
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
});