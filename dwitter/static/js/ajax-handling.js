function processLike(e) {
  var $likeForm = $(this);
  var dweetId = $likeForm.data('dweet_id');
  var $likeButton = $likeForm.find('.like-button');
  var processServerResponse = function(response) {
    if (response.not_authenticated) {
      $likeForm.parent().parent().find('.error-display')[0]
        .innerText = 'You have to be logged in to vote';
    } else {
      $likeButton.find('.score-text').html(response.likes);
      if (response.liked) {
        $likeButton.addClass('liked');
      } else {
        $likeButton.removeClass('liked');
      }
    }
  };

  var config = {
    url: '/d/' + dweetId + '/like',
    dataType: 'json',
    method: 'POST',
    headers: {
      'X-CSRFToken': $likeForm.data('csrf'),
    },
    success: processServerResponse,
  };

  e.preventDefault();
  $.ajax(config);
}

function processReport(e) {
  var $reportForm;
  var dweetId;
  var commentId;
  var processServerResponse;
  var config;
  e.preventDefault();
  if (!confirm('Are you sure you want to report this to a moderator?')) {  // eslint-disable-line
    return;
  }
  $reportForm = $(this);
  dweetId = $reportForm.data('dweet_id');
  commentId = $reportForm.data('comment_id');
  processServerResponse = function(response) {
    if (response.not_authenticated) {
      alert('You have to be logged in to report.'); // eslint-disable-line
    } else {
      alert('A moderator has been notified.'); // eslint-disable-line
    }
  };

  config = {
    dataType: 'json',
    method: 'POST',
    headers: {
      'X-CSRFToken': $reportForm.data('csrf'),
    },
    success: processServerResponse,
  };

  if (dweetId) {
    config.url = '/d/' + dweetId + '/report';
  } else {
    config.url = '/c/' + commentId + '/report';
  }

  $.ajax(config);
}

function getCommentHTML(comment) {
  return '<li class=comment><a class=comment-name href="/u/' + comment.author + '">' +
    comment.author + ':</a> ' +
    '<form class="report" data-comment_id="' + comment.id + '">' +
      '<button type="submit" class="report-button">' +
        '<div class="wrapper">' +
          '<span class="far fa-flag"></span>' +
          '<span class="text">report</span>' +
        '</div>' +
      '</button>' +
    '</form>' +
    '<span class="comment-message">' + comment.urlized_text +
    '</span>' +
    '</li>';
}

function postComment(e) {
  var $postForm = $(this);
  var dweetId = $postForm.data('dweet_id');
  var csrf = $postForm.data('csrf');
  var $commentText = $postForm.find('.comment-input');
  var $commentSection = $postForm.closest('.comment-section').children('.comments');

  var postCommentSuccess = function(response) {
    $commentText[0].value = '';
    $commentSection[0].innerHTML += getCommentHTML(response);
  };

  var postCommentError = function() {
    // Do nothing at the moment. TODO: Clearer error message displayed to the user?
  };

  var comment = {
    reply_to: dweetId,
    text: $commentText[0].value,
    csrfmiddlewaretoken: csrf,
  };

  var config = {
    url: '/api/comments/',
    method: 'POST',
    success: postCommentSuccess,
    error: postCommentError,
    data: comment,
  };

  e.preventDefault();
  $.ajax(config);
}

$(document).ready(function() {
  $('body').on('submit', 'form.like', processLike);
  $('body').on('submit', 'form.report', processReport);
  $('body').on('submit', '.new-comment', postComment);
});
