import { assetUrl, countBy, escapeHtml, fetchJson, qsa, qs, sample, toSortedEntries } from "./common.js";

const state = {
  fiches: [],
  selectedId: null,
  filtered: [],
  visibleCount: 24,
};

const views = ["fiches", "training", "stats"];

document.addEventListener("DOMContentLoaded", init);

async function init() {
  wireViewButtons();
  wireFilters();

  qs("#loadMoreBtn").addEventListener("click", () => {
    state.visibleCount += 24;
    renderFichesList();
  });
  qs("#drawRandomBtn").addEventListener("click", () => drawRandom(false));
  qs("#drawFromFiltersBtn").addEventListener("click", () => drawRandom(true));
  qs("#resetFiltersBtn").addEventListener("click", resetFilters);

  const [fiches, quizData, ministeresData] = await Promise.all([
    fetchJson("./data/fiches.json"),
    fetchJson("./data/questions.json"),
    fetchJson("./data/ministeres.json"),
  ]);

  state.fiches = fiches;
  qs("#heroFichesCount").textContent = fiches.length;
  qs("#heroQuizCount").textContent = (quizData.qcm || []).length;
  qs("#heroMinisteresCount").textContent = (ministeresData.ministeres || []).length;

  populateSelect("#domaineSelect", uniqueSorted(fiches.map((f) => f.domaine)));
  populateSelect("#administrationSelect", uniqueSorted(fiches.map((f) => f.administration)));
  populateSelect("#structureSelect", uniqueSorted(fiches.map((f) => f.structure)));
  populateSelect("#regionSelect", uniqueSorted(fiches.map((f) => f.region).filter(Boolean)));

  renderStats();
  applyFilters();
  syncViewFromHash();
  window.addEventListener("hashchange", syncViewFromHash);
}

function wireViewButtons() {
  qsa("[data-view]").forEach((button) => {
    button.addEventListener("click", () => {
      window.location.hash = button.dataset.view;
    });
  });
}

function wireFilters() {
  ["#searchInput", "#domaineSelect", "#administrationSelect", "#structureSelect", "#regionSelect"].forEach((selector) => {
    const input = qs(selector);
    input.addEventListener("input", applyFilters);
    input.addEventListener("change", applyFilters);
  });
}

function populateSelect(selector, values) {
  qs(selector).innerHTML = [
    '<option value="">Tous</option>',
    ...values.map((value) => `<option value="${escapeHtml(value)}">${escapeHtml(value)}</option>`),
  ].join("");
}

function uniqueSorted(values) {
  return [...new Set(values.filter(Boolean))].sort((a, b) => a.localeCompare(b, "fr"));
}

function resetFilters() {
  qs("#searchInput").value = "";
  qs("#domaineSelect").value = "";
  qs("#administrationSelect").value = "";
  qs("#structureSelect").value = "";
  qs("#regionSelect").value = "";
  state.visibleCount = 24;
  applyFilters();
}

function getFilters() {
  return {
    search: qs("#searchInput").value.trim().toLowerCase(),
    domaine: qs("#domaineSelect").value,
    administration: qs("#administrationSelect").value,
    structure: qs("#structureSelect").value,
    region: qs("#regionSelect").value,
  };
}

function applyFilters() {
  const filters = getFilters();

  state.filtered = state.fiches.filter((fiche) => {
    if (filters.search) {
      const haystack = [fiche.titre, fiche.administration, fiche.structure, fiche.domaine, fiche.region]
        .filter(Boolean)
        .join(" ")
        .toLowerCase();
      if (!haystack.includes(filters.search)) return false;
    }
    if (filters.domaine && fiche.domaine !== filters.domaine) return false;
    if (filters.administration && fiche.administration !== filters.administration) return false;
    if (filters.structure && fiche.structure !== filters.structure) return false;
    if (filters.region && fiche.region !== filters.region) return false;
    return true;
  });

  if (!state.filtered.some((item) => item.id === state.selectedId)) {
    state.selectedId = state.filtered[0]?.id ?? null;
  }

  renderFilterSummary(filters);
  renderFichesList();
  renderDetail();
}

function renderFilterSummary(filters) {
  const parts = [];
  if (filters.search) parts.push(`Recherche: ${filters.search}`);
  if (filters.domaine) parts.push(`Domaine: ${filters.domaine}`);
  if (filters.administration) parts.push(`Administration: ${filters.administration}`);
  if (filters.structure) parts.push(`Structure: ${filters.structure}`);
  if (filters.region) parts.push(`Region: ${filters.region}`);

  const prefix = `${state.filtered.length} fiche${state.filtered.length > 1 ? "s" : ""}`;
  qs("#filterSummary").textContent = parts.length ? `${prefix}. ${parts.join(" | ")}` : `${prefix}. Aucun filtre actif.`;
}

function renderFichesList() {
  const list = qs("#fichesList");
  if (!state.filtered.length) {
    list.innerHTML = '<div class="empty-state">Aucune fiche ne correspond aux filtres actuels.</div>';
    qs("#fichesMoreWrap").classList.add("hidden");
    return;
  }

  const visible = state.filtered.slice(0, state.visibleCount);
  list.innerHTML = visible
    .map((fiche) => {
      const activeClass = fiche.id === state.selectedId ? "is-active" : "";
      return `
        <article class="list-card ${activeClass}" data-fiche-id="${fiche.id}">
          <h3 class="list-card-title">${escapeHtml(fiche.titre)}</h3>
          <div class="list-card-meta">
            <span class="tag">${escapeHtml(fiche.domaine)}</span>
            <span class="tag">${escapeHtml(fiche.structure)}</span>
            ${fiche.region ? `<span class="tag">${escapeHtml(fiche.region)}</span>` : ""}
          </div>
        </article>
      `;
    })
    .join("");

  qsa("[data-fiche-id]").forEach((card) => {
    card.addEventListener("click", () => {
      state.selectedId = Number(card.dataset.ficheId);
      renderFichesList();
      renderDetail();
    });
  });

  qs("#fichesMoreWrap").classList.toggle("hidden", state.filtered.length <= visible.length);
}

