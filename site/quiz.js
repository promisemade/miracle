import { escapeHtml, fetchJson, localResourceUrl, qsa, qs, sample } from "./common.js";

const STORAGE_KEYS = {
  stats: "miracle-static-quiz-stats-v1",
  history: "miracle-static-quiz-history-v1",
  wrong: "miracle-static-quiz-wrong-v1",
};

const state = {
  data: null,
  mode: "qcm",
  stats: readJson(STORAGE_KEYS.stats, {
    sessions: 0,
    questionsAnswered: 0,
    correctAnswers: 0,
    flashcardsSeen: 0,
  }),
  history: readJson(STORAGE_KEYS.history, []),
  wrongIds: new Set(readJson(STORAGE_KEYS.wrong, [])),
  session: null,
};

document.addEventListener("DOMContentLoaded", init);

async function init() {
  state.data = await fetchJson("./data/questions.json");

  qs("#metricQuestions").textContent = (state.data.qcm || []).length;
  populateCategories();
  wireControls();
  updateStats();
  renderHistory();
}

function wireControls() {
  qsa("[data-mode]").forEach((button) => {
    button.addEventListener("click", () => {
      state.mode = button.dataset.mode;
      qsa("[data-mode]").forEach((btn) => btn.classList.toggle("is-active", btn === button));
      qs("#modeNote").textContent = modeNote(state.mode);
    });
  });

  qs("#startSessionBtn").addEventListener("click", startSession);
  qs("#resetStatsBtn").addEventListener("click", resetStats);
}

function populateCategories() {
  const categories = state.data.categories || [];
  qs("#categorySelect").innerHTML = [
    '<option value="">Toutes les categories</option>',
    ...categories.map((cat) => `<option value="${escapeHtml(cat.id)}">${escapeHtml(cat.name)}</option>`),
  ].join("");
}

function modeNote(mode) {
  if (mode === "review") return "Mode erreurs: rejoue seulement les questions manquees.";
  if (mode === "flashcards") return "Mode flashcards: retourne la carte, puis passe a la suivante.";
  return "Mode QCM: reponse, explication, puis question suivante.";
}

function startSession() {
  const category = qs("#categorySelect").value;
  const count = Number(qs("#countSelect").value);

  if (state.mode === "flashcards") {
    const source = filteredFlashcards(category);
    const items = sample(source, Math.min(count, source.length));
    if (!items.length) return renderEmpty("Aucune flashcard disponible pour ce filtre.");
    state.session = {
      type: "flashcards",
      category,
      items,
      index: 0,
      flipped: false,
      seen: 0,
    };
    renderFlashcard();
    return;
  }

  const source = state.mode === "review" ? filteredWrongQuestions(category) : filteredQuestions(category);
  const items = sample(source, Math.min(count, source.length));
  if (!items.length) {
    return renderEmpty(state.mode === "review"
      ? "Aucune question a revoir pour ce filtre."
      : "Aucune question disponible pour ce filtre.");
  }

  state.session = {
    type: "qcm",
    mode: state.mode,
    category,
    items,
    index: 0,
    correct: 0,
    answers: [],
    revealed: false,
  };
  renderQuestion();
}

function filteredQuestions(category) {
  return (state.data.qcm || []).filter((question) => !category || question.category === category);
}

function filteredWrongQuestions(category) {
  return filteredQuestions(category).filter((question) => state.wrongIds.has(question.id));
}

function filteredFlashcards(category) {
  return (state.data.flashcards || []).filter((card) => !category || card.category === category);
}

function renderQuestion() {
  const session = state.session;
  const question = session.items[session.index];
  const total = session.items.length;

  qs("#sessionTitle").textContent = session.mode === "review" ? "Session erreurs" : "Session QCM";
  qs("#sessionSubtitle").textContent = `Question ${session.index + 1} sur ${total}`;

  const sourceLink = question.source_url ? localResourceUrl(question.source_url) : null;
  qs("#sessionPane").innerHTML = `
    <div class="session-card">
      <div class="question-card">
        <div class="question-head">
          <span class="tag">${escapeHtml(categoryName(question.category))}</span>
          <span class="tag">Difficulte ${question.difficulty ?? "?"}</span>
        </div>
        <div class="question-text">${escapeHtml(question.question)}</div>
      </div>
      <div class="options">
        ${(question.options || []).map((option, index) => `
          <button class="option" data-answer-index="${index}" type="button">${escapeHtml(option)}</button>
        `).join("")}
      </div>
      <div id="explanationWrap"></div>
      <div class="button-row">
        <button id="nextBtn" class="btn btn-primary hidden" type="button"><i class="ri-arrow-right-line"></i>${session.index + 1 === total ? "Terminer" : "Suivante"}</button>
        ${sourceLink ? `<a class="btn" href="${sourceLink}" target="_blank" rel="noreferrer"><i class="ri-book-open-line"></i>Source</a>` : ""}
      </div>
    </div>
  `;

  qsa("[data-answer-index]").forEach((button) => {
    button.addEventListener("click", () => answerQuestion(Number(button.dataset.answerIndex)));
  });
  qs("#nextBtn").addEventListener("click", nextQuestion);
}

