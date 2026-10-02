const BACKEND_URL = window.SIDEQUEST_BACKEND_URL || "http://127.0.0.1:5000";

const storageKeys = {
  saved: "sidequest:v2:saved",
  completed: "sidequest:v2:completed",
  history: "sidequest:v2:history"
};

const TIME_OPTIONS = [
  { minutes: 30, label: "30 min" },
  { minutes: 60, label: "1 hr" },
  { minutes: 120, label: "2 hr" },
  { minutes: 240, label: "4 hr" },
  { minutes: 360, label: "4+ hr" }
];

const BUDGET_LABELS = ["Free", "$", "$$", "$$$", "$$$$"];

const state = {
  city: "pittsburgh",
  category: "surprise",
  maxMinutes: 120,
  maxDistance: 10,
  budget: 2,
  party: "solo",
  places: [],
  currentIndex: 0,
  loading: false,
  photoIndex: 0,
  saved: loadJSON(storageKeys.saved, []),
  completed: loadJSON(storageKeys.completed, []),
  history: loadJSON(storageKeys.history, [])
};

const els = {
  city: document.querySelector("#city"),
  status: document.querySelector("#status"),
  deck: document.querySelector("#deck"),
  rejectButton: document.querySelector("#rejectButton"),
  likeButton: document.querySelector("#likeButton"),
  refreshDeck: document.querySelector("#refreshDeck"),
  timeRange: document.querySelector("#timeRange"),
  timeValue: document.querySelector("#timeValue"),
  distanceRange: document.querySelector("#distanceRange"),
  distanceValue: document.querySelector("#distanceValue"),
  budgetRange: document.querySelector("#budgetRange"),
  budgetValue: document.querySelector("#budgetValue"),
  savedCount: document.querySelector("#savedCount"),
  completedCount: document.querySelector("#completedCount"),
  savedGrid: document.querySelector("#savedGrid"),
  completedGrid: document.querySelector("#completedGrid"),
  historyList: document.querySelector("#historyList"),
  clearHistory: document.querySelector("#clearHistory"),
  tabs: [...document.querySelectorAll(".tab")],
  views: [...document.querySelectorAll(".view")],
  categories: [...document.querySelectorAll(".category")]
};

function loadJSON(key, fallback) {
  try {
    return JSON.parse(localStorage.getItem(key)) ?? fallback;
  } catch {
    return fallback;
  }
}

function saveState() {
  localStorage.setItem(storageKeys.saved, JSON.stringify(state.saved));
  localStorage.setItem(storageKeys.completed, JSON.stringify(state.completed));
  localStorage.setItem(storageKeys.history, JSON.stringify(state.history));
  updateCounts();
}

function updateCounts() {
  els.savedCount.textContent = state.saved.length;
  els.completedCount.textContent = state.completed.length;
}

function escapeHTML(value = "") {
  return String(value).replace(/[&<>"']/g, (char) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#039;"
  }[char]));
}

function currentPlace() {
  return state.places[state.currentIndex] || null;
}

function currentParty() {
  return document.querySelector('input[name="party"]:checked')?.value || "solo";
}

function categoryLabel(place) {
  return place.primary_type_label || place.primary_type || "Sidequest";
}

function photoURL(photoName) {
  if (!photoName) return "";
  if (photoName.startsWith("http://") || photoName.startsWith("https://")) return photoName;
  return `${BACKEND_URL}/photo?name=${encodeURIComponent(photoName)}`;
}

function placePhotos(place) {
  return (place.photo_names && place.photo_names.length)
    ? place.photo_names.slice(0, 8)
    : (place.demo_photo_urls || []).slice(0, 8);
}

function firstPhoto(place) {
  return placePhotos(place)[0];
}

function scoreText(value) {
  if (value === null || value === undefined) return "Unknown";
  return `${value}/5`;
}

