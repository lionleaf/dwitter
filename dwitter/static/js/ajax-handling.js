function processLike(e) {
  var $likeForm = $(this);
  var dweetId = $likeForm.data('dweet_id');
  var $likeButton = $likeForm.find('.like-button');
  var processServerResponse = function(response) {
    if (response.not_authenticated) {
      window.location = '/accounts/login/';
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

function getCommentHTML(comment) {
  return '<li class=comment><a class=comment-name href="/u/' + comment.author + '">' +
    comment.author + ':</a> ' +
    '<span class="comment-message">' + comment.urlized_text +
    '</span></li>';
}

function loadComments() {
  var step = 1000;
  var currentOffset = $(this).data('offset');

  var $loadCommentsButton = $(this);

  var dweetId = $loadCommentsButton.data('dweet_id');
  // If there is a sticky comment on the top of the comments
  var stickyTop = $loadCommentsButton.data('sticky_top');

  var loadCommentsResponse = function(response) {
    var commentSection = $loadCommentsButton.parents('.comments')[0];
    var newCommentList = response.results.reverse().map(function(comment, index) {
      return stickyTop && index === 0 ? '' : getCommentHTML(comment);
    }).join('');

    if (!response.next) {
      $loadCommentsButton.parents('.comment').hide();
    }

    $(commentSection)
      .html(newCommentList + commentSection.innerHTML)
      .promise()
      .done(Waypoint.refreshAll);
  };

  var config = {
    url: '/api/comments/?offset=' + currentOffset +
         '&limit=' + step +
         '&format=json&reply_to=' + dweetId,
    dataType: 'json',
    success: loadCommentsResponse,
  };

  $.ajax(config);
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
  $('body').on('click', '.load-comments-link', loadComments);
  $('body').on('submit', '.new-comment', postComment);
});
