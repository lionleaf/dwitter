var processLike = function(e) {
  e.preventDefault();
  var $likeForm = $(this);
  var dweet_id = $likeForm.data('dweet_id');
  var $like_button = $likeForm.find('.like-button');
  var processServerResponse = function(serverResponse_json, textStatus_ignored,
       jqXHR_ignored) {
    if (serverResponse_json.not_authenticated) {
      window.location = '/accounts/login/';
    } else {
      $like_button.find('.score-text').html(serverResponse_json.likes);
      if (serverResponse_json.liked) {
        $like_button.addClass('liked');
      } else {
        $like_button.removeClass('liked');
      }
    }
  };

  var config = {
    url: '/d/' + dweet_id + '/like',
    dataType: 'json',
    method: 'POST',
    headers: {
      'X-CSRFToken': $likeForm.data('csrf'),
    },
    success: processServerResponse,
  };
  $.ajax(config);
};

var getCommentHTML = function(comment) {
  return '<li class=comment><a class=comment-name href="/u/' + comment.author + '">' +
    comment.author + ':</a> ' +
    '<span class="comment-message">' + comment.urlized_text +
    '</span></li>';
};

var loadComments = function() {
  var step = 1000;
  var current_offset = $(this).data('offset');

  var $load_comments_button = $(this);

  var dweet_id = $load_comments_button.data('dweet_id');
  var next = $load_comments_button.data('next');
   // If there is a sticky comment on the top of the comments
  var sticky_top = $load_comments_button.data('sticky_top');

  var loadCommentsResponse = function(serverResponse_json, textStatus_ignored,
       jqXHR_ignored) {
    var comment_section = $load_comments_button.parents('.comments')[0];

    if (serverResponse_json.next) {
      alert('Woops, there are more comments, but they are unloadable as of now. Please bug lionleaf to fix');
    } else {
      $load_comments_button.parents('.comment').hide();
    }
    var new_comment_list = '';
    for (var i in serverResponse_json.results.reverse()) {
      var comment = serverResponse_json.results[i];
      if (sticky_top && i == 0) {
        continue; // Hack that works for now to avoid reloading the first comment if it was sticky
      }
      new_comment_list += getCommentHTML(comment);
    }
    $(comment_section)
      .html(new_comment_list + comment_section.innerHTML)
      .promise()
      .done(Waypoint.refreshAll);
  };

  var config = {
    url: '/api/comments/?offset=' + current_offset + '&limit=' + step + '&format=json&reply_to=' + dweet_id,
    dataType: 'json',
    success: loadCommentsResponse,
  };
  $.ajax(config);
};

var postComment = function(e) {
  e.preventDefault();
  var $postForm = $(this);
  var dweet_id = $postForm.data('dweet_id');
  var csrf = $postForm.data('csrf');
  var $comment_text = $postForm.find('.comment-input');
  var $comment_section = $postForm.closest('.comment-section').children('.comments');

  var postCommentSuccess = function(serverResponse_json, textStatus_ignored,
      jqXHR_ignored) {
    $comment_text[0].value = '';
    $comment_section[0].innerHTML = $comment_section[0].innerHTML + getCommentHTML(serverResponse_json);
  };

  var postCommentError = function(serverResponse_json, textStatus_ignored,
      jqXHR_ignored) {
    // Do nothing at the moment. TODO: Clearer error message displayed to the user?
  };

  var comment = {
    reply_to: dweet_id,
    text: $comment_text[0].value,
    csrfmiddlewaretoken: csrf,
  };

  var config = {
    url: '/api/comments/',
    method: 'POST',
    success: postCommentSuccess,
    error: postCommentError,
    data: comment,
  };
  $.ajax(config);
};

$(document).ready(function() {
  $('body').on('submit', 'form.like', processLike);
  $('body').on('click', '.load-comments-link', loadComments);
  $('body').on('submit', '.new-comment', postComment);
});
