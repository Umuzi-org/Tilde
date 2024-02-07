function toggleIcon(){
    const editSubmissionLinkIcon =  document.getElementById("edit_submission_link_icon");
    editSubmissionLinkIcon.style.display = (editSubmissionLinkIcon.style.display === "none") ? "block" : "none";
}

function displayForm(){
    const form = document.getElementById("link_submission_form");
    form.style.display = "block"
    toggleIcon()
}

