/**
 * Export Google Docs tabs to the offline matplobblib.cv data layout.
 *
 * Output in Google Drive:
 *   cv-export-<timestamp>/
 *     manifest.json
 *     tickets/ticket-001-....md  (numbered theory tabs 1..48 only)
 *     assets/ticket-001__img-001--<hash>.png
 *
 * Resumable setup:
 *   1. Set EXPORT_PARENT_FOLDER_ID below.
 *   2. Confirm DOCUMENT_ID and choose BATCH_SIZE.
 *   3. Run startCvExport() once and authorize Docs/Drive access.
 *   4. Run continueCvExport() until the log reports completion.
 *   5. Download the output and copy its contents into matplobblib/cv/data/.
 *
 * The optional inspectDocumentJson_ helper requires the Advanced Docs service.
 * The production exporter uses only built-in Apps Script services:
 * DocumentApp, DriveApp, PropertiesService, and LockService.
 */

const CFG = {
  DOCUMENT_ID: '1d_njw2OubPsmc3V9h3maa4B40PPNPK4iqDKj1F51KRo',
  EXPORT_PARENT_FOLDER_ID: 'PUT_DRIVE_FOLDER_ID_HERE',
  EXPORT_FOLDER_NAME: 'cv-export',
  EXPORTER_VERSION: 'apps-script-tabs-md@1.4.0',
  BATCH_SIZE: 3,
  MAX_BATCH_RUNTIME_MS: 4 * 60 * 1000,
  EQUATION_MODE: 'safe-latex', // safe-latex | plain | placeholder
  FIRST_TICKET_NUMBER: 1,
  LAST_TICKET_NUMBER: 48,
  EXCLUDED_SERVICE_TABS: ['вопросы', 'практика'],
};

const CV_EXPORT_KEYS = {
  STATE: 'CV_EXPORT_STATE',
  // Manifest entries are stored separately so one property never contains
  // the full (potentially large) manifest.
  TICKET_PREFIX: 'CV_EXPORT_TICKET_',
  ASSET_PREFIX: 'CV_EXPORT_ASSET_',
  CHUNK_SUFFIX: '_CHUNK_',
};

/** Create a new export and process its first batch. */
function startCvExport() {
  return withCvExportLock_(() => {
    assertConfigured_();
    const doc = DocumentApp.openById(CFG.DOCUMENT_ID);
    const allTabs = flattenDocumentTabs_(doc);
    const flatTabs = selectTheoryTicketTabs_(allTabs);
    if (!flatTabs.length) {
      throw new Error('The document has no numbered theory tabs in range 1..48.');
    }

    const parentFolder = DriveApp.getFolderById(CFG.EXPORT_PARENT_FOLDER_ID);
    const exportRoot = parentFolder.createFolder(
      `${CFG.EXPORT_FOLDER_NAME}-${timestampCompact_()}`
    );
    const ticketsFolder = exportRoot.createFolder('tickets');
    const assetsFolder = exportRoot.createFolder('assets');
    const manifestFile = exportRoot.createFile(
      'manifest.json',
      '{}',
      MimeType.PLAIN_TEXT
    );

    const properties = PropertiesService.getScriptProperties();
    clearCvExportProperties_(properties);
    const now = new Date().toISOString();
    const state = {
      exporterVersion: CFG.EXPORTER_VERSION,
      documentId: CFG.DOCUMENT_ID,
      documentTitle: doc.getName(),
      exportFolderId: exportRoot.getId(),
      ticketsFolderId: ticketsFolder.getId(),
      assetsFolderId: assetsFolder.getId(),
      manifestFileId: manifestFile.getId(),
      currentTabIndex: 0,
      nextTabId: flatTabs[0].tabId,
      totalTabs: flatTabs.length,
      ticketEntryCount: 0,
      assetEntryCount: 0,
      complete: false,
      startedAtUtc: now,
      updatedAtUtc: now,
      lastError: '',
    };
    saveCvExportState_(properties, state);
    Logger.log(
      'Started CV export with %s theory tabs; skipped %s service/non-ticket tabs.',
      flatTabs.length,
      allTabs.length - flatTabs.length
    );
    Logger.log('Drive folder: %s', exportFolderUrl_(state));
    return runCvExportBatch_(properties, state, doc, flatTabs);
  });
}

/** Continue an existing export from its saved tab index. */
function continueCvExport() {
  return withCvExportLock_(() => {
    const properties = PropertiesService.getScriptProperties();
    const state = loadCvExportState_(properties);
    if (!state) {
      throw new Error('No CV export state found. Run startCvExport() first.');
    }
    assertCompatibleCvExportState_(state);
    if (state.complete) {
      // Re-sync the Drive snapshot in case the previous run saved the final
      // checkpoint but was interrupted while writing manifest.json.
      writeManifestFromState_(properties, state);
      logCvExportStatus_(state);
      return state;
    }

    const doc = DocumentApp.openById(state.documentId);
    const flatTabs = selectTheoryTicketTabs_(flattenDocumentTabs_(doc));
    return runCvExportBatch_(properties, state, doc, flatTabs);
  });
}

/** Clear the resumable checkpoint. Existing Drive export folders are retained. */
function resetCvExport() {
  return withCvExportLock_(() => {
    const properties = PropertiesService.getScriptProperties();
    const previous = loadCvExportState_(properties);
    clearCvExportProperties_(properties);
    Logger.log('CV export state cleared. Existing Drive files were not deleted.');
    if (previous && previous.exportFolderId) {
      Logger.log('Previous Drive folder: %s', exportFolderUrl_(previous));
    }
    return true;
  });
}

/** Log current progress and the Drive folder URL. */
function showCvExportStatus() {
  return withCvExportLock_(() => {
    const state = loadCvExportState_(PropertiesService.getScriptProperties());
    if (!state) {
      Logger.log('No CV export state found. Run startCvExport() first.');
      return null;
    }
    logCvExportStatus_(state);
    return state;
  });
}

/** Backward-compatible entry point: now starts only one resumable batch. */
function exportDocTabsToMarkdown() {
  Logger.log('exportDocTabsToMarkdown() now delegates to startCvExport().');
  return startCvExport();
}

function withCvExportLock_(callback) {
  const lock = LockService.getScriptLock();
  lock.waitLock(30 * 1000);
  try {
    return callback();
  } finally {
    lock.releaseLock();
  }
}

function flattenDocumentTabs_(doc) {
  const flatTabs = [];
  doc.getTabs().forEach((tab, index) => {
    collectTabs_(tab, [], flatTabs, index + 1);
  });
  return flatTabs;
}

