$('#like').click(function(){
    var videoid;
    videoid = $(this).attr("data-videoid");
    $.get('/activity/like/', {video_id: videoid}, function(like, dislike){
               $('#like_count').html(like[0]);
               $('#dislike_count').html(like[1]);
    });
});

$('#dislike').click(function(){
    var videoid;
    videoid = $(this).attr("data-videoid");
    $.get('/activity/dislike/', {video_id: videoid}, function(like, dislike){
               $('#like_count').html(like[0]);
               $('#dislike_count').html(like[1]);
    });
});


