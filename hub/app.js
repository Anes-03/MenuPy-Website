const state = {
  scripts: [],
  query: '',
  activeCategories: new Set(),
};

const elements = {
  searchInput: document.getElementById('searchInput'),
  categoryFilters: document.getElementById('categoryFilters'),
  scriptsGrid: document.getElementById('scriptsGrid'),
  resultsCount: document.getElementById('resultsCount'),
  listView: document.getElementById('listView'),
  detailView: document.getElementById('detailView'),
  backButton: document.getElementById('backButton'),
  detailTitle: document.getElementById('detailTitle'),
  detailCategory: document.getElementById('detailCategory'),
  detailDescription: document.getElementById('detailDescription'),
  detailMeta: document.getElementById('detailMeta'),
  detailCode: document.getElementById('detailCode'),
  copyButton: document.getElementById('copyButton'),
  downloadButton: document.getElementById('downloadButton'),
};

const normalize = (value) => value.toLowerCase();

const matchesQuery = (script, query) => {
  if (!query) return true;
  const haystack = [
    script.name,
    script.description,
    script.category,
    ...(script.tags || []),
  ]
    .join(' ')
    .toLowerCase();
  return haystack.includes(query);
};

const matchesCategory = (script) => {
  if (state.activeCategories.size === 0) return true;
  return state.activeCategories.has(script.category);
};

const filteredScripts = () =>
  state.scripts.filter(
    (script) => matchesQuery(script, state.query) && matchesCategory(script)
  );

const renderCategories = () => {
  const categories = Array.from(
    new Set(state.scripts.map((script) => script.category))
  ).sort();

  elements.categoryFilters.innerHTML = '';

  const allChip = document.createElement('button');
  allChip.className = 'chip';
  allChip.textContent = 'Alle';
  allChip.addEventListener('click', () => {
    state.activeCategories.clear();
    renderCategories();
    renderList();
  });
  if (state.activeCategories.size === 0) {
    allChip.classList.add('active');
  }
  elements.categoryFilters.appendChild(allChip);

  categories.forEach((category) => {
    const chip = document.createElement('button');
    chip.className = 'chip';
    chip.textContent = category;
    if (state.activeCategories.has(category)) {
      chip.classList.add('active');
    }
    chip.addEventListener('click', () => {
      if (state.activeCategories.has(category)) {
        state.activeCategories.delete(category);
      } else {
        state.activeCategories.add(category);
      }
      renderCategories();
      renderList();
    });
    elements.categoryFilters.appendChild(chip);
  });
};

const renderList = () => {
  const scripts = filteredScripts();
  elements.scriptsGrid.innerHTML = '';
  elements.resultsCount.textContent = `${scripts.length} Skripte gefunden`;

  if (scripts.length === 0) {
    const empty = document.createElement('p');
    empty.textContent = 'Keine Skripte gefunden. Probiere eine andere Suche.';
    empty.className = 'subtitle';
    elements.scriptsGrid.appendChild(empty);
    return;
  }

  scripts.forEach((script, index) => {
    const card = document.createElement('button');
    card.className = 'card';
    card.style.setProperty('--delay', `${index * 0.05}s`);
    card.addEventListener('click', () => openDetail(script.id));

    const title = document.createElement('h3');
    title.textContent = script.name;

    const desc = document.createElement('p');
    desc.textContent = script.description;

    const tagRow = document.createElement('div');
    tagRow.className = 'tag-row';

    const category = document.createElement('span');
    category.className = 'tag';
    category.textContent = script.category;
    tagRow.appendChild(category);

    (script.tags || []).slice(0, 3).forEach((tag) => {
      const tagEl = document.createElement('span');
      tagEl.className = 'tag';
      tagEl.textContent = tag;
      tagRow.appendChild(tagEl);
    });

    card.appendChild(title);
    card.appendChild(desc);
    card.appendChild(tagRow);
    elements.scriptsGrid.appendChild(card);
  });
};

const renderMeta = (script) => {
  const metaItems = [
    { label: 'Kategorie', value: script.category },
    { label: 'Python', value: script.python_version },
    { label: 'Tags', value: (script.tags || []).join(', ') || '-' },
    {
      label: 'Abhaengigkeiten',
      value: (script.requires || []).join(', ') || 'Keine',
    },
  ];

  elements.detailMeta.innerHTML = '';
  metaItems.forEach((item) => {
    const el = document.createElement('div');
    el.className = 'meta-item';
    el.textContent = `${item.label}: ${item.value}`;
    elements.detailMeta.appendChild(el);
  });
};

const openDetail = (id) => {
  const script = state.scripts.find((entry) => entry.id === id);
  if (!script) return;

  elements.detailTitle.textContent = script.name;
  elements.detailCategory.textContent = script.category;
  elements.detailDescription.textContent = script.long_description || script.description;
  elements.detailCode.textContent = script.code;
  renderMeta(script);

  elements.downloadButton.href = 'hub/' + script.script_path;
  elements.downloadButton.download = script.script_path.split('/').pop();

  elements.copyButton.onclick = () => copyToClipboard(script.code);

  elements.listView.classList.add('hidden');
  elements.detailView.classList.remove('hidden');
  window.location.hash = script.id;
};

const closeDetail = () => {
  elements.detailView.classList.add('hidden');
  elements.listView.classList.remove('hidden');
  if (window.location.hash) {
    history.replaceState(null, '', window.location.pathname);
  }
};

const copyToClipboard = (text) => {
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(() => {
      elements.copyButton.textContent = 'Kopiert';
      setTimeout(() => (elements.copyButton.textContent = 'Code kopieren'), 1500);
    });
    return;
  }

  const textarea = document.createElement('textarea');
  textarea.value = text;
  textarea.style.position = 'fixed';
  textarea.style.opacity = '0';
  document.body.appendChild(textarea);
  textarea.focus();
  textarea.select();
  try {
    document.execCommand('copy');
    elements.copyButton.textContent = 'Kopiert';
    setTimeout(() => (elements.copyButton.textContent = 'Code kopieren'), 1500);
  } finally {
    document.body.removeChild(textarea);
  }
};

const handleHash = () => {
  const id = window.location.hash.replace('#', '').trim();
  if (id) {
    openDetail(id);
  }
};

const init = async () => {
  try {
    const response = await fetch('hub/data.json', { cache: 'no-store' });
    if (!response.ok) throw new Error('data.json nicht gefunden');
    state.scripts = await response.json();
    renderCategories();
    renderList();
    handleHash();
  } catch (error) {
    elements.resultsCount.textContent = 'Fehler beim Laden der Daten.';
    const errorMsg = document.createElement('p');
    errorMsg.className = 'subtitle';
    errorMsg.textContent =
      'Hinweis: Wenn du die Datei lokal oeffnest, starte einen kleinen Webserver.';
    elements.scriptsGrid.appendChild(errorMsg);
  }
};

window.addEventListener('hashchange', handleHash);

elements.searchInput.addEventListener('input', (event) => {
  state.query = normalize(event.target.value);
  renderList();
});

elements.backButton.addEventListener('click', closeDetail);

init();
