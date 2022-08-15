function deleteNote(questionId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ questionId: questionId }),
  }).then((res) => {
    window.location.href = "/admin";
  });
}
