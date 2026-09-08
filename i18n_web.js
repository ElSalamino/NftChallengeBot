/* Localizzazione condivisa da Wiki e Single Player Playtest. */
(() => {
  'use strict';

  const SUPPORTED = ['it', 'en', 'es'];
  const FALLBACK = 'it';
  const catalogues = {};
  const KIND_ALIASES = {
    items: 'item', rings: 'ring', sets: 'set', bosses: 'boss', enemies: 'enemy',
    locations: 'location', rooms: 'room', structures: 'structure', assault: 'structure',
    incantations: 'incantation', approaches: 'approach', nuclei: 'nucleus',
    events: 'event', modifiers: 'modifier', achievements: 'achievement',
    pets: 'pet', weathers: 'weather', choices: 'choice', roles: 'role',
    marine: 'marine_boss', marineboss: 'marine_boss', marine_bosses: 'marine_boss',
    scaglioni: 'scaglione',
  };
  const textState = new WeakMap();
  const attributeState = new WeakMap();
  let language = FALLBACK;
  let sourceIndex = new Map();
  let templates = [];
  let entities = {};
  let entitiesLoaded = false;
  let entityByName = new Map();
  let entityByKindName = new Map();
  let entityPattern = null;
  let entityPairs = new Map();

  function normalize(value) {
    const base = String(value || '').trim().toLowerCase().replace('_', '-').split('-', 1)[0];
    return SUPPORTED.includes(base) ? base : FALLBACK;
  }

  async function load(locale) {
    locale = normalize(locale);
    if (catalogues[locale]) return catalogues[locale];
    const response = await fetch(`locales/${locale}.json`);
    if (!response.ok) throw new Error(`Locale ${locale}: HTTP ${response.status}`);
    const raw = await response.json();
    catalogues[locale] = Object.fromEntries(
      Object.entries(raw).filter(([key]) => !key.startsWith('_'))
    );
    return catalogues[locale];
  }

  async function loadEntities() {
    if (entitiesLoaded) return entities;
    const response = await fetch('entities.json');
    if (!response.ok) throw new Error(`Entity registry: HTTP ${response.status}`);
    const raw = await response.json();
    entities = raw && typeof raw === 'object' ? (raw.entities || raw) : {};
    entitiesLoaded = true;
    return entities;
  }

  function normalizeKind(value) {
    if (value === undefined || value === null) return null;
    const raw = String(value).trim().toLowerCase().replaceAll(' ', '_');
    return KIND_ALIASES[raw] || raw;
  }

  function entityKinds(record) {
    const values = [record?.kind, ...(Array.isArray(record?.kinds) ? record.kinds : [])];
    return [...new Set(values.map(normalizeKind).filter(Boolean))];
  }

  function splitEntityLevel(value) {
    const text = String(value ?? '').trim();
    let match = /^([a-z][a-z0-9_]*\.[a-z0-9][a-z0-9-]*)(?:@lv(max|x|\d+))?$/i.exec(text);
    if (match) return {base: match[1], level: match[2]?.toUpperCase() || null};
    match = /^(.+?)\s+LV(MAX|X|\d+)$/i.exec(text);
    if (match) return {base: match[1], level: match[2].toUpperCase()};
    return {base: text, level: null};
  }

  function withEntityLevel(value, level, identifier = false) {
    if (!level) return value;
    return identifier ? `${value}@lv${level.toLowerCase()}` : `${value} LV${level.toUpperCase()}`;
  }

  function entityRecord(value, kind = null) {
    const {base} = splitEntityLevel(value);
    const wanted = normalizeKind(kind);
    if (entities[base] && (!wanted || entityKinds(entities[base]).includes(wanted))) {
      return [base, entities[base]];
    }
    const folded = base.toLocaleLowerCase();
    const exact = wanted ? entityByKindName.get(`${wanted}\u0000${folded}`) : null;
    if (exact && entities[exact]) return [exact, entities[exact]];
    const matches = [...new Set(entityByName.get(folded) || [])].filter(id => (
      !wanted || entityKinds(entities[id]).includes(wanted)
    ));
    return matches.length === 1 ? [matches[0], entities[matches[0]]] : [null, null];
  }

  function entityId(value, kind = null) {
    const {level} = splitEntityLevel(value);
    const [id] = entityRecord(value, kind);
    return id ? withEntityLevel(id, level, true) : String(value ?? '');
  }

  function legacyEntityName(value, kind = null) {
    const {level} = splitEntityLevel(value);
    const [, record] = entityRecord(value, kind);
    if (!record) return String(value ?? '');
    const shown = record.legacy_name || record.names?.it || String(value ?? '');
    return withEntityLevel(shown, level);
  }

  function entityName(value, kind = null, locale = language) {
    const {level} = splitEntityLevel(value);
    const [, record] = entityRecord(value, kind);
    if (!record) return String(value ?? '');
    locale = normalize(locale);
    const shown = record.names?.[locale] || record.names?.it || record.legacy_name || String(value ?? '');
    return withEntityLevel(shown, level);
  }

  function entitySearch(value, kind = null) {
    const [id, record] = entityRecord(value, kind);
    if (!record) return String(value ?? '');
    return [id, record.legacy_name, ...Object.values(record.names || {})].filter(Boolean).join(' ');
  }

  function regexEscape(value) {
    return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  function compileTemplate(source, target) {
    const fields = [];
    let cursor = 0;
    let pattern = '^';
    const placeholder = /\{([^{}]+)\}/g;
    let match;
    while ((match = placeholder.exec(source))) {
      pattern += regexEscape(source.slice(cursor, match.index)) + '([\\s\\S]*?)';
      fields.push(match[1]);
      cursor = match.index + match[0].length;
    }
    if (!fields.length) return null;
    pattern += regexEscape(source.slice(cursor)) + '$';
    try {
      return {regex: new RegExp(pattern), fields, target, weight: source.length};
    } catch (_) {
      return null;
    }
  }

  function rebuildIndexes() {
    const italian = catalogues.it || {};
    const target = catalogues[language] || italian;
    sourceIndex = new Map();
    templates = [];
    for (const [key, source] of Object.entries(italian)) {
      const translated = target[key] || source;
      sourceIndex.set(source, translated);
      const compiled = compileTemplate(source, translated);
      if (compiled) templates.push(compiled);
    }
    templates.sort((a, b) => b.weight - a.weight);

    entityByName = new Map();
    entityByKindName = new Map();
    const replacement = new Map();
    for (const [id, record] of Object.entries(entities)) {
      const variants = new Set([
        record.legacy_name,
        ...Object.values(record.names || {}),
        ...(Array.isArray(record.aliases) ? record.aliases : []),
      ].filter(Boolean));
      for (const value of variants) {
        const folded = String(value).toLocaleLowerCase();
        if (!entityByName.has(folded)) entityByName.set(folded, []);
        entityByName.get(folded).push(id);
        for (const kind of entityKinds(record)) {
          const key = `${kind}\u0000${folded}`;
          if (!entityByKindName.has(key)) entityByKindName.set(key, id);
        }
      }
      const source = record.legacy_name || record.names?.it;
      const translated = record.names?.[language] || record.names?.it || source;
      if (source && translated && source !== translated && !replacement.has(source)) {
        replacement.set(source, translated);
      }
    }
    entityPairs = replacement;
    const choices = [...replacement.keys()].sort((a, b) => b.length - a.length);
    entityPattern = choices.length
      ? new RegExp(`(?<![\\w.])(?:${choices.map(regexEscape).join('|')})(?![\\w-])`, 'gu')
      : null;
  }

  function renderTemplate(template, fields, values) {
    const byName = new Map(fields.map((field, index) => [field, translateCore(values[index] || '')]));
    return template.replace(/\{([^{}]+)\}/g, (_, field) => byName.get(field) ?? `{${field}}`);
  }

  function translateCore(source) {
    if (!source) return source;
    const directEntity = entityName(source);
    if (directEntity !== source) return directEntity;
    if (language === FALLBACK) return source;
    const equipped = /^Set (?:del|della|dell'|dei|degli|delle)\s*(.+?) equipaggiato!$/i.exec(source);
    if (equipped) {
      const id = entityId(equipped[1], 'set');
      if (id !== equipped[1]) {
        const shown = entityName(id, 'set');
        return language === 'en' ? `${shown} set equipped!` : `¡Set de ${shown} equipado!`;
      }
    }
    const exact = sourceIndex.get(source);
    if (exact !== undefined) return translateEntityNames(exact);
    for (const template of templates) {
      const match = template.regex.exec(source);
      if (match) return translateEntityNames(renderTemplate(template.target, template.fields, match.slice(1)));
    }
    return translateEntityNames(source);
  }

  function translateEntityNames(source) {
    if (!entityPattern || !source) return source;
    entityPattern.lastIndex = 0;
    return source.replace(entityPattern, match => entityPairs.get(match) || match);
  }

  function translateLine(source) {
    const leading = source.match(/^\s*/)?.[0] || '';
    const trailing = source.match(/\s*$/)?.[0] || '';
    const end = trailing ? source.length - trailing.length : source.length;
    return leading + translateCore(source.slice(leading.length, end)) + trailing;
  }

  function translate(source) {
    source = String(source ?? '');
    return source
      .split(/(\r\n|\r|\n)/)
      .map(part => /^(\r\n|\r|\n)$/.test(part) ? part : translateLine(part))
      .join('');
  }

  function skipped(node) {
    const parent = node.nodeType === Node.ELEMENT_NODE ? node : node.parentElement;
    return Boolean(parent && parent.closest('script,style,[data-i18n-skip]'));
  }

  function translateTextNode(node) {
    if (!node.nodeValue || skipped(node)) return;
    let state = textState.get(node);
    if (!state || node.nodeValue !== state.rendered) state = {source: node.nodeValue, rendered: node.nodeValue};
    const rendered = translate(state.source);
    textState.set(node, {source: state.source, rendered});
    if (node.nodeValue !== rendered) node.nodeValue = rendered;
  }

  function translateAttributes(element) {
    if (skipped(element)) return;
    const names = ['alt', 'placeholder', 'title', 'aria-label'];
    const state = attributeState.get(element) || {};
    for (const name of names) {
      if (!element.hasAttribute(name)) continue;
      const current = element.getAttribute(name) || '';
      const previous = state[name];
      const source = !previous || current !== previous.rendered ? current : previous.source;
      const rendered = translate(source);
      state[name] = {source, rendered};
      if (current !== rendered) element.setAttribute(name, rendered);
    }
    attributeState.set(element, state);
  }

  function apply(root = document) {
    if (root.nodeType === Node.TEXT_NODE) {
      translateTextNode(root);
      return;
    }
    if (root.nodeType !== Node.ELEMENT_NODE && root.nodeType !== Node.DOCUMENT_NODE) return;
    if (root.nodeType === Node.ELEMENT_NODE) translateAttributes(root);
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT);
    let node;
    while ((node = walker.nextNode())) {
      if (node.nodeType === Node.TEXT_NODE) translateTextNode(node);
      else translateAttributes(node);
    }
    document.documentElement.lang = language;
  }

  async function setLanguage(next) {
    language = normalize(next);
    await Promise.all([load(FALLBACK), load(language), loadEntities()]);
    rebuildIndexes();
    localStorage.setItem('nft-language', language);
    const selector = document.getElementById('languageSelect');
    if (selector) selector.value = language;
    apply(document);
    window.dispatchEvent(new CustomEvent('nftlanguagechange', {detail: {language}}));
  }

  async function init() {
    language = normalize(localStorage.getItem('nft-language') || navigator.language);
    await setLanguage(language);
    const selector = document.getElementById('languageSelect');
    if (selector) selector.onchange = () => setLanguage(selector.value);
    new MutationObserver(records => {
      for (const record of records) {
        if (record.type === 'characterData') translateTextNode(record.target);
        for (const node of record.addedNodes) apply(node);
      }
    }).observe(document.body, {subtree: true, childList: true, characterData: true});
    return language;
  }

  window.NFTI18n = {
    apply, entityId, entityName, entitySearch, init, legacyEntityName, loadEntities,
    normalize, setLanguage, translate, get language() { return language; },
  };
})();