function selectTheoryTicketTabs_(flatTabs) {
  const selected = [];
  const seenNumbers = {};

  flatTabs.forEach(tabInfo => {
    const ticketNumber = inferTicketNumber_(tabInfo.title);
    if (ticketNumber === null) return;
    if (seenNumbers[ticketNumber]) {
      throw new Error(
        `Duplicate theory ticket number ${ticketNumber}: ` +
        `${seenNumbers[ticketNumber]} and ${tabInfo.title}.`
      );
    }
    seenNumbers[ticketNumber] = tabInfo.title;
    tabInfo.ticketNumber = ticketNumber;
    selected.push(tabInfo);
  });

  selected.sort((left, right) => left.ticketNumber - right.ticketNumber);
  return selected;
}

function runCvExportBatch_(properties, state, doc, flatTabs) {
  const runStartedAt = Date.now();
  assertCompatibleCvExportState_(state);
  reconcileCvExportPosition_(state, flatTabs);
  state.documentTitle = doc.getName();
  state.totalTabs = flatTabs.length;
  state.complete = state.currentTabIndex >= state.totalTabs;
  state.updatedAtUtc = new Date().toISOString();
  saveCvExportState_(properties, state);
  writeManifestFromState_(properties, state);

  if (state.complete) {
    logCvExportStatus_(state);
    return state;
  }

  const ticketsFolder = DriveApp.getFolderById(state.ticketsFolderId);
  const assetsFolder = DriveApp.getFolderById(state.assetsFolderId);
  const assetRegistry = loadAssetRegistry_(properties);
  const knownAssetShas = {};
  Object.keys(assetRegistry).forEach(sha => {
    knownAssetShas[sha] = true;
  });

  const batchSize = Math.max(1, Math.floor(Number(CFG.BATCH_SIZE) || 1));
  const maxRuntimeMs = Math.max(
    60 * 1000,
    Number(CFG.MAX_BATCH_RUNTIME_MS) || 4 * 60 * 1000
  );
  let exportedThisRun = 0;

  try {
    while (
      state.currentTabIndex < flatTabs.length &&
      exportedThisRun < batchSize
    ) {
      const elapsedMs = Date.now() - runStartedAt;
      const estimatedNextTabMs = exportedThisRun > 0
        ? elapsedMs / exportedThisRun
        : 0;
      if (
        elapsedMs >= maxRuntimeMs ||
        (
          exportedThisRun > 0 &&
          elapsedMs + estimatedNextTabMs + 15 * 1000 >= maxRuntimeMs
        )
      ) {
        Logger.log(
          'Stopping this batch after %s ms to preserve the checkpoint.',
          elapsedMs
        );
        break;
      }

      const tabIndex = state.currentTabIndex;
      const tabInfo = flatTabs[tabIndex];
      const existingTicket = loadTicketEntry_(properties, tabIndex);
      if (existingTicket) {
        Logger.log(
          'Recovered saved tab %s: %s; advancing checkpoint.',
          tabIndex + 1,
          existingTicket.title || tabInfo.title
        );
        advanceCvExportState_(state, flatTabs, tabIndex);
        state.ticketEntryCount = Math.max(
          Number(state.ticketEntryCount) || 0,
          state.currentTabIndex
        );
        state.assetEntryCount = Object.keys(assetRegistry).length;
        state.updatedAtUtc = new Date().toISOString();
        saveCvExportState_(properties, state);
        continue;
      }

      const ticketMeta = exportOneTab_(
        tabInfo,
        ticketsFolder,
        assetsFolder,
        assetRegistry
      );

      Object.keys(assetRegistry).forEach(sha => {
        if (!knownAssetShas[sha]) {
          saveAssetEntry_(properties, sha, assetRegistry[sha]);
          knownAssetShas[sha] = true;
        }
      });
      saveTicketEntry_(properties, tabIndex, ticketMeta);

      advanceCvExportState_(state, flatTabs, tabIndex);
      state.ticketEntryCount = Math.max(
        Number(state.ticketEntryCount) || 0,
        state.currentTabIndex
      );
      state.assetEntryCount = Object.keys(assetRegistry).length;
      state.lastError = '';
      state.updatedAtUtc = new Date().toISOString();
      saveCvExportState_(properties, state);

      exportedThisRun += 1;
      Logger.log('Exported tab %s: %s', tabIndex + 1, tabInfo.title);
      Logger.log('Exported %s / %s', state.currentTabIndex, flatTabs.length);
    }
  } catch (error) {
    state.lastError = (error && error.stack
      ? String(error.stack)
      : String(error)).slice(0, 1500);
    state.updatedAtUtc = new Date().toISOString();
    saveCvExportState_(properties, state);
    try {
      writeManifestFromState_(properties, state);
    } catch (manifestError) {
      Logger.log('Could not update manifest after failure: %s', manifestError);
    }
    Logger.log('Batch failed after saved tab index %s.', state.currentTabIndex);
    logCvExportStatus_(state);
    throw error;
  }

  state.complete = state.currentTabIndex >= flatTabs.length;
  state.nextTabId = state.complete
    ? ''
    : flatTabs[state.currentTabIndex].tabId;
  state.updatedAtUtc = new Date().toISOString();
  saveCvExportState_(properties, state);
  writeManifestFromState_(properties, state);
  logCvExportStatus_(state);
  return state;
}

function advanceCvExportState_(state, flatTabs, completedTabIndex) {
  state.currentTabIndex = completedTabIndex + 1;
  state.nextTabId = state.currentTabIndex < flatTabs.length
    ? flatTabs[state.currentTabIndex].tabId
    : '';
}

function reconcileCvExportPosition_(state, flatTabs) {
  let index = Math.max(0, Math.floor(Number(state.currentTabIndex) || 0));
  if (
    state.nextTabId &&
    (!flatTabs[index] || flatTabs[index].tabId !== state.nextTabId)
  ) {
    const recoveredIndex = flatTabs.findIndex(
      tabInfo => tabInfo.tabId === state.nextTabId
    );
    if (recoveredIndex === -1) {
      throw new Error(
        'The next saved tab no longer exists. Restore the document or run resetCvExport() and startCvExport().'
      );
    }
    Logger.log(
      'Tab order changed; resumed saved tab id at index %s.',
      recoveredIndex
    );
    index = recoveredIndex;
  }
  state.currentTabIndex = Math.min(index, flatTabs.length);
}

function loadCvExportState_(properties) {
  const raw = properties.getProperty(CV_EXPORT_KEYS.STATE);
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch (error) {
    throw new Error('Saved CV export state is invalid JSON. Run resetCvExport().');
  }
}

function saveCvExportState_(properties, state) {
  properties.setProperty(CV_EXPORT_KEYS.STATE, JSON.stringify(state));
}

function assertCompatibleCvExportState_(state) {
  if (state.exporterVersion !== CFG.EXPORTER_VERSION) {
    throw new Error(
      `Saved export uses ${state.exporterVersion}; current exporter is ` +
      `${CFG.EXPORTER_VERSION}. Run resetCvExport() and startCvExport().`
    );
  }
}

