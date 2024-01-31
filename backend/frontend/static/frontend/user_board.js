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

function showCardAlert({
  cardId,
  message,
  alertType = "info",
  persist = true,
}) {
  const alertThemes = {
    success: "border-green-300 bg-green-100 text-green-800",
    error: "border-red-300 bg-red-100 text-red-800",
    warning: "border-yellow-300 bg-yellow-100 text-yellow-800",
    info: "border-blue-300 bg-blue-100 text-blue-800",
  };

  const iconThemes = {
    success: "fa-check-circle",
    error: "fa-times-circle",
    warning: "fa-exclamation-circle",
    info: "fa-info-circle",
  };

  const card = document.getElementById(`card_${cardId}`);
  const alert = document.createElement("div");

  const buttons = card.querySelectorAll('button');

  let startButton
  for(let i=0;i<buttons.length;i++){
    if (buttons[i].textContent.trim()==="Start"){
      startButton=buttons[i]
    }
  }
  
  alert.className = `mb-3 relative leading-tight flex gap-2 rounded-xl border p-3 text-sm ${alertThemes[alertType]}`;

  alert.innerHTML = `
      <i class="fas ${iconThemes[alertType]} self-center"></i>
      <p>${message}</p>
  `;

  card.parentNode.insertBefore(alert, card);

  if (alertType === "error" || alertType === "warning") {
    // shake the card to draw attention to the error
    card.classList.add("shake");
    alert.classList.add("shake");
    // disable buttons
    startButton.classList.add("disable-button")
  }

  if (!persist) {
    // clear the alert after 5 seconds if it's not a persistent alert
    setTimeout(() => {
      alert.remove();
      startButton.classList.remove("disable-button")
    }, 5000);
  }
}
