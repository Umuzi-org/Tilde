/* 
When we page we need to see how many items are in a parent element. The "load more" button will also be in there
*/
function countLoadedPageItems(parentId) {
  const parent = document.getElementById(parentId);
  return parent.childElementCount - 1; // the button is an element too
}

/*
 * Swaps in the body of error pages returned from htmx requests 
 * for example when an action is forbidden.
 */
document.addEventListener("htmx:beforeOnLoad", function (event) {
  const xhr = event.detail.xhr
  if (xhr.status == 500 || xhr.status == 403 || xhr.status == 404) {
    event.stopPropagation() // Tell htmx not to process these requests
    document.children[0].innerHTML = xhr.response // Swap in body of response instead
  }
})