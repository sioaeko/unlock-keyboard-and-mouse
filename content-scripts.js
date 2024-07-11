// content-scripts.js
const extension = {
  hostname: location.hostname,
  storage: {
    data: {},
    website: {}
  },
  hid: {
    alt: false,
    ctrl: false,
    shift: false,
    keys: new Set(),
    wheel: 0,
    click: false,
    context: false
  }
};

function prevent(event) {
  if (!extension.storage.website.active) return;

  for (const [key, item] of Object.entries(extension.storage.website)) {
    if (typeof item !== 'object') continue;

    const sameKeys = extension.hid.keys.size === Object.keys(item.keys || {}).length &&
      [...extension.hid.keys].every(code => item.keys && item.keys[code]);

    if (sameKeys &&
      (item.shift === extension.hid.shift || item.shift === undefined) &&
      (item.ctrl === extension.hid.ctrl || item.ctrl === undefined) &&
      (item.alt === extension.hid.alt || item.alt === undefined) &&
      (item.click === extension.hid.click || item.click === undefined) &&
      (item.context === extension.hid.context || item.context === undefined) &&
      (item.wheel === extension.hid.wheel || item.wheel === undefined)) {
      event.stopPropagation();
      break;
    }
  }
}

function handleKeyEvent(event) {
  if (event.code === 'AltLeft' || event.code === 'AltRight') {
    extension.hid.alt = event.type === 'keydown';
  } else if (event.code === 'ControlLeft' || event.code === 'ControlRight') {
    extension.hid.ctrl = event.type === 'keydown';
  } else if (event.code === 'ShiftLeft' || event.code === 'ShiftRight') {
    extension.hid.shift = event.type === 'keydown';
  } else if (event.type === 'keydown') {
    extension.hid.keys.add(event.keyCode);
  } else if (event.type === 'keyup') {
    extension.hid.keys.delete(event.keyCode);
  }

  if (extension.storage.website.active &&
    extension.storage.website.search &&
    extension.hid.keys.has(70) &&
    !extension.hid.shift &&
    extension.hid.ctrl &&
    !extension.hid.alt) {
    event.stopPropagation();
  }

  prevent(event);

  if (event.type === 'keyup' && extension.hid.keys.size === 0) {
    extension.hid.alt = false;
    extension.hid.ctrl = false;
    extension.hid.shift = false;
  }
}

// Event listeners
['keydown', 'keypress', 'keyup'].forEach(eventType => {
  window.addEventListener(eventType, handleKeyEvent, true);
});

// ... (rest of the mouse and touch event listeners)

// Initialize
chrome.runtime.sendMessage('tab-connected', (response) => {
  extension.hostname = response;
  extension.storage.import(() => {
    if (extension.storage.get('websites/' + extension.hostname + '/separated')) {
      extension.storage.website = extension.storage.get('websites/' + extension.hostname);
    } else {
      extension.storage.website = extension.storage.get('global');
      extension.storage.website.active = extension.storage.get('websites/' + extension.hostname + '/active');
    }
  });
});
