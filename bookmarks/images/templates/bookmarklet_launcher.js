(function(){
  if (window.myBookmarklet !== undefined){
    myBookmarklet();
  }
  else {
    document.body.appendChild(
      document.createElement('script')
    ).src='https://c987f400d36d.ngrok.io/static/js/bookmarklet.js?r=' +
    Math.floor(Math.random()*99999999999999999999);
  }
})();
// ).src='http://127.0.0.1:8000/static/js/bookmarklet.js?r=' +