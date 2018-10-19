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

function getCommentHTML(comment) {
  return '<li class=comment><a class=comment-name href="/u/' + comment.author + '">' +
    comment.author + ':</a> ' +
    '<span class="comment-message">' + comment.urlized_text +
    '</span></li>';
}

function loadComments() {
  var $loadCommentsButton = $(this);

  var dweetId = $loadCommentsButton.data('dweet_id');
  var offset = $loadCommentsButton.data('hidden_comments_offset');
  var limit = $loadCommentsButton.data('hidden_comments_number');

  var loadCommentsResponse = function(response) {
    var commentSection = $loadCommentsButton.parents('.comments')[0];
    var newCommentList = response.results.map(getCommentHTML).join('');

    $loadCommentsButton.parents('.comment').hide();

    $(commentSection)
      .html(newCommentList + commentSection.innerHTML)
      .promise()
      .done(Waypoint.refreshAll);
  };

  var config = {
    url: '/api/comments/?offset=' + offset +
         '&limit=' + limit +
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
