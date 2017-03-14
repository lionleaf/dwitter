window.onload = function() {
  var dweets = document.querySelectorAll('.dweet');
  var dweetiframes = document.querySelectorAll('.dweetiframe');
  var editor = document.querySelector('#editor');
  var editoriframe = document.querySelector('#preview-iframe');
  var oldCode = editor && editor.value;

  [].forEach.call(dweetiframes, function(iframe) {
    registerWaypoint(iframe);
  });

  [].forEach.call(dweets, function(dweet) {
    registerOnKeyListener(dweet);
    registerStatsClickListeners(dweet);
  });

  if (editor && editoriframe) {
    // Update editor!
    showCode(editoriframe, oldCode);
    editor.addEventListener('keyup', function() {
      if (editor.value === oldCode) {
        return;
      }
      editor.size = Math.max(editor.value.length, 1);
      showCode(editoriframe, editor.value);
      oldCode = editor.value;
    });
  }

  // eslint-disable-next-line no-new
  new Waypoint.Infinite({
    element: $('.dweet-feed')[0],
    items: '.dweet-wrapper, .loading, .end-of-feed',
    more: '.next-page',
    onAfterPageLoad: function(items) {
      $('.loading:not(:last-of-type)').hide();

      function requestFullscreen(el) {
        (el.mozRequestFullScreen ||
           el.webkitRequestFullscreen ||
           el.requestFullscreen).call(el);
      }

      $.each(items, function(index, div) {
        var iframe = $(div).find('.dweetiframe')[0];
        var link = $(div).find('.fullscreen-button');
        var sharebutt = $(div).find('.share-button');
        var sharelink = $(div).find('.share-link');

        registerOnKeyListener(div);
        registerStatsClickListeners(div);
        registerWaypoint(iframe);

        // Register full-screen button
        link.on('click', function(e) {
          e.preventDefault();
          requestFullscreen(iframe);
        });

        sharebutt.on('click', function(e) {
          e.preventDefault();
          sharelink.toggle();

          if (sharelink.is(':visible')) {
            sharelink.select();
          }
        });

        $(sharelink).focus(function() {
          var timestamp = $(div).find('time');
          var postedDate = moment.utc(timestamp.attr('datetime'));

          moment.locale(navigator.userLanguage || navigator.language || 'en-US');
          timestamp.text(postedDate.local().format('lll'));

          $(this).on('click.a keyup.a', function() {
            $(this).off('click.a keyup.a').select();
          });
        });
      });
    },
  });
};

function registerWaypoint(iframe) {
  // eslint-disable-next-line no-new
  new Waypoint.Inview({
    element: iframe,
    entered: function() {
      play(iframe);
    },
    exit: function() {
      var fullscreenElement = (document.fullscreenElement ||
            document.webkitFullscreenElement ||
            document.mozFullScreenElement);
      if (fullscreenElement !== iframe) {
        pause(iframe);
      }
    },
  });
}

function play(iframe) {
  var dweetwin = iframe.contentWindow || iframe;
  dweetwin.postMessage('play', '*');
}

function pause(iframe) {
  var dweetwin = iframe.contentWindow || iframe;
  dweetwin.postMessage('pause', '*');
}

function showCode(iframe, code) {
  var dweetwin = iframe.contentWindow || iframe;
  dweetwin.postMessage('code ' + code, '*');
}

function showStats(dweet, iframe) {
  (iframe.contentWindow || iframe).postMessage('showStats', '*');
  $(dweet).find('.show-stats').hide();
  $(dweet).find('.hide-stats').show();
}

function hideStats(dweet, iframe) {
  (iframe.contentWindow || iframe).postMessage('hideStats', '*');
  $(dweet).find('.show-stats').show();
  $(dweet).find('.hide-stats').hide();
}

function registerOnKeyListener(dweet) {
  var iframe = $(dweet).find('.dweetiframe')[0];
  var editor = $(dweet).find('.code-input')[0];
  var changedDweetMenu = $(dweet).find('.dweet-changed');
  var oldCode = editor.value;
  var originalCode = oldCode;

  showCode(iframe, oldCode);
  editor.addEventListener('keyup', function() {
    showStats(dweet, iframe);

    if (editor.value === originalCode) {
      changedDweetMenu.hide();
    } else {
      changedDweetMenu.show();
    }

    if (editor.value === oldCode) {
      return;
    }
    editor.size = Math.max(editor.value.length, 1);
    showCode(iframe, editor.value);
    oldCode = editor.value;
  });
}

function registerStatsClickListeners(element) {
  var iframe = $(element).find('.dweetiframe')[0];
  $(element).find('.show-stats').click(function(e) {
    e.preventDefault();
    showStats(element, iframe);
  });
  $(element).find('.hide-stats').click(function(e) {
    e.preventDefault();
    hideStats(element, iframe);
  });
}
