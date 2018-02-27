// Check for compatibility
if (localStorage){
  var switchTheme = function(){
    // Change the imported stylesheet from main.css to main_dark.css or vice versa
    // Change localstorage theme to 'dark'
    var theme = localStorage.getItem('theme');
    if (theme == 'dark')
    {
      localStorage.setItem('theme','');
      l = document.getElementById('style');
      l.setAttribute('href', '{% static "main.css" %}');
    }
    else{
      localStorage.setItem('theme','dark');
      l = document.getElementById('style');
      l.setAttribute('href', '{% static "main_dark.css" %}');
    }
    location.reload();
    // Call this function in the li to change the mode
  }

  // Do the same thing outside the function without changing localStorage to set correct theme
  var theme = localStorage.getItem('theme');
  if (theme == '')
  {
    l = document.getElementById('style');
    l.setAttribute('href', '{% static "main.css" %}');
  }
  else{
    l = document.getElementById('style');
    l.setAttribute('href', '{% static "main_dark.css" %}');
  }
}
