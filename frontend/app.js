"use strict";

const form = document.getElementById("visit-form");
const doctorSelect = document.getElementById("doctor");
const visitDateInput = document.getElementById("visit-date");
const visitsBody = document.querySelector("#visits-table tbody");
const message = document.getElementById("form-message");

async function loadDoctors() {
  const response = await fetch("/api/doctors");
  const data = await response.json();
  doctorSelect.innerHTML = "";
  for (const doctor of data.doctors) {
    const option = document.createElement("option");
    option.value = doctor.id;
    option.textContent = `${doctor.name} (${doctor.specialty})`;
    doctorSelect.appendChild(option);
  }
}

async function loadVisits() {
  const response = await fetch("/api/visits");
  const data = await response.json();
  visitsBody.innerHTML = "";
  if (data.visits.length === 0) {
    visitsBody.appendChild(renderEmptyRow());
    return;
  }
  for (const visit of data.visits) {
    visitsBody.appendChild(renderVisitRow(visit));
  }
}

function renderEmptyRow() {
  const row = document.createElement("tr");
  const cell = document.createElement("td");
  cell.colSpan = 5;
  cell.className = "empty";
  cell.textContent = "Brak zaplanowanych wizyt.";
  row.appendChild(cell);
  return row;
}

function renderVisitRow(visit) {
  const row = document.createElement("tr");
  const doctor = `${visit.doctor_name} – ${visit.doctor_specialty}`;
  const statusLabel =
    visit.status === "cancelled" ? "Odwołana" : "Zarezerwowana";

  row.appendChild(createCell(visit.patient_name));
  row.appendChild(createCell(doctor));
  row.appendChild(createCell(formatDate(visit.visit_date)));
  row.appendChild(createCell(statusLabel));

  const actionCell = document.createElement("td");
  if (visit.status !== "cancelled") {
    const button = document.createElement("button");
    button.textContent = "Odwołaj";
    button.className = "cancel";
    button.addEventListener("click", () => cancelVisit(visit.id));
    actionCell.appendChild(button);
  }
  row.appendChild(actionCell);
  return row;
}

function createCell(text) {
  const cell = document.createElement("td");
  cell.textContent = text;
  return cell;
}

async function cancelVisit(id) {
  if (!window.confirm("Czy na pewno odwołać tę wizytę?")) {
    return;
  }
  await fetch(`/api/visits/${id}`, { method: "DELETE" });
  showMessage("Wizyta została odwołana.", false);
  await loadVisits();
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  clearMessage();
  const payload = {
    patient_name: document.getElementById("patient-name").value,
    doctor_id: Number(doctorSelect.value),
    visit_date: visitDateInput.value,
  };
  const response = await fetch("/api/visits", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (response.ok) {
    form.reset();
    setMinVisitDate();
    showMessage("Wizyta została zarezerwowana.", false);
    await loadVisits();
  } else {
    const data = await response.json();
    showMessage(data.error || "Nie udało się zarezerwować wizyty.", true);
  }
});

function showMessage(text, isError) {
  message.textContent = text;
  message.classList.toggle("error", isError);
  message.classList.toggle("success", !isError);
}

function clearMessage() {
  message.textContent = "";
  message.classList.remove("error", "success");
}

function setMinVisitDate() {
  const now = new Date();
  now.setSeconds(0, 0);
  const offsetMs = now.getTimezoneOffset() * 60000;
  visitDateInput.min = new Date(now.getTime() - offsetMs)
    .toISOString()
    .slice(0, 16);
}

function formatDate(value) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value;
  }
  return date.toLocaleString("pl-PL");
}

setMinVisitDate();
loadDoctors().then(loadVisits);