function clearCvExportProperties_(properties) {
  const all = properties.getProperties();
  Object.keys(all).forEach(key => {
    if (key.indexOf('CV_EXPORT_') === 0) properties.deleteProperty(key);
  });
}

function ticketPropertyKey_(tabIndex) {
  return `${CV_EXPORT_KEYS.TICKET_PREFIX}${String(tabIndex).padStart(6, '0')}`;
}

function assetPropertyKey_(sha) {
  return `${CV_EXPORT_KEYS.ASSET_PREFIX}${sha}`;
}

function saveTicketEntry_(properties, tabIndex, ticketMeta) {
  setChunkedJsonProperty_(
    properties,
    ticketPropertyKey_(tabIndex),
    ticketMeta
  );
}

function loadTicketEntry_(properties, tabIndex) {
  return getChunkedJsonProperty_(properties, ticketPropertyKey_(tabIndex));
}

function saveAssetEntry_(properties, sha, assetMeta) {
  setChunkedJsonProperty_(properties, assetPropertyKey_(sha), assetMeta);
}

function setChunkedJsonProperty_(properties, baseKey, value) {
  if (properties.getProperty(baseKey) !== null) {
    deleteChunkedJsonProperty_(properties, baseKey);
  }
  const json = JSON.stringify(value);
  const chunkSize = 1800; // <= 7.2 KB even if every character uses 4 UTF-8 bytes.
  if (json.length <= chunkSize) {
    properties.setProperty(baseKey, json);
    return;
  }

  const chunks = [];
  for (let offset = 0; offset < json.length; offset += chunkSize) {
    chunks.push(json.slice(offset, offset + chunkSize));
  }
  properties.setProperty(
    baseKey,
    JSON.stringify({ chunked: true, count: chunks.length })
  );
  chunks.forEach((chunk, index) => {
    properties.setProperty(
      `${baseKey}${CV_EXPORT_KEYS.CHUNK_SUFFIX}${String(index).padStart(4, '0')}`,
      chunk
    );
  });
}

function getChunkedJsonProperty_(properties, baseKey) {
  const raw = properties.getProperty(baseKey);
  if (!raw) return null;
  let parsed;
  try {
    parsed = JSON.parse(raw);
  } catch (error) {
    throw new Error(`Invalid saved manifest entry: ${baseKey}`);
  }
  if (!parsed || parsed.chunked !== true) return parsed;

  const chunks = [];
  for (let index = 0; index < parsed.count; index++) {
    const chunk = properties.getProperty(
      `${baseKey}${CV_EXPORT_KEYS.CHUNK_SUFFIX}${String(index).padStart(4, '0')}`
    );
    if (chunk === null) {
      throw new Error(`Missing saved manifest chunk for ${baseKey}.`);
    }
    chunks.push(chunk);
  }
  return JSON.parse(chunks.join(''));
}

function deleteChunkedJsonProperty_(properties, baseKey) {
  const all = properties.getProperties();
  properties.deleteProperty(baseKey);
  const chunkPrefix = `${baseKey}${CV_EXPORT_KEYS.CHUNK_SUFFIX}`;
  Object.keys(all).forEach(key => {
    if (key.indexOf(chunkPrefix) === 0) properties.deleteProperty(key);
  });
}

function getChunkedJsonFromSnapshot_(snapshot, baseKey) {
  const raw = snapshot[baseKey];
  if (!raw) return null;
  const parsed = JSON.parse(raw);
  if (!parsed || parsed.chunked !== true) return parsed;

  const chunks = [];
  for (let index = 0; index < parsed.count; index++) {
    const key =
      `${baseKey}${CV_EXPORT_KEYS.CHUNK_SUFFIX}` +
      `${String(index).padStart(4, '0')}`;
    if (snapshot[key] === undefined) {
      throw new Error(`Missing saved manifest chunk for ${baseKey}.`);
    }
    chunks.push(snapshot[key]);
  }
  return JSON.parse(chunks.join(''));
}

function loadAssetRegistry_(properties) {
  const snapshot = properties.getProperties();
  const registry = {};
  const pattern = new RegExp(
    `^${CV_EXPORT_KEYS.ASSET_PREFIX}([0-9a-f]{64})$`
  );
  Object.keys(snapshot).forEach(key => {
    const match = key.match(pattern);
    if (!match) return;
    registry[match[1]] = getChunkedJsonFromSnapshot_(snapshot, key);
  });
  return registry;
}

function collectManifestEntries_(properties) {
  const snapshot = properties.getProperties();
  const ticketPattern = new RegExp(
    `^${CV_EXPORT_KEYS.TICKET_PREFIX}([0-9]{6})$`
  );
  const assetPattern = new RegExp(
    `^${CV_EXPORT_KEYS.ASSET_PREFIX}([0-9a-f]{64})$`
  );
  const tickets = [];
  const assets = [];

  Object.keys(snapshot).forEach(key => {
    let match = key.match(ticketPattern);
    if (match) {
      tickets.push({
        tabIndex: Number(match[1]),
        meta: getChunkedJsonFromSnapshot_(snapshot, key),
      });
      return;
    }
    match = key.match(assetPattern);
    if (match) {
      assets.push(getChunkedJsonFromSnapshot_(snapshot, key));
    }
  });

  tickets.sort((left, right) => left.tabIndex - right.tabIndex);
  assets.sort((left, right) =>
    String(left.path || '').localeCompare(String(right.path || ''))
  );
  return {
    tickets: tickets.map(item => item.meta),
    assets: assets,
  };
}

function writeManifestFromState_(properties, state) {
  const entries = collectManifestEntries_(properties);
  const manifest = {
    format_version: 1,
    source: {
      google_doc_id: state.documentId,
      google_doc_title: state.documentTitle,
      exported_at_utc: state.updatedAtUtc,
      exporter: state.exporterVersion,
    },
    package: {
      package: 'matplobblib.cv',
      data_package: 'matplobblib.cv.data',
      root: 'matplobblib/cv/data',
    },
    assets: entries.assets,
    tickets: entries.tickets,
  };
  DriveApp.getFileById(state.manifestFileId).setContent(
    JSON.stringify(manifest, null, 2)
  );
}

function exportFolderUrl_(state) {
  return `https://drive.google.com/drive/folders/${state.exportFolderId}`;
}

function logCvExportStatus_(state) {
  Logger.log('Exported %s / %s', state.currentTabIndex, state.totalTabs);
  Logger.log('Drive folder: %s', exportFolderUrl_(state));
  Logger.log(
    state.complete
      ? 'Export is complete.'
      : 'Export is not complete. Run continueCvExport() for the next batch.'
  );
  if (state.lastError) Logger.log('Last error: %s', state.lastError);
}

