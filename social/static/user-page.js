$(document).ready(function() {
    $('.commends').click(function() {
        var postId = $(this).attr("data-postid");
        $.get('/commend/', {post_id: postId}, function(data) {
            $('#' + postId +'-commendations').html(data);
            $('#' + postId +'-commends').hide();
        });
    })
});