function renderPhoto(place) {
  const names = placePhotos(place);
  const stage = document.querySelector("#photoStage");
  if (!stage) return;

  if (!names.length) {
    stage.innerHTML = `<div class="image-placeholder"></div>`;
    return;
  }

  state.photoIndex = Math.max(0, Math.min(state.photoIndex, names.length - 1));

  const dots = names.slice(0, 8).map((_, i) =>
    `<button class="photo-dot ${i === state.photoIndex ? "active" : ""}" data-photo-index="${i}" aria-label="Photo ${i + 1}"></button>`
  ).join("");

  stage.innerHTML = `
    <img src="${escapeHTML(photoURL(names[state.photoIndex]))}"
         alt="${escapeHTML(place.name)} photo ${state.photoIndex + 1}"
         draggable="false">
    <span class="photo-counter">${state.photoIndex + 1} / ${Math.min(names.length, 8)}</span>
    ${names.length > 1 ? `
      <button class="photo-button prev" data-photo-action="prev" aria-label="Previous photo">‹</button>
      <button class="photo-button next" data-photo-action="next" aria-label="Next photo">›</button>
      <div class="photo-dots">${dots}</div>` : ""}
  `;
}

function renderCard(place) {
  state.photoIndex = 0;

  if (!place) {
    els.deck.innerHTML = `
      <div class="empty-state">
        <strong>No more cards.</strong><br>
        Change your filters or press “Find sidequests” for another deck.
      </div>`;
    els.rejectButton.disabled = true;
    els.likeButton.disabled = true;
    return;
  }

  els.rejectButton.disabled = false;
  els.likeButton.disabled = false;

  const rating = place.rating ? `★ ${place.rating}` : "No rating";
  const reviews = place.user_rating_count ? `${place.user_rating_count.toLocaleString()} ratings` : "Rating count n/a";
  const price = place.price_label || "Price unknown";
  const time = place.estimated_time_label || "Time varies";
  const distance = Number.isFinite(place.distance_miles) ? `${place.distance_miles.toFixed(1)} mi` : "Distance n/a";
  const mapsURL = place.maps_url || "#";
  const objectives = (place.quest_objectives || []).slice(0, 6)
    .map((objective) => `<li>${escapeHTML(objective)}</li>`).join("");

  els.deck.innerHTML = `
    <article class="place-card" id="activeCard">
      <div class="swipe-stamp nope" id="nopeStamp">NOPE</div>
      <div class="swipe-stamp save" id="saveStamp">SAVE ♥</div>

      <div class="card-scroll">
        <div class="photo-stage" id="photoStage"></div>

        <div class="card-content">
          <p class="card-kicker">${escapeHTML(categoryLabel(place))}</p>
          <h2 class="card-title">${escapeHTML(place.name)}</h2>
          <a class="address-link" href="${escapeHTML(mapsURL)}" target="_blank" rel="noopener">
            ${escapeHTML(place.address || "Address unavailable")} ↗
          </a>

          <div class="quick-meta">
            <span class="meta-pill">${escapeHTML(rating)}</span>
            <span class="meta-pill">${escapeHTML(reviews)}</span>
            <span class="meta-pill">${escapeHTML(price)}</span>
            <span class="meta-pill">~${escapeHTML(time)}</span>
            <span class="meta-pill">${escapeHTML(distance)}</span>
          </div>

          <p class="intro">${escapeHTML(place.intro || "A potential sidequest worth checking out.")}</p>

          <div class="metric-grid">
            <div class="metric"><span>Nicheness</span><strong>${scoreText(place.metrics?.nicheness)}</strong></div>
            <div class="metric"><span>Distance fit</span><strong>${scoreText(place.metrics?.distance)}</strong></div>
            <div class="metric"><span>Popularity</span><strong>${scoreText(place.metrics?.popularity)}</strong></div>
            <div class="metric"><span>Accessibility</span><strong>${scoreText(place.metrics?.accessibility)}</strong></div>
            <div class="metric"><span>Adventure</span><strong>${scoreText(place.metrics?.adventure)}</strong></div>
            <div class="metric"><span>Group fit</span><strong>${scoreText(place.metrics?.group_fit)}</strong></div>
          </div>

          <section class="objectives">
            <h3>Quest objectives</h3>
            <ol>${objectives}</ol>
          </section>

          <div class="card-actions">
            <button class="card-action" data-card-action="bookmark">♡ Bookmark quest</button>
            <button class="card-action primary" data-card-action="complete">✓ Mark complete</button>
          </div>
        </div>
      </div>
    </article>
  `;

  renderPhoto(place);
  attachSwipeGesture(document.querySelector("#activeCard"));
}

