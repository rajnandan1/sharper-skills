document.addEventListener("click", async (event) => {
  const button = event.target.closest("[data-copy]");
  if (!button) return;
  const field = document.getElementById(button.dataset.copy);
  const status = button.parentElement.querySelector(".copy-status") || document.querySelector(".copy-status");
  const label = button.querySelector(".copy-label");
  try {
    const text = field.value ?? field.textContent.trim();
    await navigator.clipboard.writeText(text);
    label.textContent = "Copied";
    if (status) status.textContent = "Copied: " + text;
  } catch {
    if (field.select) { field.focus(); field.select(); } else { const range = document.createRange(); range.selectNodeContents(field); const sel = getSelection(); sel.removeAllRanges(); sel.addRange(range); }
    label.textContent = "Press Ctrl+C";
    if (status) status.textContent = "Copy failed. The command is selected: press Ctrl+C, or Cmd+C on a Mac.";
  }
  clearTimeout(button._reset);
  button._reset = setTimeout(() => { label.textContent = "Copy"; }, 2400);
});
