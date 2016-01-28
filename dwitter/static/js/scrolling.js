window.onload = function() {
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

  inviews = {};

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
};