function assertConfigured_() {
  if (!CFG.DOCUMENT_ID || CFG.DOCUMENT_ID.indexOf('PUT_') === 0) {
    throw new Error('Set CFG.DOCUMENT_ID before running the exporter.');
  }
  if (
    !CFG.EXPORT_PARENT_FOLDER_ID ||
    CFG.EXPORT_PARENT_FOLDER_ID.indexOf('PUT_') === 0
  ) {
    throw new Error('Set CFG.EXPORT_PARENT_FOLDER_ID before running the exporter.');
  }
}

function collectTabs_(tab, titlePath, output, ordinal) {
  const title = safeTitle_(tab.getTitle() || `tab-${ordinal}`);
  const currentPath = titlePath.concat([title]);
  output.push({
    tab: tab,
    tabId: tab.getId(),
    title: title,
    titlePath: currentPath,
    nestingLevel: currentPath.length - 1,
  });

  const childTabs = tab.getChildTabs() || [];
  childTabs.forEach((child, index) => {
    collectTabs_(child, currentPath, output, index + 1);
  });
}

function exportOneTab_(
  tabInfo,
  ticketsFolder,
  assetsFolder,
  assetRegistry
) {
  const body = tabInfo.tab.asDocumentTab().getBody();
  const title = tabInfo.title;
  const slug = slugify_(title);
  const ticketNumber = tabInfo.ticketNumber !== undefined
    ? tabInfo.ticketNumber
    : inferTicketNumber_(title);
  if (ticketNumber === null) {
    throw new Error(`Refusing to export non-theory tab: ${title}`);
  }
  const ticketStem =
    `ticket-${String(ticketNumber).padStart(3, '0')}-${slug}`;
  const markdownPath = `tickets/${ticketStem}.md`;
  const context = {
    ticketNumber: ticketNumber,
    ticketStem: ticketStem,
    assetsFolder: assetsFolder,
    assetRegistry: assetRegistry,
    localImageCounter: 0,
    assetRefs: [],
  };

  const lines = [`# ${title}`, ''];
  for (let index = 0; index < body.getNumChildren(); index++) {
    const block = stringifyBlockElement_(body.getChild(index), context);
    if (block && block.trim()) {
      lines.push(block.trimEnd(), '');
    }
  }

  const markdown = lines.join('\n').replace(/\n{3,}/g, '\n\n');
  upsertTextFile_(
    ticketsFolder,
    `${ticketStem}.md`,
    markdown
  );

  return {
    number: ticketNumber,
    title: title,
    slug: slug,
    tab_id: tabInfo.tabId,
    nesting_level: tabInfo.nestingLevel,
    title_path: tabInfo.titlePath,
    path: markdownPath,
    short: firstMeaningfulParagraph_(markdown),
    keywords: extractKeywords_(title, markdown),
    assets: uniqueStrings_(context.assetRefs),
  };
}

function stringifyBlockElement_(element, context) {
  const type = element.getType();
  switch (type) {
    case DocumentApp.ElementType.PARAGRAPH:
      return stringifyParagraphLike_(element.asParagraph(), context, false);
    case DocumentApp.ElementType.LIST_ITEM:
      return stringifyParagraphLike_(element.asListItem(), context, true);
    case DocumentApp.ElementType.TABLE:
      return stringifyTable_(element.asTable(), context);
    case DocumentApp.ElementType.INLINE_IMAGE:
      return saveInlineImage_(element.asInlineImage(), context);
    case DocumentApp.ElementType.EQUATION:
      return stringifyEquation_(safeCast_(element, 'asEquation'));
    case DocumentApp.ElementType.TABLE_OF_CONTENTS:
      return '> [table of contents omitted]\n';
    case DocumentApp.ElementType.PAGE_BREAK:
      return '\n<!-- page-break -->\n';
    case DocumentApp.ElementType.HORIZONTAL_RULE:
      return '\n***\n';
    case DocumentApp.ElementType.UNSUPPORTED:
      return '<!-- unsupported element omitted -->';
    default:
      try {
        if (typeof element.getText === 'function') {
          return escapeMdText_(element.getText());
        }
      } catch (error) {
        // Keep exporting the rest of the tab.
      }
      return '<!-- unknown element omitted -->';
  }
}

function stringifyParagraphLike_(paragraph, context, isList) {
  const heading =
    (typeof paragraph.getHeading === 'function' && paragraph.getHeading()) ||
    null;
  const inline = stringifyContainerChildren_(paragraph, context).trim();
  if (!inline) return '';

  if (isList) {
    const level =
      typeof paragraph.getNestingLevel === 'function'
        ? paragraph.getNestingLevel()
        : 0;
    return `${'  '.repeat(level)}- ${inline}`;
  }

  const headingMap = {
    TITLE: '#',
    SUBTITLE: '##',
    HEADING1: '##',
    HEADING2: '###',
    HEADING3: '####',
    HEADING4: '#####',
    HEADING5: '######',
    HEADING6: '######',
  };
  const key = heading
    ? String(heading).replace('DocumentApp.ParagraphHeading.', '')
    : '';
  return headingMap[key] ? `${headingMap[key]} ${inline}` : inline;
}

function stringifyContainerChildren_(container, context) {
  const parts = [];
  const count =
    typeof container.getNumChildren === 'function'
      ? container.getNumChildren()
      : 0;

  for (let index = 0; index < count; index++) {
    const child = container.getChild(index);
    const type = child.getType();
    switch (type) {
      case DocumentApp.ElementType.TEXT:
        parts.push(escapeMdText_(child.asText().getText()));
        break;
      case DocumentApp.ElementType.INLINE_IMAGE:
        parts.push(saveInlineImage_(child.asInlineImage(), context));
        break;
      case DocumentApp.ElementType.EQUATION:
      case DocumentApp.ElementType.EQUATION_FUNCTION:
      case DocumentApp.ElementType.EQUATION_SYMBOL:
      case DocumentApp.ElementType.EQUATION_FUNCTION_ARGUMENT_SEPARATOR:
        parts.push(stringifyEquation_(child));
        break;
      case DocumentApp.ElementType.PAGE_BREAK:
        parts.push('\n<!-- page-break -->\n');
        break;
      default:
        try {
          if (typeof child.getText === 'function') {
            parts.push(escapeMdText_(child.getText()));
          }
        } catch (error) {
          // Unknown inline elements are omitted rather than aborting the export.
        }
    }
  }
  return parts.join('').replace(/[ \t]+\n/g, '\n').trim();
}

