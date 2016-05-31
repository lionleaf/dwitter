$('window').ready(function() {
  //Unfocus when we scroll away
  var wayp = new Waypoint.Inview({
    element: $('#editor'),
      exited: function(dir) {
        $('#editor').blur(); 
      },
  });

  console.log(wayp);

  $('#editor').focusin(function(){
    $('#submit-preview').show(500, function(){wayp.element.context.refresh()});
    $('#submit-help').show(500);
    $('#click-the-code').hide();
    play($('#preview-iframe')[0]);
  });

  $('#editor').focusout(function(){
    $('#submit-preview').hide(500);
    $('#submit-help').hide(500);
    $('#click-the-code').show();
    pause($('#preview-iframe')[0]);
  });


  function play(iframe){
    console.log(iframe);
    dweetwin =  iframe.contentWindow || iframe;
    dweetwin.postMessage("play","*");
    console.log("Send play to " + iframe.src);
  }

  function pause(iframe){
    console.log(iframe);
    dweetwin =  iframe.contentWindow || iframe;
    dweetwin.postMessage("pause", "*");
    console.log("Send pause to " + iframe.src);
  }
});
