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

  $('body').on('click', '[data-popover]', function(e) {
    var dweetCard = $(this).closest('.dweet');
    var $popover = $(dweetCard).find($(this).data('popover'));
    var shareLink = $popover.find('.share-link');
    e.preventDefault();

    if ($popover.is(':visible')) {
      $popover.hide();
    } else {
      $('.popover').hide();
      $popover.show();

      if ($(this).data('popover') === '.share-container') {
        shareLink.select();
      }
    }
  });

  $('body').on('click', '.record-button', function() {
    var recordButton = $(this)[0];
    var iframe = document.getElementById(recordButton.dataset.dweet_id);
    var span = recordButton.getElementsByTagName('span')[0];
    if (recordButton.classList.contains('recording')) {
      iframe.contentWindow.postMessage('stopGifRecord', '*');
      recordButton.classList.remove('recording');
      recordButton.classList.add('processing');
      span.innerHTML = 'processing';
    } else if (!recordButton.classList.contains('processing')) {
      iframe.contentWindow.postMessage({ msg: 'startGifRecord', dweetId: recordButton.dataset.dweet_id }, '*');
      recordButton.classList.add('recording');
      span.innerHTML = 'recording';
    }
  });

  $('body').on('click', function(e) {
    if (!$(e.target).is('[data-popover]') &&
        $(e.target).closest('.popover').length === 0) {
      $('.popover').hide();
    }
  });

  $('body').on('focus', '.share-link, .embed-src', function() {
    $(this).select();
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
