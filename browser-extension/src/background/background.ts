/**
 * Background service worker for the GCT Coherence Monitor extension
 */

import browser from 'webextension-polyfill';

// Initialize extension
browser.runtime.onInstalled.addListener(async (details) => {
  console.log('GCT Monitor installed:', details.reason);
  
  // Set default settings
  if (details.reason === 'install') {
    await browser.storage.sync.set({
      enabled: true,
      apiEndpoint: 'http://localhost:5001',
      showFloatingWidget: true,
      autoAnalyze: true
    });
  }

  // Create context menu
  browser.contextMenus.create({
    id: 'analyze-selection',
    title: 'Analyze coherence of selection',
    contexts: ['selection']
  });
});

// Handle context menu clicks
browser.contextMenus.onClicked.addListener(async (info, tab) => {
  if (info.menuItemId === 'analyze-selection' && info.selectionText && tab?.id) {
    // Send selected text to content script for analysis
    await browser.tabs.sendMessage(tab.id, {
      type: 'ANALYZE_SELECTION',
      text: info.selectionText
    });
  }
});

// Listen for messages from content scripts
browser.runtime.onMessage.addListener(async (message, sender) => {
  switch (message.type) {
    case 'GET_SETTINGS':
      return browser.storage.sync.get();
      
    case 'ANALYZE_WITH_API':
      // Forward to API for advanced analysis
      try {
        const settings = await browser.storage.sync.get(['apiEndpoint']);
        const response = await fetch(`${settings.apiEndpoint}/api/analyze/text`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            text: message.text,
            context: message.context
          })
        });
        
        if (response.ok) {
          return await response.json();
        }
      } catch (error) {
        console.error('API analysis failed:', error);
      }
      return null;
      
    case 'UPDATE_BADGE':
      // Update extension badge with coherence score
      if (sender.tab?.id) {
        const score = Math.round(message.score * 100);
        await browser.action.setBadgeText({
          text: `${score}`,
          tabId: sender.tab.id
        });
        
        // Set badge color based on score
        let color = '#ef4444'; // Red
        if (score >= 80) color = '#10b981'; // Green
        else if (score >= 60) color = '#f59e0b'; // Yellow
        else if (score >= 40) color = '#f97316'; // Orange
        
        await browser.action.setBadgeBackgroundColor({
          color,
          tabId: sender.tab.id
        });
      }
      break;
  }
});

// Monitor active tab changes
browser.tabs.onActivated.addListener(async (activeInfo) => {
  const tab = await browser.tabs.get(activeInfo.tabId);
  
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
    new URL(tab.url!).hostname.includes(domain)
  );
  
  // Update icon to indicate if monitoring is active
  if (isSupported) {
    await browser.action.setIcon({
      path: {
        16: 'icons/icon16-active.png',
        32: 'icons/icon32-active.png',
        48: 'icons/icon48-active.png',
        128: 'icons/icon128-active.png'
      }
    });
  } else {
    await browser.action.setIcon({
      path: {
        16: 'icons/icon16.png',
        32: 'icons/icon32.png',
        48: 'icons/icon48.png',
        128: 'icons/icon128.png'
      }
    });
  }
});

// Export for service worker
export {};