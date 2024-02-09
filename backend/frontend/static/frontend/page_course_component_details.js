function toggleEditLinkSubmissionIcon(){
    const editLinkSubmissionIcon =  document.getElementById("edit_link_submission_icon");
    editLinkSubmissionIcon.style.display = (editLinkSubmissionIcon.style.display === "none") ? "block" : "none";
}

function displayLinkSubmissionForm(){
    const form = document.getElementById("link_submission_form");
    form.style.display = "block"
    toggleEditLinkSubmissionIcon()
}