function syncControls() {
  const timeOption = TIME_OPTIONS[Number(els.timeRange.value)] || TIME_OPTIONS[2];
  els.timeValue.textContent = timeOption.label;
  els.distanceValue.textContent = `${els.distanceRange.value} mi`;
  els.budgetValue.textContent = BUDGET_LABELS[Number(els.budgetRange.value)] || "$$";
}

function readControls() {
  state.city = els.city.value;
  state.maxMinutes = TIME_OPTIONS[Number(els.timeRange.value)]?.minutes || 120;
  state.maxDistance = Number(els.distanceRange.value);
  state.budget = Number(els.budgetRange.value);
  state.party = currentParty();
}

async function loadPlaces() {
  if (state.loading) return;
  readControls();
  state.loading = true;
  els.status.textContent = "Finding sidequests…";
  els.rejectButton.disabled = true;
  els.likeButton.disabled = true;
  els.refreshDeck.disabled = true;

  try {
    const params = new URLSearchParams({
      city: state.city,
      category: state.category,
      max_minutes: String(state.maxMinutes),
      max_distance: String(state.maxDistance),
      budget: String(state.budget),
      party: state.party,
      limit: "20"
    });

    const response = await fetch(`${BACKEND_URL}/places?${params.toString()}`);
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Could not load places.");
    }

    state.places = data.places || [];
    state.currentIndex = 0;

    const demoNote = data.source === "demo"
      ? " Demo mode is active — add GOOGLE_PLACES_API_KEY for live results."
      : "";

    els.status.textContent = `${state.places.length} sidequests loaded.${demoNote}`;
    renderCard(currentPlace());
  } catch (error) {
    state.places = [];
    state.currentIndex = 0;
    els.rejectButton.disabled = true;
    els.likeButton.disabled = true;

    const networkHelp = error instanceof TypeError
      ? `<div class="error-state">
          <strong>Frontend is running, but the backend is offline.</strong>
          Start Flask in a second Terminal, then reload this page.
          <code>cd ~/Downloads/sidequest-capstone-v2/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py</code>
          Then test <code>http://127.0.0.1:5000/health</code>
        </div>`
      : `<div class="error-state"><strong>Could not load Sidequests.</strong>${escapeHTML(error.message)}</div>`;

    els.deck.innerHTML = networkHelp;
    els.status.textContent = "Could not reach the Sidequest backend.";
  } finally {
    state.loading = false;
    els.refreshDeck.disabled = false;
  }
}

function storeUnique(listName, place) {
  const list = state[listName];
  if (!list.some((item) => item.id === place.id)) {
    list.unshift(place);
  }
}

function removeById(listName, id) {
  state[listName] = state[listName].filter((place) => place.id !== id);
}

function advanceCard() {
  state.currentIndex += 1;
  renderCard(currentPlace());
}

function logDecision(place, decision) {
  state.history.unshift({
    id: place.id,
    name: place.name,
    city_label: place.city_label,
    primary_type_label: place.primary_type_label,
    photo_names: place.photo_names,
    decision,
    swiped_at: new Date().toISOString()
  });
  state.history = state.history.slice(0, 100);
}

function swipe(direction) {
  const place = currentPlace();
  const card = document.querySelector("#activeCard");
  if (!place || !card) return;

  const liked = direction === "right";
  logDecision(place, liked ? "liked" : "passed");

  if (liked) storeUnique("saved", place);

  saveState();

  const exitX = direction === "right" ? window.innerWidth : -window.innerWidth;
  card.style.transform = `translate(${exitX}px, -10px) rotate(${direction === "right" ? 18 : -18}deg)`;
  card.style.opacity = "0";

  setTimeout(advanceCard, 220);
}

