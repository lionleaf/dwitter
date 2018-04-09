function onDweetChanged() {
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
}

$(document).ajaxComplete(function() {
  $('.code-input').each(onDweetChanged);
});

$(document).ready(function() {
  function requestFullscreen(el) {
    (el.mozRequestFullScreen ||
     el.webkitRequestFullscreen ||
     el.requestFullscreen).call(el);
  }

  $('body').on('input', '.code-input', onDweetChanged);
  $('.code-input').each(onDweetChanged);

  $('body').on('click', '.fullscreen-button', function(e) {
    var dweetCard = $(this).closest('.dweet');
    var iframe = $(dweetCard).find('iframe.dweetiframe');
    e.preventDefault();
    requestFullscreen(iframe[0]);
  });

  $('body').on('click', '.share-button', function(e) {
    var dweetCard = $(this).closest('.dweet');
    var shareContainer = $(dweetCard).find('.share-container');
    var shareLink = $(dweetCard).find('.share-link');
    e.preventDefault();
    shareContainer.toggle();
    if (shareLink.is(':visible')) {
      shareLink.select();
    }
  });

  $('body').on('focus', '.share-link', function() {
    $(this).on('click.a keyup.a', function() {
      $(this).off('click.a keyup.a').select();
    });
  });

  moment.locale(navigator.userLanguage || navigator.language || 'en-US');
  $('.dweet-timestamp').each(function(_, element) {
    var postedDate = moment.utc($(element).find('time').attr('datetime'));
    $(element).text(postedDate.local().format('lll'));
  });

  $('.dweet-create-form-title').click(function() {
    var dweet = $('.submit-box').slideDown(Waypoint.refreshAll);
    var iframe = $(dweet).find('.dweetiframe')[0];

    /* eslint-disable no-undef */
    registerOnKeyListener(dweet);
    registerWaypoint(iframe);
    /* eslint-enable no-undef */

    $(dweet).find('textarea').focus();
  });
});
