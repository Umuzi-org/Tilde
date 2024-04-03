/* 
When we page we need to see how many items are in a parent element. The "load more" button will also be in there
*/
function countLoadedPageItems(parentId) {
  const parent = document.getElementById(parentId);
  return parent.childElementCount - 1; // the button is an element too
}

/*
  Detect user's timezone and store it in a cookie.
*/
(function () {
  let tz = Intl.DateTimeFormat().resolvedOptions().timeZone;
  if (!tz) {
    tz = "Africa/Johannesburg"
  }
  document.cookie = "tilde_tz=" + tz + ";path=/";
})();