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
        var commentText = $('#' + postId + '-comment-input').val();
        var url = location.pathname + postId + "/comment/";
        console.log("Attempt to get " + url);
        $.get(url, {post_id: postId, comment_text: commentText}, function(data) {
           $('#' + postId + '-comments').html(data);
        });
    });
});