function stringifyEquation_(equation, modeOverride) {
  const mode = equationMode_(modeOverride);
  if (mode === 'placeholder') return '[formula]';

  if (mode === 'safe-latex') {
    const latex = collectEquationLatex_(equation).trim();
    if (
      !latex ||
      /fractext|pcap|pcup|subscript|superscript|Equation/i.test(latex)
    ) {
      return '[formula]';
    }
    return '$' + latex + '$';
  }

  const raw = collectEquationText_(equation).trim();
  if (!raw || raw.indexOf('[formula]') !== -1) return '[formula]';
  return escapePlainEquationMarkdown_(raw);
}

function equationMode_(modeOverride) {
  const requested = String(
    modeOverride || CFG.EQUATION_MODE || 'safe-latex'
  ).toLowerCase();
  if (requested === 'latex') return 'safe-latex';
  return ['safe-latex', 'plain', 'placeholder'].indexOf(requested) !== -1
    ? requested
    : 'safe-latex';
}

function collectEquationLatex_(element, depth) {
  const currentDepth = depth || 0;
  if (!element || currentDepth > 64) return '';

  try {
    const typeName = safeTypeName_(element).toUpperCase();
    if (typeName.indexOf('EQUATION_FUNCTION_ARGUMENT_SEPARATOR') !== -1) {
      return ',';
    }

    const count = safeChildCount_(element);
    const children = [];
    for (let index = 0; index < count; index++) {
      const child = safeGetChild_(element, index);
      const childText = child
        ? collectEquationLatex_(child, currentDepth + 1)
        : '';
      if (!childText) return '';
      children.push(childText);
    }

    const code = safeGetCode_(element).trim();
    if (children.length) {
      return formatSafeLatexStructure_(typeName, code, children) || '';
    }

    const text = safeGetText_(element).trim();
    if (text) return safeLatexEquationLeaf_(text);

    return safeLatexSymbolFromCode_(code);
  } catch (error) {
    return '';
  }
}

function formatSafeLatexStructure_(typeName, code, children) {
  const name = equationCodeName_(code);
  if (name === 'subscript') {
    return children.length >= 2
      ? children[0] + '_{' + children.slice(1).join('') + '}'
      : '';
  }
  if (name === 'superscript') {
    return children.length >= 2
      ? children[0] + '^{' + children.slice(1).join('') + '}'
      : '';
  }
  if (name === 'sbracelr' || name === 'bracelr') {
    return '\\left(' + children.join('') + '\\right)';
  }
  if (name === 'frac') {
    return children.length >= 2
      ? '\\frac{' + children[0] + '}{' + children.slice(1).join('') + '}'
      : '';
  }
  if (name === 'sqrt') {
    return children.length ? '\\sqrt{' + children.join('') + '}' : '';
  }
  if (name === 'text') {
    const value = children.join('');
    return /^[A-Za-z0-9 ]+$/.test(value)
      ? '\\mathrm{' + value.trim() + '}'
      : '';
  }

  const symbol = safeLatexSymbolFromCode_(code);
  if (symbol) return symbol + children.join('');
  if (!code && typeName.indexOf('EQUATION') !== -1) {
    return children.join('');
  }
  return '';
}

function safeLatexEquationLeaf_(value) {
  const text = String(value || '').replace(/\s+/g, ' ').trim();
  if (!text) return '';
  if (
    /fractext|pcap|pcup|subscript|superscript|Equation/i.test(text)
  ) {
    return '';
  }
  if (text.indexOf('\\') === 0) return safeLatexSymbolFromCode_(text);
  if (!/^[A-Za-z0-9+\-*/=<>()[\],.^_ ]+$/.test(text)) return '';
  return text;
}

function safeLatexSymbolFromCode_(code) {
  const value = String(code || '').trim();
  const symbols = {
    '≤': '\\leq ', '≥': '\\geq ', '≠': '\\neq ', '≈': '\\approx ',
    '→': '\\to ', '∞': '\\infty ', 'α': '\\alpha ', 'β': '\\beta ',
    'γ': '\\gamma ', 'δ': '\\delta ', 'Δ': '\\Delta ', 'θ': '\\theta ',
    'Θ': '\\Theta ', 'λ': '\\lambda ', 'μ': '\\mu ', 'σ': '\\sigma ',
    'Σ': '\\Sigma ', 'π': '\\pi ', '√': '\\sqrt ', '×': '\\times ',
    '·': '\\cdot ', '±': '\\pm ',
    '\\leq': '\\leq ', '\\geq': '\\geq ', '\\neq': '\\neq ',
    '\\approx': '\\approx ', '\\to': '\\to ',
    '\\rightarrow': '\\rightarrow ', '\\infty': '\\infty ',
    '\\alpha': '\\alpha ', '\\beta': '\\beta ', '\\gamma': '\\gamma ',
    '\\delta': '\\delta ', '\\Delta': '\\Delta ', '\\theta': '\\theta ',
    '\\Theta': '\\Theta ', '\\lambda': '\\lambda ', '\\mu': '\\mu ',
    '\\sigma': '\\sigma ', '\\Sigma': '\\Sigma ', '\\pi': '\\pi ',
    '\\times': '\\times ', '\\cdot': '\\cdot ', '\\pm': '\\pm ',
    '\\cap': '\\cap ', '\\cup': '\\cup ', '\\int': '\\int ',
    '\\sum': '\\sum ',
  };
  if (Object.prototype.hasOwnProperty.call(symbols, value)) {
    return symbols[value];
  }
  if (/^[+\-*/=<>()[\],.^_]+$/.test(value)) return value;
  return '';
}
function collectEquationText_(element, depth) {
  const currentDepth = depth || 0;
  if (!element || currentDepth > 64) return '[formula]';

  try {
    const typeName = safeTypeName_(element).toUpperCase();
    if (typeName.indexOf('EQUATION_FUNCTION_ARGUMENT_SEPARATOR') !== -1) {
      return ',';
    }

    const count = safeChildCount_(element);
    const children = [];
    for (let index = 0; index < count; index++) {
      const child = safeGetChild_(element, index);
      const childText = child
        ? collectEquationText_(child, currentDepth + 1)
        : '[formula]';
      if (!childText || childText.indexOf('[formula]') !== -1) {
        return '[formula]';
      }
      children.push(childText);
    }

    const code = safeGetCode_(element).trim();
    if (children.length) {
      const structured = formatPlainEquationStructure_(
        typeName,
        code,
        children
      );
      return structured === null ? '[formula]' : structured;
    }

    const text = safeGetText_(element).trim();
    if (text) return safePlainEquationLeaf_(text) || '[formula]';

    return plainEquationSymbolFromCode_(code) || '[formula]';
  } catch (error) {
    return '[formula]';
  }
}