function attachSwipeGesture(card) {
  let startX = 0;
  let startY = 0;
  let currentX = 0;
  let currentY = 0;
  let dragging = false;
  let horizontalIntent = false;

  const nopeStamp = card.querySelector("#nopeStamp");
  const saveStamp = card.querySelector("#saveStamp");

  card.addEventListener("pointerdown", (event) => {
    if (event.target.closest("a, button, input, label")) return;
    dragging = true;
    horizontalIntent = false;
    startX = event.clientX;
    startY = event.clientY;
    currentX = 0;
    currentY = 0;
    card.classList.add("dragging");
  });

  card.addEventListener("pointermove", (event) => {
    if (!dragging) return;

    currentX = event.clientX - startX;
    currentY = event.clientY - startY;

    if (!horizontalIntent && Math.abs(currentX) > 8) {
      horizontalIntent = Math.abs(currentX) > Math.abs(currentY) * 1.25;
    }

    if (!horizontalIntent) return;

    const rotation = Math.max(-14, Math.min(14, currentX / 18));
    card.style.transform = `translateX(${currentX}px) rotate(${rotation}deg)`;

    const strength = Math.min(1, Math.abs(currentX) / 110);
    if (currentX > 0) {
      saveStamp.style.opacity = strength;
      nopeStamp.style.opacity = 0;
    } else {
      nopeStamp.style.opacity = strength;
      saveStamp.style.opacity = 0;
    }
  });

  const finish = () => {
    if (!dragging) return;
    dragging = false;
    card.classList.remove("dragging");

    if (horizontalIntent && Math.abs(currentX) >= 105) {
      swipe(currentX > 0 ? "right" : "left");
      return;
    }

    card.style.transform = "";
    nopeStamp.style.opacity = 0;
    saveStamp.style.opacity = 0;
  };

  card.addEventListener("pointerup", finish);
  card.addEventListener("pointercancel", finish);
}

function collectionCard(place, completed = false) {
  const photoName = firstPhoto(place);
  const image = photoName
    ? `<img src="${escapeHTML(photoURL(photoName))}" alt="${escapeHTML(place.name)}">`
    : `<div class="image-placeholder"></div>`;

  return `
    <article class="saved-card">
      ${image}
      <div class="saved-body">
        <h3>${escapeHTML(place.name)}</h3>
        <p>${escapeHTML(place.city_label || "")} · ${escapeHTML(categoryLabel(place))}</p>
        <div class="saved-actions">
          <a class="small-button" href="${escapeHTML(place.maps_url || "#")}" target="_blank" rel="noopener">Maps ↗</a>
          ${completed
            ? `<button class="small-button" data-action="uncomplete" data-id="${escapeHTML(place.id)}">Undo complete</button>`
            : `<button class="small-button primary" data-action="complete" data-id="${escapeHTML(place.id)}">✓ Complete</button>
               <button class="small-button" data-action="remove" data-id="${escapeHTML(place.id)}">Remove</button>`}
        </div>
      </div>
    </article>
  `;
}

function renderSaved() {
  if (!state.saved.length) {
    els.savedGrid.innerHTML = `<div class="empty-state">Bookmark a quest or swipe right and it will appear here.</div>`;
    return;
  }
  els.savedGrid.innerHTML = state.saved.map((place) => collectionCard(place, false)).join("");
}

function renderCompleted() {
  if (!state.completed.length) {
    els.completedGrid.innerHTML = `<div class="empty-state">Finish a quest and log it here.</div>`;
    return;
  }
  els.completedGrid.innerHTML = state.completed.map((place) => collectionCard(place, true)).join("");
}

