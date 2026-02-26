// Helper: show/hide elements
const $ = (sel) => document.querySelector(sel);

function toggle(el, show) {
  if (!el) return;
  if (show) {
    el.classList.remove("hidden");
    el.classList.add("animate__fadeIn");
  } else {
    el.classList.add("hidden");
    el.classList.remove("animate__fadeIn");
  }
}

function openModal(id) {
  const el = document.getElementById(id);
  if (!el) return;
  el.classList.remove("hidden");
}

function closeModal(id) {
  const el = document.getElementById(id);
  if (!el) return;
  el.classList.add("hidden");
}

function celebrate() {
  if (typeof confetti !== "function") return;
  const duration = 2000;
  const end = Date.now() + duration;

  (function frame() {
    confetti({
      particleCount: 3,
      angle: 60,
      spread: 55,
      origin: { x: 0 },
      colors: ["#f9c74f", "#90be6d", "#f94144", "#577590", "#f9844a"]
    });
    confetti({
      particleCount: 3,
      angle: 120,
      spread: 55,
      origin: { x: 1 },
      colors: ["#f9c74f", "#90be6d", "#f94144", "#577590", "#f9844a"]
    });
    if (Date.now() < end) requestAnimationFrame(frame);
  })();
}

document.addEventListener("DOMContentLoaded", () => {
  const nameInput   = $("#nameInput");
  const genderRow   = $("#genderRow");
  const genderSelect= $("#genderSelect");

  // Unlock gender selector only if name is "shreya"
  nameInput.addEventListener("input", () => {
    const val = (nameInput.value || "").trim().toLowerCase();
    toggle(genderRow, val === "shreya");
    if (val !== "shreya") genderSelect.value = "";
  });

  // Handle selection
  genderSelect.addEventListener("change", () => {
    const v = genderSelect.value;
    if (!v) return;
    if (["male", "female", "angel"].includes(v)) {
      openModal("errorModal");
    } else if (v === "bhaluu") {
      openModal("successModal");
      celebrate();
    }
  });

  // Modal close buttons
  document.querySelectorAll("[data-close]").forEach(btn => {
    btn.addEventListener("click", () => closeModal(btn.getAttribute("data-close")));
  });

  // Close on backdrop click
  document.querySelectorAll(".modal").forEach(m => {
    m.addEventListener("click", (e) => {
      if (e.target.classList.contains("modal")) {
        m.classList.add("hidden");
      }
    });
  });
});
