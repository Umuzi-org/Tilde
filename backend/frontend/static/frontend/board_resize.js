/* 
 Adjust the height of the columns in the board to fit the window height
*/

function adjustColumnHeight() {
  const columns = document.querySelectorAll(".grid-cols-5 > div");
  const windowHeight = window.innerHeight;

  columns.forEach(function (column) {
    column.style.height = windowHeight - 160 + "px";
  });
}
