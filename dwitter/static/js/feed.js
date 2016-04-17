var onDweetChanged = function() {
  var charCount = $(this).parent().find(".character-count")[0];

  charCount.textContent = this.value.length + '/140';
};


$(document).ready(function()  {
  $('body').on('input','.code-input', onDweetChanged);
});
