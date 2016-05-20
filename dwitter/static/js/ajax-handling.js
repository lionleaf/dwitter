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
       new_comment_list  += '<div class=comment><p><span class=comment-name>'+comment.author+':</span>'+comment.text+'</p></div>';
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


$(document).ready(function()  {
  $('body').on('click','.like-button', processLike);
  $('body').on('click','.load-comments-link', loadComments);
});