function formatPlainEquationStructure_(typeName, code, children) {
  const name = equationCodeName_(code);
  if (name === 'subscript') {
    return children.length >= 2
      ? `${children[0]}_${children.slice(1).join('')}`
      : null;
  }
  if (name === 'superscript') {
    return children.length >= 2
      ? `${children[0]}^${children.slice(1).join('')}`
      : null;
  }
  if (name === 'sbracelr' || name === 'bracelr') {
    return `(${children.join('')})`;
  }
  if (name === 'frac') {
    return children.length >= 2
      ? `(${children[0]})/(${children.slice(1).join('')})`
      : null;
  }
  if (name === 'sqrt') {
    return children.length ? `√(${children.join('')})` : null;
  }

  const symbol = plainEquationSymbolFromCode_(code);
  if (symbol) return symbol + children.join('');
  if (!code && typeName.indexOf('EQUATION') !== -1) {
    return children.join('');
  }
  return null;
}

function equationCodeName_(code) {
  return String(code || '')
    .trim()
    .replace(/^\\+/, '')
    .toLowerCase();
}

function safePlainEquationLeaf_(value) {
  const text = String(value || '').replace(/\s+/g, ' ').trim();
  if (!text || /Equation(?:Function|Symbol)?/i.test(text)) return '';
  if (/\\(?:subscript|superscript|s?bracelr)/i.test(text)) return '';
  if (text.indexOf('\\') === 0) return plainEquationSymbolFromCode_(text);
  if (/[$`\r\n]/.test(text)) return '';
  return text;
}

function plainEquationSymbolFromCode_(code) {
  const value = String(code || '').trim();
  const symbols = {
    '\\alpha': 'α', '\\beta': 'β', '\\gamma': 'γ', '\\delta': 'δ',
    '\\Delta': 'Δ', '\\theta': 'θ', '\\Theta': 'Θ', '\\lambda': 'λ',
    '\\mu': 'μ', '\\sigma': 'σ', '\\Sigma': 'Σ', '\\pi': 'π',
    '\\leq': '≤', '\\geq': '≥', '\\neq': '≠', '\\approx': '≈',
    '\\to': '→', '\\rightarrow': '→', '\\infty': '∞',
    '\\times': '×', '\\cdot': '·', '\\pm': '±',
  };
  if (Object.prototype.hasOwnProperty.call(symbols, value)) {
    return symbols[value];
  }
  if (!value || value.indexOf('\\') !== -1) return '';
  if (/Equation(?:Function|Symbol)?/i.test(value)) return '';
  if (/[$`\r\n]/.test(value) || value.length > 80) return '';
  return value;
}

function escapePlainEquationMarkdown_(value) {
  return escapeMdText_(String(value || '')).replace(/\$/g, '\\$');
}

function stringifyTable_(table, context) {
  const rows = [];
  let maximumColumns = 0;
  for (let rowIndex = 0; rowIndex < table.getNumRows(); rowIndex++) {
    const row = table.getRow(rowIndex);
    const cells = [];
    for (let cellIndex = 0; cellIndex < row.getNumCells(); cellIndex++) {
      cells.push(stringifyTableCell_(row.getCell(cellIndex), context));
    }
    maximumColumns = Math.max(maximumColumns, cells.length);
    rows.push(cells);
  }
  if (!rows.length || !maximumColumns) return '';

  const simple = rows.every(row =>
    row.every(cell => !/\n/.test(cell) && !/<table/i.test(cell))
  );
  if (!simple) {
    const htmlRows = rows
      .map(row => {
        const cells = row.map(cell => `<td>${escapeHtml_(cell)}</td>`).join('');
        return `<tr>${cells}</tr>`;
      })
      .join('\n');
    return `<table>\n${htmlRows}\n</table>`;
  }

  const normalized = rows.map(row => {
    const copy = row.slice();
    while (copy.length < maximumColumns) copy.push('');
    return copy.map(cell => cell.replace(/\|/g, '\\|'));
  });
  const header = normalized[0];
  const separator = new Array(maximumColumns).fill('---');
  return [
    `| ${header.join(' | ')} |`,
    `| ${separator.join(' | ')} |`,
  ]
    .concat(normalized.slice(1).map(row => `| ${row.join(' | ')} |`))
    .join('\n');
}

function stringifyTableCell_(cell, context) {
  const count =
    typeof cell.getNumChildren === 'function' ? cell.getNumChildren() : 0;
  const parts = [];
  for (let index = 0; index < count; index++) {
    const child = cell.getChild(index);
    const type = child.getType();
    if (type === DocumentApp.ElementType.PARAGRAPH) {
      parts.push(stringifyParagraphLike_(child.asParagraph(), context, false));
    } else if (type === DocumentApp.ElementType.LIST_ITEM) {
      parts.push(stringifyParagraphLike_(child.asListItem(), context, true));
    } else if (type === DocumentApp.ElementType.TABLE) {
      parts.push('[nested table omitted]');
    } else {
      try {
        if (typeof child.getText === 'function') parts.push(child.getText());
      } catch (error) {
        // Continue with the remaining cell elements.
      }
    }
  }
  return parts.join('<br />').trim() || escapeMdText_(cell.getText() || '');
}

function saveInlineImage_(image, context) {
  const blob = image.getBlob();
  const bytes = blob.getBytes();
  const fullSha = sha256Hex_(bytes);
  const shortSha = fullSha.slice(0, 12);
  const mime = blob.getContentType() || 'image/png';
  const existing = context.assetRegistry[fullSha];
  if (existing) {
    context.assetRefs.push(existing.path);
    const existingAlt = escapeMdText_(
      existing.alt_title || existing.alt_description || 'image'
    );
    return `![${existingAlt}](${relativeAssetPath_(existing.path)})`;
  }

  context.localImageCounter += 1;
  const extension = extensionForMime_(mime);
  const filename =
    `${context.ticketStem}__img-` +
    `${String(context.localImageCounter).padStart(3, '0')}--` +
    `${shortSha}.${extension}`;
  createOrReuseBlobFile_(
    context.assetsFolder,
    blob,
    filename,
    bytes.length
  );

  const metadata = {
    path: `assets/${filename}`,
    sha256: fullSha,
    mime_type: mime,
    width_px: safeCall_(image, 'getWidth'),
    height_px: safeCall_(image, 'getHeight'),
    alt_title: safeCall_(image, 'getAltTitle') || '',
    alt_description: safeCall_(image, 'getAltDescription') || '',
    first_seen_ticket: context.ticketStem,
  };
  context.assetRegistry[fullSha] = metadata;
  context.assetRefs.push(metadata.path);
  const alt = escapeMdText_(
    metadata.alt_title || metadata.alt_description || 'image'
  );
  return `![${alt}](${relativeAssetPath_(metadata.path)})`;
}

function upsertTextFile_(folder, filename, content) {
  const matches = folder.getFilesByName(filename);
  if (!matches.hasNext()) {
    return folder.createFile(filename, content, MimeType.PLAIN_TEXT);
  }

  const file = matches.next();
  file.setContent(content);
  while (matches.hasNext()) matches.next().setTrashed(true);
  return file;
}

