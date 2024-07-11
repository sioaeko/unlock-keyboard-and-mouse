// background.js
const hostnameCache = new Map();

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message === 'tab-connected') {
    const hostname = getHostname(sender.url);
    hostnameCache.set(sender.tab.id, hostname);
    sendResponse(hostname);
    return true; // Indicates that the response is sent asynchronously
  } else if (message === 'options-page-connected') {
    sendResponse({
      isTab: sender.tab !== undefined
    });
    return false; // Indicates that the response is sent synchronously
  }
});

chrome.tabs.onRemoved.addListener((tabId) => {
  hostnameCache.delete(tabId);
});

function getHostname(url) {
  return new URL(url).hostname;
}

// Periodic cleanup of hostname cache
setInterval(() => {
  chrome.tabs.query({}, (tabs) => {
    const activeTabIds = new Set(tabs.map(tab => tab.id));
    for (const [tabId] of hostnameCache) {
      if (!activeTabIds.has(tabId)) {
        hostnameCache.delete(tabId);
      }
    }
  });
}, 30 * 60 * 1000); // Run every 30 minutes
