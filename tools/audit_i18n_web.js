#!/usr/bin/env node
'use strict';

const fs = require('fs');

global.Node = {ELEMENT_NODE: 1, TEXT_NODE: 3, DOCUMENT_NODE: 9};
global.NodeFilter = {SHOW_ELEMENT: 1, SHOW_TEXT: 4};
global.document = {
  nodeType: Node.DOCUMENT_NODE,
  documentElement: {lang: 'it'},
  getElementById: () => null,
  createTreeWalker: () => ({nextNode: () => null}),
};
global.window = {dispatchEvent: () => {}};
global.CustomEvent = class {
  constructor(name, options) { this.name = name; this.detail = options?.detail; }
};
global.localStorage = {getItem: () => null, setItem: () => {}};
Object.defineProperty(global, 'navigator', {value: {language: 'it'}, configurable: true});
global.fetch = async path => ({
  ok: true,
  json: async () => JSON.parse(fs.readFileSync(path, 'utf8')),
});

require('../i18n_web.js');

(async () => {
  await window.NFTI18n.setLanguage('en');
  if (window.NFTI18n.translate('Mancano 5 secondi!') !== '5 seconds remaining!') {
    throw new Error('Template countdown EN non valido');
  }
  if (window.NFTI18n.translate('Pesce Drago') !== 'Fish Dragon') {
    throw new Error('Template oggetto EN non valido');
  }
  if (window.NFTI18n.entityId('Sword', 'item') !== 'item.spada') {
    throw new Error('Risoluzione ID entità EN non valida');
  }
  if (window.NFTI18n.entityName('item.spada', 'item') !== 'Sword') {
    throw new Error('Nome entità EN non valido');
  }
  if (window.NFTI18n.translate('Set del Abitante equipaggiato!') !== 'Resident set equipped!') {
    throw new Error('Frase scenica set EN non valida');
  }
  if (window.NFTI18n.translate('Mancano 5 secondi!\nSpada LV0') !== '5 seconds remaining!\nSword LV0') {
    throw new Error('Testo multilinea EN non valido');
  }
  if (window.NFTI18n.translate('=== VITTORIA ===') !== '=== VICTORY ===') {
    throw new Error('Template annidato EN non valido');
  }
  if (window.NFTI18n.translate('Libri') !== 'Books' || window.NFTI18n.translate('Effetto tecnico') !== 'Technical effect' || window.NFTI18n.translate('Ingrediente') !== 'Ingredient') {
    throw new Error('Etichette Wiki EN non valide');
  }
  await window.NFTI18n.setLanguage('es');
  if (window.NFTI18n.translate('Mancano 5 secondi!') !== '¡Quedan 5 segundos!') {
    throw new Error('Template countdown ES non valido');
  }
  if (window.NFTI18n.translate('Pesce Drago') !== 'Pez Dragón') {
    throw new Error('Template oggetto ES non valido');
  }
  if (window.NFTI18n.entityId('Espada', 'item') !== 'item.spada') {
    throw new Error('Risoluzione ID entità ES non valida');
  }
  if (window.NFTI18n.translate('Set del Abitante equipaggiato!') !== '¡Set de Habitante equipado!') {
    throw new Error('Frase scenica set ES non valida');
  }
  if (window.NFTI18n.translate('=== VITTORIA ===') !== '=== VICTORIA ===') {
    throw new Error('Template annidato ES non valido');
  }
  if (window.NFTI18n.translate('Libri') !== 'Libros' || window.NFTI18n.translate('Usabili') !== 'Objetos usables' || window.NFTI18n.translate('Pesce') !== 'Pez') {
    throw new Error('Etichette Wiki ES non valide');
  }
  console.log('Web i18n OK: template IT/EN/ES validi');
})().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
