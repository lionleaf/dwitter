var onDweetChanged = function() {
  // eslint-disable-next-line newline-per-chained-call
  var charCount = $(this).parent().parent().parent().find('.character-count')[0];
  var submitButton = $(this).parent().parent().find('.remix-button')[0];

  charCount.textContent = this.value.length + '/140';
  if (this.value.length > 140) {
    $(charCount).addClass('too-long');
    $(submitButton).prop('disabled', true);
  } else {
    $(charCount).removeClass('too-long');
    $(submitButton).prop('disabled', false);
  }
};

$(document).ajaxComplete(function() {
  $('.code-input').each(onDweetChanged);
});

$(document).ready(function() {
  $('body').on('input', '.code-input', onDweetChanged);
  $('.code-input').each(onDweetChanged);

  function requestFullscreen(el) {
    (el.mozRequestFullScreen ||
     el.webkitRequestFullscreen ||
     el.requestFullscreen).call(el);
  }
  $('.dweet').each(function(i, el) {
    var link = $(el).find('.fullscreen-button');
    var iframe = $(el).find('iframe.dweetiframe');
    link.on('click', function(e) {
      e.preventDefault();
      requestFullscreen(iframe[0]);
    });

    var sharebutt = $(el).find('.share-button');
    var sharelink = $(el).find('.share-link');
    sharebutt.on('click', function(e) {
      e.preventDefault();
      sharelink.toggle();
      if (sharelink.is(':visible')) {
        sharelink.select();
      }
    });
    $(sharelink).focus(function() {
      $(this).on('click.a keyup.a', function() {
        $(this).off('click.a keyup.a').select();
      });
    });
  });

  moment.locale(navigator.userLanguage || navigator.language || 'en-US');
  $('.dweet-timestamp').each(function(_, element) {
    var postedDate = moment.utc($(element).find('time').attr('datetime'));
    $(element).text(postedDate.local().format('lll'));
  });

  $('.dweet-create-form-title').click(function() {
    $(this).hide();
    /* eslint-disable no-undef */
    var dweet = $('.submit-box').slideDown(Waypoint.refreshAll);
    registerOnKeyListener(dweet);
    var iframe = $(dweet).find('.dweetiframe')[0];
    registerWaypoint(iframe);
    /* eslint-enable no-undef */
    $(dweet).find('textarea').focus();
  });
});