function createOrReuseBlobFile_(folder, blob, filename, expectedSize) {
  const matches = folder.getFilesByName(filename);
  let reusable = null;
  while (matches.hasNext()) {
    const file = matches.next();
    if (!reusable && Number(file.getSize()) === Number(expectedSize)) {
      reusable = file;
    } else {
      file.setTrashed(true);
    }
  }
  if (reusable) return reusable;

  blob.setName(filename);
  return folder.createFile(blob);
}

function relativeAssetPath_(assetPath) {
  return `../${assetPath}`;
}

function extensionForMime_(mime) {
  const extensions = {
    'image/png': 'png',
    'image/jpeg': 'jpg',
    'image/jpg': 'jpg',
    'image/gif': 'gif',
    'image/webp': 'webp',
    'image/svg+xml': 'svg',
    'image/bmp': 'bmp',
  };
  return extensions[mime] || 'bin';
}

function inferTicketNumber_(title) {
  const normalized = safeTitle_(title).toLowerCase();
  if (CFG.EXCLUDED_SERVICE_TABS.indexOf(normalized) !== -1) return null;

  const match = normalized.match(/^([0-9]+)(?=$|[\s.):—-])/);
  if (!match) return null;
  const number = Number(match[1]);
  if (
    number < CFG.FIRST_TICKET_NUMBER ||
    number > CFG.LAST_TICKET_NUMBER
  ) {
    return null;
  }
  return number;
}

/** Pure regression check for service-tab and ticket-range filtering. */
function testTheoryTicketTabFilter() {
  const cases = [
    ['Вопросы', null],
    ['Практика', null],
    ['Приложение', null],
    ['Билет 3', null],
    ['1', 1],
    ['2. История развития', 2],
    [' 48 — Современные тенденции', 48],
    ['49', null],
  ];

  cases.forEach(testCase => {
    const actual = inferTicketNumber_(testCase[0]);
    if (actual !== testCase[1]) {
      throw new Error(
        `Theory-tab filter failed for "${testCase[0]}": ` +
        `expected ${testCase[1]}, got ${actual}`
      );
    }
  });
  Logger.log('Theory ticket tab filter regression test passed.');
}

function firstMeaningfulParagraph_(markdown) {
  const blocks = markdown.split(/\n\s*\n/);
  for (let index = 0; index < blocks.length; index++) {
    const text = blocks[index]
      .replace(/^#+\s+/gm, '')
      .replace(/!\[[^\]]*\]\([^)]+\)/g, '')
      .replace(/\|/g, ' ')
      .trim();
    if (text && text.length > 30) return text.slice(0, 240);
  }
  return '';
}

function extractKeywords_(title, markdown) {
  const words = `${title}\n${markdown}`
    .toLowerCase()
    .replace(/[^a-zа-яё0-9+\-_/ ]/gi, ' ')
    .split(/\s+/)
    .filter(Boolean)
    .filter(word => word.length >= 4);
  return uniqueStrings_(words).slice(0, 20);
}

function uniqueStrings_(values) {
  const seen = {};
  const unique = [];
  values.forEach(value => {
    if (!seen[value]) {
      seen[value] = true;
      unique.push(value);
    }
  });
  return unique;
}

function slugify_(value) {
  const transliteration = {
    а: 'a', б: 'b', в: 'v', г: 'g', д: 'd', е: 'e', ё: 'e', ж: 'zh',
    з: 'z', и: 'i', й: 'y', к: 'k', л: 'l', м: 'm', н: 'n', о: 'o',
    п: 'p', р: 'r', с: 's', т: 't', у: 'u', ф: 'f', х: 'h', ц: 'ts',
    ч: 'ch', ш: 'sh', щ: 'sch', ъ: '', ы: 'y', ь: '', э: 'e', ю: 'yu',
    я: 'ya',
  };
  let output = String(value).trim().toLowerCase();
  output = output
    .split('')
    .map(character =>
      transliteration[character] !== undefined
        ? transliteration[character]
        : character
    )
    .join('');
  output = output
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .replace(/-{2,}/g, '-');
  return output || 'untitled';
}

function safeTitle_(value) {
  return String(value || '').replace(/\s+/g, ' ').trim();
}

function sha256Hex_(bytes) {
  const digest = Utilities.computeDigest(
    Utilities.DigestAlgorithm.SHA_256,
    bytes
  );
  return digest
    .map(byte => {
      const value = (byte < 0 ? byte + 256 : byte).toString(16);
      return value.length === 1 ? `0${value}` : value;
    })
    .join('');
}

function hasMethod_(object, methodName) {
  try {
    return Boolean(object) && typeof object[methodName] === 'function';
  } catch (error) {
    return false;
  }
}

function safeCast_(object, methodName) {
  if (!hasMethod_(object, methodName)) return object;
  try {
    return object[methodName]() || object;
  } catch (error) {
    return object;
  }
}

function safeGetText_(object) {
  if (!hasMethod_(object, 'getText')) return '';
  try {
    const value = object.getText();
    return value === null || value === undefined ? '' : String(value);
  } catch (error) {
    return '';
  }
}

function safeGetCode_(object) {
  if (!hasMethod_(object, 'getCode')) return '';
  try {
    const value = object.getCode();
    return value === null || value === undefined ? '' : String(value);
  } catch (error) {
    return '';
  }
}

function safeTypeName_(object) {
  if (!hasMethod_(object, 'getType')) return '';
  try {
    const value = object.getType();
    return value === null || value === undefined ? '' : String(value);
  } catch (error) {
    return '';
  }
}

function safeChildCount_(object) {
  if (!hasMethod_(object, 'getNumChildren')) return 0;
  try {
    const count = Number(object.getNumChildren());
    return isFinite(count) && count > 0 ? Math.floor(count) : 0;
  } catch (error) {
    return 0;
  }
}

function safeGetChild_(object, index) {
  if (!hasMethod_(object, 'getChild')) return null;
  try {
    return object.getChild(index) || null;
  } catch (error) {
    return null;
  }
}

