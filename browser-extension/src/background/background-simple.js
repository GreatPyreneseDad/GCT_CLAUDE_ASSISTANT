/**
 * Background service worker for the GCT Coherence Monitor extension
 * Using Chrome API directly without imports for Manifest V3 compatibility
 */

// Initialize extension
chrome.runtime.onInstalled.addListener(async (details) => {
  console.log('GCT Monitor installed:', details.reason);
  
  // Set default settings
  if (details.reason === 'install') {
    await chrome.storage.sync.set({
      enabled: true,
      apiEndpoint: 'http://localhost:5001',
      showFloatingWidget: true,
      autoAnalyze: true
    });
  }

  // Create context menu
  chrome.contextMenus.create({
    id: 'analyze-selection',
    title: 'Analyze coherence of selection',
    contexts: ['selection']
  });
});

// Handle context menu clicks
chrome.contextMenus.onClicked.addListener(async (info, tab) => {
  if (info.menuItemId === 'analyze-selection' && info.selectionText && tab?.id) {
    // Send selected text to content script for analysis
    await chrome.tabs.sendMessage(tab.id, {
      type: 'ANALYZE_SELECTION',
      text: info.selectionText
    });
  }
});

// Listen for messages from content scripts
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  switch (message.type) {
    case 'GET_SETTINGS':
      chrome.storage.sync.get().then(sendResponse);
      return true; // Will respond asynchronously
      
    case 'ANALYZE_WITH_API':
      // Forward to API for advanced analysis
      chrome.storage.sync.get(['apiEndpoint']).then(async (settings) => {
        try {
          const response = await fetch(`${settings.apiEndpoint}/api/analyze/text`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              text: message.text,
              context: message.context
            })
          });
          
          if (response.ok) {
            const data = await response.json();
            sendResponse(data);
          } else {
            sendResponse(null);
          }
        } catch (error) {
          console.error('API analysis failed:', error);
          sendResponse(null);
        }
      });
      return true; // Will respond asynchronously
      
    case 'UPDATE_BADGE':
      // Update extension badge with coherence score
      if (sender.tab?.id) {
        const score = Math.round(message.score * 100);
        chrome.action.setBadgeText({
          text: `${score}`,
          tabId: sender.tab.id
        });
        
        // Set badge color based on score
        let color = '#ef4444'; // Red
        if (score >= 80) color = '#10b981'; // Green
        else if (score >= 60) color = '#f59e0b'; // Yellow
        else if (score >= 40) color = '#f97316'; // Orange
        
        chrome.action.setBadgeBackgroundColor({
          color,
          tabId: sender.tab.id
        });
      }
      break;
  }
});

// Monitor active tab changes
chrome.tabs.onActivated.addListener(async (activeInfo) => {
  const tab = await chrome.tabs.get(activeInfo.tabId);
  
  // Check if we're on a supported LLM platform
  const supportedDomains = [
    'chat.openai.com',
    'claude.ai',
    'bard.google.com',
    'gemini.google.com',
    'poe.com',
    'perplexity.ai'
  ];
  
  const isSupported = tab.url && supportedDomains.some(domain => 
    new URL(tab.url).hostname.includes(domain)
  );
  
  // Update icon to indicate if monitoring is active
  // Note: Icon change removed since we don't have icon files yet
  console.log('Tab activated:', tab.url, 'Supported:', isSupported);
});