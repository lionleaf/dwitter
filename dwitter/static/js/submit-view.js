$('window').ready(function() {
  // Unfocus when we scroll away
  var wayp = new Waypoint.Inview({
    element: $('#editor'),
    exited: function() {
      $('#editor').blur();
    },
  });

  $('#editor').focusin(function() {
    $('#submit-preview').show(500, function() { wayp.element.context.refresh(); });
    $('#submit-help').show(500);
    $('#click-the-code').hide();
    play($('#preview-iframe')[0]);
  });

  $('#editor').focusout(function() {
    $('#submit-preview').hide(500);
    $('#submit-help').hide(500);
    $('#click-the-code').show();
    pause($('#preview-iframe')[0]);
  });

  function play(iframe) {
    var dweetwin = iframe.contentWindow || iframe;
    dweetwin.postMessage('play', '*');
  }

  function pause(iframe) {
    var dweetwin = iframe.contentWindow || iframe;
    dweetwin.postMessage('pause', '*');
  }
});
