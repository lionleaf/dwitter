document.addEventListener('DOMContentLoaded', function() {
  var editor = document.querySelector('#editor');
  var iframe = document.querySelector('#preview-iframe');


  oldCode = editor.value;
  showCode(oldCode);
  editor.addEventListener('keyup', function() {
    if(editor.value == oldCode) {
      return;
    }
    editor.size = Math.max(editor.value.length, 1);
    showCode(editor.value);
    oldCode = editor.value;
  });
  function showCode(code) {
    dweetwin =  iframe.contentWindow || iframe;
    dweetwin.postMessage("code "+code,iframe.src);
  }
}, false);

