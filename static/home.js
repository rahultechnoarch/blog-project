function setStyleSheet(url, classvalue){
  var stylesheet = document.getElementById('stylesheet');
  stylesheet.setAttribute('href', url);

  var NavClass = document.getElementById('nav-mode');
  NavClass.setAttribute('class', classvalue);

}

