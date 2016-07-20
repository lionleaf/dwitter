var onDweetChanged = function() {
  var charCount = $(this).parent().find(".character-count")[0];

  charCount.textContent = this.value.length + '/140';
};


$(document).ready(function()  {
  $('body').on('input','.code-input', onDweetChanged);


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
