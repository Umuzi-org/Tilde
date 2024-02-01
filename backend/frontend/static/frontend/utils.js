/* 
When we page we need to see how many items are in a parent element. The "load more" button will also be in there
*/
function countLoadedPageItems(parentId) {
  const parent = document.getElementById(parentId);
  return parent.childElementCount - 1; // the button is an element too
}