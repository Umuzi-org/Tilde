function moveCardToCorrectColumn(cardId, column) {
  const card = document.getElementById(`card_${cardId}`);
  const currentColumn = card.parentElement;
  const destinationColumn = document.getElementById(`column_${column}`);

  if (currentColumn !== destinationColumn) {
    // delete the card from the current column
    currentColumn.removeChild(card);

    // add the card to the top of the destination column
    destinationColumn.insertBefore(card, destinationColumn.firstChild);
  }
}
