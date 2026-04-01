import { escapeHtml, fetchJson, qsa, qs } from "./common.js";

const state = {
  ministeres: [],
  filtered: [],
  selectedId: null,
};

document.addEventListener("DOMContentLoaded", init);

async function init() {
  const payload = await fetchJson("./data/ministeres.json");
  state.ministeres = payload.ministeres || [];
  state.filtered = [...state.ministeres];
  state.selectedId = state.filtered[0]?.id ?? null;

  qs("#heroCount").textContent = state.ministeres.length;
  qs("#searchMinistere").addEventListener("input", applySearch);

  renderList();
  renderDetail();
}

function applySearch() {
  const query = qs("#searchMinistere").value.trim().toLowerCase();

  state.filtered = state.ministeres.filter((ministere) => {
    if (!query) return true;
    const haystack = [
      ministere.name,
      ministere.short_name,
      ministere.resume,
      ...(ministere.missions || []),
      ...(ministere.politiques_publiques || []),
      ...(ministere.budget || []),
    ]
      .filter(Boolean)
      .join(" ")
      .toLowerCase();
    return haystack.includes(query);
  });

  if (!state.filtered.some((item) => item.id === state.selectedId)) {
    state.selectedId = state.filtered[0]?.id ?? null;
  }

  renderList();
  renderDetail();
}

function renderList() {
  qs("#listSummary").textContent = `${state.filtered.length} ministere(s) visibles`;
  const list = qs("#ministeresList");

  if (!state.filtered.length) {
    list.innerHTML = '<div class="empty-state">Aucun ministere ne correspond a la recherche.</div>';
    return;
  }

  list.innerHTML = state.filtered
    .map((ministere) => {
      const activeClass = ministere.id === state.selectedId ? "is-active" : "";
      return `
        <article class="list-card ${activeClass}" data-id="${ministere.id}">
          <h3 class="list-card-title">${escapeHtml(ministere.name)}</h3>
          <div class="list-card-meta">
            ${ministere.short_name ? `<span class="tag">${escapeHtml(ministere.short_name)}</span>` : ""}
            <span class="tag">${(ministere.missions || []).length} missions</span>
          </div>
        </article>
      `;
    })
    .join("");

  qsa("[data-id]").forEach((card) => {
    card.addEventListener("click", () => {
      state.selectedId = card.dataset.id;
      renderList();
      renderDetail();
    });
  });
}

function renderDetail() {
  const pane = qs("#ministereDetail");
  const ministere = state.filtered.find((item) => item.id === state.selectedId);

  if (!ministere) {
    pane.innerHTML = '<div class="empty-state">Choisis un ministere pour afficher sa fiche.</div>';
    return;
  }

  pane.innerHTML = `
    <h2 class="detail-title">${escapeHtml(ministere.name)}</h2>
    ${ministere.short_name ? `<p class="detail-lead">${escapeHtml(ministere.short_name)}</p>` : ""}
    <div class="button-row" style="margin:16px 0 18px;">
      ${ministere.site_url ? `<a class="btn btn-primary" href="${ministere.site_url}" target="_blank" rel="noreferrer"><i class="ri-external-link-line"></i>Site officiel</a>` : ""}
    </div>
    <div class="detail-sections">
      ${ministere.resume ? block("Resume", `<p>${escapeHtml(ministere.resume)}</p>`) : ""}
      ${renderListBlock("Missions", ministere.missions)}
      ${renderListBlock("Competences", ministere.competences)}
      ${renderListBlock("Politiques publiques", ministere.politiques_publiques)}
      ${renderListBlock("Chiffres cles", ministere.chiffres_cles)}
      ${renderListBlock("Operateurs", ministere.operateurs)}
      ${renderListBlock("Budget", ministere.budget)}
      ${renderNestedDetails(ministere.details)}
      ${renderLois(ministere.grandes_lois)}
      ${renderSources(ministere.sources)}
      ${ministere.notes ? block("Notes", `<p>${escapeHtml(ministere.notes)}</p>`) : ""}
    </div>
  `;
}

function renderListBlock(title, items) {
  if (!items || !items.length) return "";
  return block(title, `<ul>${items.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>`);
}

function renderNestedDetails(details) {
  if (!details || typeof details !== "object" || !Object.keys(details).length) return "";

  const groups = Object.entries(details)
    .map(([section, content]) => {
      if (Array.isArray(content)) {
        return `<h3>${escapeHtml(section)}</h3><ul>${content.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>`;
      }
      if (content && typeof content === "object") {
        const inner = Object.entries(content)
          .map(([label, value]) => {
            if (Array.isArray(value)) {
              return `<p><strong>${escapeHtml(label)}</strong></p><ul>${value.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>`;
            }
            return `<p><strong>${escapeHtml(label)}</strong> ${escapeHtml(String(value))}</p>`;
          })
          .join("");
        return `<h3>${escapeHtml(section)}</h3>${inner}`;
      }
      return `<p><strong>${escapeHtml(section)}</strong> ${escapeHtml(String(content))}</p>`;
    })
    .join("");

  return block("Details", groups);
}

function renderLois(lois) {
  if (!lois || !lois.length) return "";

  const html = lois
    .map((loi) => `
      <div class="content-block" style="padding:0; border:none; background:transparent;">
        <h3>${escapeHtml(loi.label || loi.title || "Texte")}</h3>
        ${loi.synthese ? `<p style="margin-bottom:10px;">${escapeHtml(loi.synthese)}</p>` : ""}
        ${Array.isArray(loi.details) && loi.details.length ? `<ul>${loi.details.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>` : ""}
        ${loi.url ? `<div class="button-row" style="margin-top:12px;"><a class="btn" href="${loi.url}" target="_blank" rel="noreferrer"><i class="ri-book-open-line"></i>Consulter</a></div>` : ""}
      </div>
    `)
    .join("");

  return block("Grands textes", html);
}

function renderSources(sources) {
  if (!sources || !sources.length) return "";
  return block(
    "Sources",
    `<ul>${sources.map((source) => `<li>${source.url ? `<a href="${source.url}" target="_blank" rel="noreferrer">${escapeHtml(source.label || source.url)}</a>` : escapeHtml(source.label || "")}</li>`).join("")}</ul>`,
  );
}

function block(title, html) {
  return `<section class="content-block"><h3>${escapeHtml(title)}</h3>${html}</section>`;
}
