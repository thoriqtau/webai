window.addEventListener("pageshow", function (event) {
  const navType = performance.getEntriesByType("navigation")[0]?.type;

  if (
    event.persisted || 
    navType === "reload" || 
    navType === "back_forward"
  ) {
    // Hapus semua value input
    document.querySelectorAll("input").forEach(input => input.value = "");

    // Hapus semua pesan error
    document.querySelectorAll(".error-message").forEach(el => el.remove());
  }
});
