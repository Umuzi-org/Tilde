/*
This gets called when we do anything to update the state of a card. It just moves the card into the correct column and puts it right at the top.

TODO: Preserve the order of the cards in the column  
*/
function moveCardToCorrectColumn(cardId, column) {
  const card = document.getElementById(`card_${cardId}`);
  const currentColumn = card.parentElement;

  const backlogColumns = ["R", "B"];
  if (backlogColumns.includes(column)) {
    column = "RB";
  }
  const destinationColumn = document.getElementById(`column_${column}`);

  if (currentColumn !== destinationColumn) {
    // delete the card from the current column
    currentColumn.removeChild(card);

    // add the card to the top of the destination column
    destinationColumn.insertBefore(card, destinationColumn.firstChild);
  }
}