function answerQuestion(selectedIndex) {
  const session = state.session;
  const question = session.items[session.index];
  if (session.revealed) return;

  session.revealed = true;
  const isCorrect = selectedIndex === question.correct;
  if (isCorrect) {
    session.correct += 1;
    state.wrongIds.delete(question.id);
  } else {
    state.wrongIds.add(question.id);
  }
  session.answers.push({ id: question.id, selectedIndex, isCorrect });
  persistWrongIds();

  qsa("[data-answer-index]").forEach((button) => {
    const index = Number(button.dataset.answerIndex);
    button.disabled = true;
    if (index === question.correct) button.classList.add("is-correct");
    if (index === selectedIndex && !isCorrect) button.classList.add("is-wrong");
  });

  qs("#explanationWrap").innerHTML = `
    <div class="explanation">
      <strong>${isCorrect ? "Bonne reponse." : "A revoir."}</strong><br>
      ${escapeHtml(question.explanation || "Pas d'explication disponible.")}
    </div>
  `;
  qs("#nextBtn").classList.remove("hidden");
  updateStats();
}

function nextQuestion() {
  const session = state.session;
  if (!session) return;
  session.revealed = false;
  session.index += 1;
  if (session.index >= session.items.length) {
    finishQcmSession();
    return;
  }
  renderQuestion();
}

function finishQcmSession() {
  const session = state.session;
  const total = session.items.length;
  const percent = Math.round((session.correct / total) * 100);

  state.stats.sessions += 1;
  state.stats.questionsAnswered += total;
  state.stats.correctAnswers += session.correct;
  persistStats();

  prependHistory({
    title: session.mode === "review" ? "Erreurs" : "QCM",
    subtitle: `${session.correct}/${total} bonnes reponses`,
    value: `${percent}%`,
  });

  qs("#sessionTitle").textContent = "Session terminee";
  qs("#sessionSubtitle").textContent = "Resultat enregistre localement";
  qs("#sessionPane").innerHTML = `
    <div class="question-card">
      <div class="question-head">
        <span class="tag">${session.mode === "review" ? "Erreurs" : "QCM"}</span>
        <span class="tag">${percent}%</span>
      </div>
      <div class="question-text">Score final: ${session.correct} bonne(s) reponse(s) sur ${total}.</div>
      <div class="explanation" style="margin-top:16px;">
        Les questions manquees restent dans le mode "Erreurs" tant qu'elles ne sont pas reussies.
      </div>
      <div class="button-row" style="margin-top:16px;">
        <button id="restartBtn" class="btn btn-primary" type="button"><i class="ri-refresh-line"></i>Nouvelle session</button>
      </div>
    </div>
  `;
  qs("#restartBtn").addEventListener("click", startSession);
  state.session = null;
  updateStats();
  renderHistory();
}

function renderFlashcard() {
  const session = state.session;
  const card = session.items[session.index];
  const total = session.items.length;
  const sourceLink = card.source_url ? localResourceUrl(card.source_url) : null;

  qs("#sessionTitle").textContent = "Flashcards";
  qs("#sessionSubtitle").textContent = `Carte ${session.index + 1} sur ${total}`;
  qs("#sessionPane").innerHTML = `
    <div class="session-card">
      <div class="flashcard">
        <div class="flashcard-side">
          <div class="flashcard-label">${session.flipped ? "Reponse" : "Question"}</div>
          <div class="flashcard-text">${escapeHtml(session.flipped ? card.back : card.front)}</div>
        </div>
      </div>
      <div class="button-row">
        <button id="flipBtn" class="btn" type="button"><i class="ri-loop-left-line"></i>${session.flipped ? "Voir la question" : "Retourner"}</button>
        <button id="nextFlashBtn" class="btn btn-primary" type="button"><i class="ri-arrow-right-line"></i>${session.index + 1 === total ? "Terminer" : "Suivante"}</button>
        ${sourceLink ? `<a class="btn" href="${sourceLink}" target="_blank" rel="noreferrer"><i class="ri-book-open-line"></i>Source</a>` : ""}
      </div>
    </div>
  `;

  qs("#flipBtn").addEventListener("click", () => {
    session.flipped = !session.flipped;
    renderFlashcard();
  });
  qs("#nextFlashBtn").addEventListener("click", nextFlashcard);
}

