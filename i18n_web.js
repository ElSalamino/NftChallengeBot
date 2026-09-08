/* Localizzazione condivisa da Wiki e Single Player Playtest. */
(() => {
  'use strict';

  const SUPPORTED = ['it', 'en', 'es'];
  const FALLBACK = 'it';
  const catalogues = {};
  const textState = new WeakMap();
  const attributeState = new WeakMap();
  let language = FALLBACK;
  let sourceIndex = new Map();
  let templates = [];

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
  }

  function renderTemplate(template, fields, values) {
    const byName = new Map(fields.map((field, index) => [field, translateCore(values[index] || '')]));
    return template.replace(/\{([^{}]+)\}/g, (_, field) => byName.get(field) ?? `{${field}}`);
  }

  function translateCore(source) {
    if (language === FALLBACK || !source) return source;
    const exact = sourceIndex.get(source);
    if (exact !== undefined) return exact;
    for (const template of templates) {
      const match = template.regex.exec(source);
      if (match) return renderTemplate(template.target, template.fields, match.slice(1));
    }
    return source;
  }

  function translate(source) {
    source = String(source ?? '');
    const leading = source.match(/^\s*/)?.[0] || '';
    const trailing = source.match(/\s*$/)?.[0] || '';
    const end = trailing ? source.length - trailing.length : source.length;
    return leading + translateCore(source.slice(leading.length, end)) + trailing;
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
    await Promise.all([load(FALLBACK), load(language)]);
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

  window.NFTI18n = {apply, init, normalize, setLanguage, translate, get language() { return language; }};
})();
