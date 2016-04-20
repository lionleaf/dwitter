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


$(document).ready(function()  {
  $('body').on('click','.like-button', processLike);
});