function escapeMdText_(value) {
  return String(value || '')
    .replace(/\\/g, '\\\\')
    .replace(/([*_`[\]])/g, '\\$1')
    .replace(/\r/g, '')
    .replace(/\u000b/g, ' ');
}

function escapeHtml_(value) {
  return String(value || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

function safeCall_(object, methodName) {
  try {
    return typeof object[methodName] === 'function'
      ? object[methodName]()
      : null;
  } catch (error) {
    return null;
  }
}

function timestampCompact_() {
  return new Date().toISOString().replace(/[:.]/g, '-');
}

/**
 * Regression test for equation nodes that do not implement getText().
 * Run this function directly in Apps Script before testing a real document.
 */
function testEquationStringifier() {
  return testEquationStringifier_();
}

function testEquationStringifier_() {
  const textNode = value => ({
    getType: () => 'TEXT',
    getText: () => value,
  });
  const functionNode = (code, children) => ({
    getType: () => 'EQUATION_FUNCTION',
    getCode: () => code,
    getNumChildren: () => children.length,
    getChild: index => children[index],
  });
  const equationNode = children => ({
    getType: () => 'EQUATION',
    getNumChildren: () => children.length,
    getChild: index => children[index],
  });

  const subscript = functionNode(
    '\\subscript',
    [textNode('a'), textNode('b')]
  );
  const symbolWithoutGetText = {
    getType: () => 'EQUATION_SYMBOL',
    getCode: () => '≤',
  };
  const equation = equationNode([subscript, symbolWithoutGetText]);

  const collected = collectEquationText_(equation);
  if (collected !== 'a_b≤') {
    throw new Error('Unexpected equation test output: ' + collected);
  }

  const plain = stringifyEquation_(equation, 'plain');
  if (plain !== 'a\\_b≤' || plain.indexOf('$') !== -1) {
    throw new Error('Plain equations must not emit math delimiters: ' + plain);
  }
  if (plain.indexOf('\\subscript') !== -1) {
    throw new Error('Plain equations must not expose Google pseudo-LaTeX.');
  }
  if (stringifyEquation_(equation, 'placeholder') !== '[formula]') {
    throw new Error('Placeholder equation mode must always emit [formula].');
  }

  const latex = stringifyEquation_(equation, 'safe-latex');
  if (latex !== '$a_{b}\\leq$') {
    throw new Error('Unexpected safe LaTeX output: ' + latex);
  }

  const predicted = functionNode(
    '\\subscript',
    [textNode('B'), textNode('p')]
  );
  const groundTruth = functionNode(
    '\\subscript',
    [textNode('B'), textNode('gt')]
  );
  const intersection = equationNode([
    predicted,
    { getType: () => 'EQUATION_SYMBOL', getCode: () => '\\cap' },
    groundTruth,
  ]);
  const union = equationNode([
    predicted,
    { getType: () => 'EQUATION_SYMBOL', getCode: () => '\\cup' },
    groundTruth,
  ]);
  const areaOf = expression => equationNode([
    functionNode('\\text', [textNode('Area')]),
    textNode('('),
    expression,
    textNode(')'),
  ]);
  const iouEquation = equationNode([
    functionNode('\\text', [textNode('IoU')]),
    textNode('='),
    functionNode('\\frac', [areaOf(intersection), areaOf(union)]),
  ]);
  const iouLatex = stringifyEquation_(iouEquation, 'safe-latex');
  ['\\mathrm{IoU}', '\\frac', '\\mathrm{Area}', '\\cap', '\\cup']
    .forEach(token => {
      if (iouLatex.indexOf(token) === -1) {
        throw new Error('IoU safe LaTeX is missing ' + token + ': ' + iouLatex);
      }
    });
  if (/fractext|pcap|pcup|subscript|superscript/i.test(iouLatex)) {
    throw new Error('IoU safe LaTeX leaked an artifact: ' + iouLatex);
  }

  const unknownNode = {
    getType: () => 'FUTURE_EQUATION_NODE',
  };
  if (stringifyEquation_(unknownNode, 'safe-latex') !== '[formula]') {
    throw new Error('Unknown equation nodes must degrade to [formula].');
  }

  const throwingNode = {
    getType: () => { throw new Error('getType failed'); },
    getCode: () => { throw new Error('getCode failed'); },
    getText: () => { throw new Error('getText failed'); },
    getNumChildren: () => { throw new Error('getNumChildren failed'); },
  };
  if (collectEquationLatex_(throwingNode) !== '') {
    throw new Error('Throwing equation nodes must not emit LaTeX.');
  }

  Logger.log('Equation stringifier regression test passed: %s', iouLatex);
  return true;
}
/** Regression test for resumable state, sharded entries, and selective reset. */
function testCvExportCheckpoint() {
  return testCvExportCheckpoint_();
}

function testCvExportCheckpoint_() {
  const store = { UNRELATED_SETTING: 'keep-me' };
  const properties = {
    getProperty: key => Object.prototype.hasOwnProperty.call(store, key)
      ? store[key]
      : null,
    setProperty: (key, value) => {
      store[key] = String(value);
      return properties;
    },
    deleteProperty: key => {
      delete store[key];
      return properties;
    },
    getProperties: () => {
      const copy = {};
      Object.keys(store).forEach(key => { copy[key] = store[key]; });
      return copy;
    },
  };

  const state = {
    exporterVersion: CFG.EXPORTER_VERSION,
    exportFolderId: 'folder-id',
    currentTabIndex: 2,
  };
  saveCvExportState_(properties, state);
  if (loadCvExportState_(properties).currentTabIndex !== 2) {
    throw new Error('CV export state did not round-trip.');
  }

  const largeTicket = {
    number: 3,
    title: 'Билет ' + 'я'.repeat(5000),
    path: 'tickets/ticket-003.md',
    assets: [],
  };
  saveTicketEntry_(properties, 2, largeTicket);
  if (loadTicketEntry_(properties, 2).title !== largeTicket.title) {
    throw new Error('Chunked ticket metadata did not round-trip.');
  }

  const sha = 'a'.repeat(64);
  saveAssetEntry_(properties, sha, {
    path: 'assets/example.png',
    sha256: sha,
    mime_type: 'image/png',
  });
  const entries = collectManifestEntries_(properties);
  if (entries.tickets.length !== 1 || entries.assets.length !== 1) {
    throw new Error('Saved manifest entries were not collected correctly.');
  }

  clearCvExportProperties_(properties);
  if (store.UNRELATED_SETTING !== 'keep-me') {
    throw new Error('resetCvExport() must preserve unrelated properties.');
  }
  if (Object.keys(store).some(key => key.indexOf('CV_EXPORT_') === 0)) {
    throw new Error('CV export properties were not fully cleared.');
  }

  Logger.log('CV export checkpoint regression test passed.');
  return true;
}

/** Whole-document baseline for visual QA; not used for per-tab production data. */
function exportWholeDocumentMarkdownForQA_() {
  assertConfigured_();
  const file = DriveApp.getFileById(CFG.DOCUMENT_ID);
  const blob = file.getAs('text/markdown');
  const parent = DriveApp.getFolderById(CFG.EXPORT_PARENT_FOLDER_ID);
  parent.createFile(blob.setName('whole-document-qa.md'));
}

/** Requires Services -> Google Docs API -> ON. */
function inspectDocumentJson_() {
  const doc = Docs.Documents.get(CFG.DOCUMENT_ID, {
    includeTabsContent: true,
  });
  Logger.log(JSON.stringify((doc.tabs || []).slice(0, 2), null, 2));
}