function nextFlashcard() {
  const session = state.session;
  session.seen += 1;
  session.index += 1;
  session.flipped = false;

  if (session.index >= session.items.length) {
    state.stats.sessions += 1;
    state.stats.flashcardsSeen += session.seen;
    persistStats();
    prependHistory({
      title: "Flashcards",
      subtitle: `${session.seen} carte(s) vues`,
      value: "OK",
    });
    qs("#sessionTitle").textContent = "Session terminee";
    qs("#sessionSubtitle").textContent = "Flashcards parcourues";
    qs("#sessionPane").innerHTML = `
      <div class="question-card">
        <div class="question-text">Session terminee. ${session.seen} carte(s) vues.</div>
        <div class="button-row" style="margin-top:16px;">
          <button id="restartBtn" class="btn btn-primary" type="button"><i class="ri-refresh-line"></i>Nouvelle session</button>
        </div>
      </div>
    `;
    qs("#restartBtn").addEventListener("click", startSession);
    state.session = null;
    updateStats();
    renderHistory();
    return;
  }

  renderFlashcard();
}

function renderHistory() {
  const list = qs("#historyList");
  if (!state.history.length) {
    list.innerHTML = '<div class="empty-state">Aucune session enregistree pour le moment.</div>';
    return;
  }

  list.innerHTML = state.history
    .slice(0, 10)
    .map((item) => `
      <div class="history-item">
        <div>
          <strong>${escapeHtml(item.title)}</strong>
          <span>${escapeHtml(item.subtitle)} | ${escapeHtml(item.date)}</span>
        </div>
        <span>${escapeHtml(item.value)}</span>
      </div>
    `)
    .join("");
}

function prependHistory(entry) {
  state.history.unshift({
    ...entry,
    date: new Date().toLocaleDateString("fr-FR"),
  });
  state.history = state.history.slice(0, 20);
  persistHistory();
}

function updateStats() {
  const answered = state.stats.questionsAnswered || 0;
  const correct = state.stats.correctAnswers || 0;
  const accuracy = answered ? Math.round((correct / answered) * 100) : 0;
  qs("#metricSessions").textContent = state.stats.sessions || 0;
  qs("#metricAccuracy").textContent = `${accuracy}%`;
  qs("#metricWrong").textContent = state.wrongIds.size;
}

function resetStats() {
  state.stats = { sessions: 0, questionsAnswered: 0, correctAnswers: 0, flashcardsSeen: 0 };
  state.history = [];
  state.wrongIds = new Set();
  persistStats();
  persistHistory();
  persistWrongIds();
  updateStats();
  renderHistory();
  renderEmpty("Statistiques reinitialisees. Lance une nouvelle session.");
}

function renderEmpty(message) {
  state.session = null;
  qs("#sessionTitle").textContent = "Pret";
  qs("#sessionSubtitle").textContent = "Lance une session pour commencer.";
  qs("#sessionPane").innerHTML = `<div class="empty-state">${escapeHtml(message)}</div>`;
}

function categoryName(categoryId) {
  return (state.data.categories || []).find((category) => category.id === categoryId)?.name || categoryId || "General";
}

function persistStats() {
  localStorage.setItem(STORAGE_KEYS.stats, JSON.stringify(state.stats));
}

function persistHistory() {
  localStorage.setItem(STORAGE_KEYS.history, JSON.stringify(state.history));
}

function persistWrongIds() {
  localStorage.setItem(STORAGE_KEYS.wrong, JSON.stringify([...state.wrongIds]));
}

function readJson(key, fallback) {
  try {
    const raw = localStorage.getItem(key);
    return raw ? JSON.parse(raw) : fallback;
  } catch {
    return fallback;
  }
}
