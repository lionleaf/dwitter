// Check for compatibility
if (window.localStorage){
  var l = document.getElementById('style');
  var switchTheme = function(){
    // Change the imported stylesheet from main.css to main_dark.css or vice versa
    // Change localstorage theme to 'dark'
    var theme = localStorage.getItem('theme');
    if (theme == 'dark')
    {
      localStorage.setItem('theme','');
      l.setAttribute('href', '{% static "main.css" %}');
    }
    else{
      localStorage.setItem('theme','dark');
      l.setAttribute('href', '{% static "main_dark.css" %}');
    }
    location.reload();
    // Call this function in the li to change the mode
  }

  // Do the same thing outside the function without changing localStorage to set correct theme
  var theme = localStorage.getItem('theme');
  if (theme == '')
  {
    l.setAttribute('href', '{% static "main.css" %}');
  }
  else{
    l.setAttribute('href', '{% static "main_dark.css" %}');
  }
}
