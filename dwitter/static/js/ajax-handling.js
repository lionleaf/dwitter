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


var loadComments = function() {
  var $load_comments_button = $(this);

  console.log($load_comments_button);

   var dweet_id = $load_comments_button.data('dweet_id');

   var loadCommentsResponse = function(serverResponse_json, textStatus_ignored,
       jqXHR_ignored)  {
  console.log('Result!!' + serverResponse_json);
     var $comment_section = $load_comments_button.parents('.comments');
     $load_comments_button.parents('.comment').hide();
     for(var i in serverResponse_json){
       var comment = serverResponse_json[i];
       console.log(comment);
       console.log($comment_section)
       $comment_section[0].innerHTML += '<div class=comment><p><span class=comment-name>'+comment.author_username +':</span>'+comment.text+'</p></div>';
     }
     
   }

   var config = {
     url: '/get-comments/' + dweet_id,
     dataType: 'json',
      success: loadCommentsResponse,
   };
   $.ajax(config);
}


$(document).ready(function()  {
  $('body').on('click','.like-button', processLike);
  $('body').on('click','.load-comments-link', loadComments);
});
