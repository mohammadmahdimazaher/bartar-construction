(function () {
  function setupSaleAvailability() {
    const statusField = document.getElementById("id_construction_status");
    const saleRow = document.querySelector(".form-row.field-is_for_sale");
    const saleField = document.getElementById("id_is_for_sale");

    if (!statusField || !saleRow || !saleField) return;

    function syncSaleField() {
      const isCompleted = statusField.value === "completed";
      saleRow.hidden = !isCompleted;
      saleRow.style.display = isCompleted ? "" : "none";
      if (!isCompleted) saleField.checked = false;
    }

    statusField.addEventListener("change", syncSaleField);
    syncSaleField();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", setupSaleAvailability);
  } else {
    setupSaleAvailability();
  }
})();
