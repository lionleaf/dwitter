window.onload = function() {

  var infinite = new Waypoint.Infinite({
    element: $('.dweet-feed')[0],
      items: '.dweet-wrapper',
      more: '.next-page',
      onAfterPageLoad: function(items) {
        var dwiframes = [];
        $.each(items, function(index, div){
          registerOnKeyListener(div);
          var iframe =  $(div).find(".dweetiframe")[0];
          registerWaypoint(iframe);

        });
      }
  });

  var dweetiframes = document.querySelectorAll(".dweetiframe");

  [].forEach.call(dweetiframes, function(iframe){
    registerWaypoint(iframe);
  });

  function registerWaypoint(iframe){
    console.log("Registering " + iframe.src);
    var inview = new Waypoint.Inview({
      element: iframe,
        entered: function(dir) {
          play(iframe)
        },
        exit: function(dir) {
          var fullscreenElement = (document.fullscreenElement ||
              document.webkitFullscreenElement ||
              document.mozFullScreenElement);
          if(fullscreenElement != iframe) {
            pause(iframe)
          }
        },
    });

  }

  var dweets = document.querySelectorAll(".dweet");
  [].forEach.call(dweets, function(dweet) {
    registerOnKeyListener(dweet);
  });


  // Update editor!
  var editor = document.querySelector('#editor');
  var editoriframe = document.querySelector('#preview-iframe');
  oldCode = editor.value;
  showCode(editoriframe, oldCode);
  editor.addEventListener('keyup', function() {
    if(editor.value == oldCode) {
      return;
    }
    editor.size = Math.max(editor.value.length, 1);
    showCode(editoriframe, editor.value);
    oldCode = editor.value;
  });

  function play(iframe){
    dweetwin =  iframe.contentWindow || iframe;
    dweetwin.postMessage("play","*");
    console.log("Send play to " + iframe.src);
  }
  function pause(iframe){
    dweetwin =  iframe.contentWindow || iframe;
    dweetwin.postMessage("pause","*");
    console.log("Send pause to " + iframe.src);
  }

  function showCode(iframe, code) {
    dweetwin =  iframe.contentWindow || iframe;
    dweetwin.postMessage("code "+code,'*');
  }

  function registerOnKeyListener(dweet){
    var iframe = $(dweet).find('.dweetiframe')[0];
    var editor = $(dweet).find('.code-input')[0];
    var changedDweetMenu = $(dweet).find('.dweet-changed');
    var oldCode = editor.value;
    var originalCode = oldCode;

    showCode(iframe, oldCode);
    editor.addEventListener('keyup', function() {
      if(editor.value == originalCode){
        changedDweetMenu.hide();
      }else{
        changedDweetMenu.show();
      }

      if(editor.value == oldCode) {
        return;
      }
      editor.size = Math.max(editor.value.length, 1);
      showCode(iframe, editor.value);
      oldCode = editor.value;
    });

  }
};
