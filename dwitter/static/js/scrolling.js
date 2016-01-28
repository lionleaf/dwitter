document.addEventListener('DOMContentLoaded', function() {
  var infinite = new Waypoint.Infinite({
    element: $('.dweet-feed')[0],
      items: '.dweet',
      more: '.next-page',
      onAfterPageLoad: function(items) {
        var dwiframes = [];
        $.each(items, function(index, div){
          console.log("each " + div);
          var iframe =  $(div).find(".dweetiframe")[0];
          console.log("Registering " + iframe.src);
          var inview = new Waypoint.Inview({
            element: iframe,
              entered: function(dir) {
                play(iframe);
              },
              exit: function(dir) {
                      pause(iframe);
                    },
          });
        });
      }
  });
  console.log("infite element: " + infinite.element);

  var dweetiframes = document.querySelectorAll(".dweetiframe");

  [].forEach.call(dweetiframes, function(iframe){
    var inview = new Waypoint.Inview({
      element: iframe,
        entered: function(dir) {
          play(iframe)
        },
        exit: function(dir) {
                pause(iframe)
              },
    });
  });


  var dweets = document.querySelectorAll(".dweet");
  [].forEach.call(dweets, function(dweet) {
    var iframe = $(dweet).find('.dweetiframe')[0];
    var editor = $(dweet).find('.code-input')[0];
    oldCode = editor.value;

    showCode(iframe, oldCode);
    editor.addEventListener('keyup', function() {
      if(editor.value == oldCode) {
        return;
      }
      editor.size = Math.max(editor.value.length, 1);
      showCode(iframe, editor.value);
      oldCode = editor.value;
    });
    
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
    dweetwin.postMessage("play",iframe.src);
    console.log("Send play to " + iframe.src);
  }
  function pause(iframe){
    dweetwin =  iframe.contentWindow || iframe;
    dweetwin.postMessage("pause",iframe.src);
    console.log("Send pause to " + iframe.src);
  }

  function showCode(iframe, code) {
    dweetwin =  iframe.contentWindow || iframe;
    dweetwin.postMessage("code "+code,iframe.src);
  }
}, false);