function renderHistory() {
  if (!state.history.length) {
    els.historyList.innerHTML = `<div class="empty-state">Your swipes will appear here.</div>`;
    return;
  }

  els.historyList.innerHTML = state.history.map((item) => `
    <article class="history-item">
      <div class="history-icon">${item.decision === "liked" ? "♥" : "✕"}</div>
      <div>
        <h3>${escapeHTML(item.name)}</h3>
        <p>${escapeHTML(item.city_label || "")} · ${item.decision === "liked" ? "Saved" : "Passed"}</p>
      </div>
      ${item.decision === "passed"
        ? `<button class="small-button" data-action="restore" data-id="${escapeHTML(item.id)}">Restore</button>`
        : ""}
    </article>
  `).join("");
}

function setView(name) {
  els.tabs.forEach((tab) => tab.classList.toggle("active", tab.dataset.view === name));
  els.views.forEach((view) => view.classList.toggle("active", view.id === `${name}View`));

  if (name === "saved") renderSaved();
  if (name === "completed") renderCompleted();
  if (name === "history") renderHistory();
}

function completePlace(place, advance = false) {
  storeUnique("completed", place);
  removeById("saved", place.id);
  saveState();
  if (advance) advanceCard();
}

els.timeRange.addEventListener("input", syncControls);
els.distanceRange.addEventListener("input", syncControls);
els.budgetRange.addEventListener("input", syncControls);

els.categories.forEach((button) => {
  button.addEventListener("click", () => {
    els.categories.forEach((item) => item.classList.remove("active"));
    button.classList.add("active");
    state.category = button.dataset.category;
  });
});

els.refreshDeck.addEventListener("click", loadPlaces);
els.city.addEventListener("change", loadPlaces);

els.tabs.forEach((tab) => {
  tab.addEventListener("click", () => setView(tab.dataset.view));
});

els.rejectButton.addEventListener("click", () => swipe("left"));
els.likeButton.addEventListener("click", () => swipe("right"));

els.deck.addEventListener("click", (event) => {
  const place = currentPlace();
  if (!place) return;

  const photoAction = event.target.closest("[data-photo-action]");
  if (photoAction) {
    const count = Math.min((place.photo_names || []).length, 8);
    if (!count) return;
    if (photoAction.dataset.photoAction === "next") {
      state.photoIndex = (state.photoIndex + 1) % count;
    } else {
      state.photoIndex = (state.photoIndex - 1 + count) % count;
    }
    renderPhoto(place);
    return;
  }

  const photoDot = event.target.closest("[data-photo-index]");
  if (photoDot) {
    state.photoIndex = Number(photoDot.dataset.photoIndex);
    renderPhoto(place);
    return;
  }

  const action = event.target.closest("[data-card-action]")?.dataset.cardAction;
  if (action === "bookmark") {
    storeUnique("saved", place);
    saveState();
    event.target.textContent = "♥ Bookmarked";
  }

  if (action === "complete") {
    completePlace(place, true);
  }
});

els.savedGrid.addEventListener("click", (event) => {
  const button = event.target.closest("button[data-action]");
  if (!button) return;

  const place = state.saved.find((item) => item.id === button.dataset.id);
  if (!place) return;

  if (button.dataset.action === "remove") {
    removeById("saved", place.id);
  }

  if (button.dataset.action === "complete") {
    completePlace(place, false);
  }

  saveState();
  renderSaved();
});

els.completedGrid.addEventListener("click", (event) => {
  const button = event.target.closest('button[data-action="uncomplete"]');
  if (!button) return;
  removeById("completed", button.dataset.id);
  saveState();
  renderCompleted();
});

els.historyList.addEventListener("click", (event) => {
  const button = event.target.closest('button[data-action="restore"]');
  if (!button) return;

  const place = state.places.find((item) => item.id === button.dataset.id);
  if (place) {
    storeUnique("saved", place);
    saveState();
    renderHistory();
  }
});

els.clearHistory.addEventListener("click", () => {
  state.history = [];
  saveState();
  renderHistory();
});

syncControls();
updateCounts();
loadPlaces();
