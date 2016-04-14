var processLike = function()  {
 
   var $button_just_clicked_on = $(this);
 
   var dweet_id = $button_just_clicked_on.data('dweet_id');
 
   var processServerResponse = function(sersverResponse_data, textStatus_ignored,
                            jqXHR_ignored)  {
      //alert("sf sersverResponse_data='" + sersverResponse_data + "', textStatus_ignored='" + textStatus_ignored + "', jqXHR_ignored='" + jqXHR_ignored + "', dweet_id='" + dweet_id + "'");
      $('#like-button-' + dweet_id).html(sersverResponse_data);
   }
 
   var config = {
      url: '/like/' + dweet_id,
      dataType: 'html',
      success: processServerResponse
      //Should also have a "fail" call as well.
   };
   $.ajax(config);
};


$(document).ready(function()  {
  $('.like-button-div').click(processLike);
});
