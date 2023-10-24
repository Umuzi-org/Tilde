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

/* Used when fetching the next page of cards, we check how many cards there are and then fetch the next batch */
function countCardsInColumn(columnId) {
  const column = document.getElementById(`column_${columnId}`);
  return column.childElementCount - 1; // the button is an element too
}
