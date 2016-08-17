var onDweetChanged = function() {
  var charCount = $(this).parent().find(".character-count")[0];
  var submitButton = $(this).parent().parent().find(".dweet-button")[0];

  charCount.textContent = this.value.length + '/140';
  if(this.value.length > 140){
    $(charCount).addClass('too-long');
    $(submitButton).prop('disabled', true);
  }else{
    $(charCount).removeClass('too-long');
    $(submitButton).prop('disabled', false);
  }
};

$(document).ajaxComplete(function() {
  $('.code-input').each(onDweetChanged);
});

$(document).ready(function()  {
  $('body').on('input','.code-input', onDweetChanged);
  $('.code-input').each(onDweetChanged);


  function requestFullscreen(el) {
    (el.mozRequestFullScreen ||
     el.webkitRequestFullscreen ||
     el.requestFullscreen).call(el);
  }
  $('.dweet').each(function(i, el) {
    var link = $(el).find('.arktis-link');
    var iframe = $(el).find('iframe.dweetiframe');
    link.on('click', function(e) {
      e.preventDefault();
      requestFullscreen(iframe[0]);
    });
  });
});
