

var processLike = function()  {
   var $like_button = $(this);
   var dweet_id = $like_button.data('dweet_id');
   var processServerResponse = function(serverResponse_json, textStatus_ignored,
       jqXHR_ignored)  {
     if(serverResponse_json.not_authenticated){
       window.location = "/accounts/login/";
     }else{
       $like_button.find('.score-text').html(serverResponse_json.likes);
       if(serverResponse_json.liked){
         $like_button.addClass('liked');
       }else{
         $like_button.removeClass('liked');
       }
     }
   }

   var config = {
     url: '/like/' + dweet_id,
     dataType: 'json',
      success: processServerResponse,
   };
   $.ajax(config);
};

var getCommentHTML = function(comment) {
       return '<div class=comment><p><span class=comment-name>'+comment.author+':</span>'+comment.text+'</p></div>';
}
var loadComments = function() {
  var step = 1000;
  var current_offset = $(this).data('offset') ;

  var $load_comments_button = $(this);

   var dweet_id = $load_comments_button.data('dweet_id');
   var next = $load_comments_button.data('next');

   var loadCommentsResponse = function(serverResponse_json, textStatus_ignored,
       jqXHR_ignored)  {

     var $comment_section = $load_comments_button.parents('.comments');

     if(serverResponse_json.next){
       alert("Woops, there are more comments, but they are unloadable as of now. Please bug lionleaf to fix");
     }else{
       $load_comments_button.parents('.comment').hide();
     }
     var new_comment_list = '';
     for(var i in serverResponse_json.results.reverse()){
       var comment = serverResponse_json.results[i];
       console.log(comment);
       console.log($comment_section);
       new_comment_list  += getCommentHTML(comment);
     }
     $comment_section[0].innerHTML = new_comment_list + $comment_section[0].innerHTML;
     
   }

   var config = {
     url: 'api/comments/?offset='+current_offset+'&limit='+step+'&format=json&reply_to='+dweet_id,
     dataType: 'json',
      success: loadCommentsResponse,
   };
   $.ajax(config);
}

var postComment = function() {
  var $post_comment_button = $(this);
  var dweet_id = $post_comment_button.data('dweet_id');
  var csrf = $post_comment_button.data('csrf');
  console.log("csrf: " + csrf);
  var $comment_text = $post_comment_button.siblings('.comment-input');
  var $comment_section = $post_comment_button.closest('.comment-section').children('.comments');

  var postCommentResponse = function(serverResponse_json, textStatus_ignored,
      jqXHR_ignored)  {

    $comment_text[0].value = '';
    $comment_section[0].innerHTML =  $comment_section[0].innerHTML + getCommentHTML(serverResponse_json);
  }

  var comment = {
    reply_to: dweet_id,
    text: $comment_text[0].value,
    csrfmiddlewaretoken: csrf,
  }

  var config = {
    url: 'api/comments/',
    method: 'POST',
    success: postCommentResponse,
    error: postCommentResponse,
    data: comment,
  };
  console.log(config);
  $.ajax(config);
}


$(document).ready(function()  {
  $('body').on('click','.like-button', processLike);
  $('body').on('click','.load-comments-link', loadComments);
  $('body').on('click','.comment-submit', postComment);
});