function renderDetail() {
  const pane = qs("#detailPane");
  const fiche = state.filtered.find((item) => item.id === state.selectedId);

  if (!fiche) {
    pane.innerHTML = '<div class="empty-state">Choisis une fiche pour afficher son contenu ici.</div>';
    return;
  }

  const pdfUrl = assetUrl(`Fiches de postes/${fiche.path}`);
  pane.innerHTML = `
    <h2 class="detail-title">${escapeHtml(fiche.titre)}</h2>
    <p class="detail-lead">${escapeHtml(fiche.administration)} | ${escapeHtml(fiche.structure)}</p>
    <div class="detail-meta">
      <span class="tag">${escapeHtml(fiche.domaine)}</span>
      ${fiche.region ? `<span class="tag">${escapeHtml(fiche.region)}</span>` : ""}
    </div>
    <div class="button-row" style="margin:16px 0 18px;">
      <a class="btn btn-primary" href="${pdfUrl}" target="_blank" rel="noreferrer"><i class="ri-external-link-line"></i>Ouvrir le PDF</a>
      <button class="btn" type="button" id="copyTitleBtn"><i class="ri-file-copy-line"></i>Copier le titre</button>
    </div>
    <iframe class="pdf-frame" src="${pdfUrl}" title="${escapeHtml(fiche.titre)}"></iframe>
  `;

  const copyBtn = qs("#copyTitleBtn");
  copyBtn.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(fiche.titre);
      copyBtn.innerHTML = '<i class="ri-check-line"></i>Copie';
      setTimeout(() => {
        copyBtn.innerHTML = '<i class="ri-file-copy-line"></i>Copier le titre';
      }, 1200);
    } catch {
      copyBtn.innerHTML = '<i class="ri-close-line"></i>Echec';
    }
  });
}

function drawRandom(useFilteredPool) {
  const pool = useFilteredPool && state.filtered.length ? state.filtered : state.fiches;
  const [fiche] = sample(pool, 1);
  const pane = qs("#trainingPane");

  if (!fiche) {
    pane.innerHTML = '<div class="empty-state">Aucune fiche disponible pour ce tirage.</div>';
    return;
  }

  const pdfUrl = assetUrl(`Fiches de postes/${fiche.path}`);
  pane.innerHTML = `
    <div class="question-card">
      <div class="question-head">
        <div>
          <div class="eyebrow" style="margin-bottom:6px;">Tirage</div>
          <h2 class="detail-title" style="font-size:1.7rem;">${escapeHtml(fiche.titre)}</h2>
        </div>
        <span class="tag">${escapeHtml(fiche.domaine)}</span>
      </div>
      <p class="section-copy">${escapeHtml(fiche.administration)} | ${escapeHtml(fiche.structure)}${fiche.region ? ` | ${escapeHtml(fiche.region)}` : ""}</p>
      <div class="button-row" style="margin-top:16px;">
        <a class="btn btn-primary" href="${pdfUrl}" target="_blank" rel="noreferrer"><i class="ri-external-link-line"></i>Ouvrir le PDF</a>
        <button class="btn" type="button" id="focusCurrentBtn"><i class="ri-focus-3-line"></i>Afficher aussi dans Fiches</button>
      </div>
      <iframe class="pdf-frame" style="margin-top:18px; min-height:560px;" src="${pdfUrl}" title="${escapeHtml(fiche.titre)}"></iframe>
    </div>
  `;

  const focusBtn = qs("#focusCurrentBtn");
  focusBtn.addEventListener("click", () => {
    state.selectedId = fiche.id;
    if (!state.filtered.some((item) => item.id === fiche.id)) {
      resetFilters();
    } else {
      renderFichesList();
      renderDetail();
    }
    window.location.hash = "fiches";
  });
}

function renderStats() {
  const domains = countBy(state.fiches, (fiche) => fiche.domaine);
  const structures = countBy(state.fiches, (fiche) => fiche.structure);
  const administrations = countBy(state.fiches, (fiche) => fiche.administration);
  const regions = countBy(state.fiches, (fiche) => fiche.region || "Non renseigne");

  qs("#metricTotal").textContent = state.fiches.length;
  qs("#metricAdmins").textContent = Object.keys(administrations).length;
  qs("#metricDomaines").textContent = Object.keys(domains).length;
  qs("#metricRegions").textContent = Object.keys(regions).length;

  renderRankList("#statsDomaines", toSortedEntries(domains, 12));
  renderRankList("#statsStructures", toSortedEntries(structures, 12));
  renderRankList("#statsAdministrations", toSortedEntries(administrations, 12));
}

function renderRankList(selector, entries) {
  qs(selector).innerHTML = entries
    .map(
      ([label, count]) => `
        <div class="rank-item">
          <div><strong>${escapeHtml(label)}</strong></div>
          <span>${count}</span>
        </div>
      `,
    )
    .join("");
}

function syncViewFromHash() {
  const view = views.includes(window.location.hash.slice(1)) ? window.location.hash.slice(1) : "fiches";
  views.forEach((name) => {
    qs(`#view-${name}`).classList.toggle("hidden", name !== view);
  });
  qsa("[data-view]").forEach((button) => {
    button.classList.toggle("is-active", button.dataset.view === view);
  });
}
