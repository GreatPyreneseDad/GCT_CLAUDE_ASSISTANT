#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Files to preserve after build
const filesToPreserve = {
  'background.js': `/**
 * Background service worker for GCT Coherence Monitor
 * Simplified version without context menus to avoid permission issues
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
          const response = await fetch(\`\${settings.apiEndpoint}/api/analyze/text\`, {
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
          text: \`\${score}\`,
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
  try {
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
      tab.url.includes(domain)
    );
    
    console.log('Tab activated:', tab.url, 'Supported:', isSupported);
  } catch (error) {
    console.error('Failed to get tab info:', error);
  }
});

console.log('GCT Monitor background service worker loaded');`,
  'manifest.json': `{
  "manifest_version": 3,
  "name": "GCT Coherence Monitor",
  "version": "1.0.0",
  "description": "Real-time coherence evaluation for LLM outputs using Grounded Coherence Theory",
  
  "permissions": [
    "activeTab",
    "storage",
    "scripting",
    "tabs"
  ],
  
  "host_permissions": [
    "https://chat.openai.com/*",
    "https://claude.ai/*",
    "https://bard.google.com/*",
    "https://gemini.google.com/*",
    "https://poe.com/*",
    "https://perplexity.ai/*",
    "http://localhost:5001/*"
  ],
  
  "background": {
    "service_worker": "background.js"
  },
  
  "content_scripts": [
    {
      "matches": [
        "https://chat.openai.com/*",
        "https://claude.ai/*",
        "https://bard.google.com/*",
        "https://gemini.google.com/*",
        "https://poe.com/*",
        "https://perplexity.ai/*"
      ],
      "js": ["content.js"],
      "css": ["content.css"],
      "run_at": "document_idle"
    }
  ],
  
  "action": {
    "default_popup": "popup.html"
  }
}`
};

// Ensure files exist in dist
Object.entries(filesToPreserve).forEach(([filename, content]) => {
  const filepath = path.join(__dirname, '../dist', filename);
  fs.writeFileSync(filepath, content);
  console.log(`✓ Preserved ${filename}`);
});

// Fix popup.html script path
const popupPath = path.join(__dirname, '../dist/popup.html');
if (fs.existsSync(popupPath)) {
  let popupContent = fs.readFileSync(popupPath, 'utf8');
  popupContent = popupContent.replace(/src="[^"]*popup\.js"/, 'src="./popup.js"');
  fs.writeFileSync(popupPath, popupContent);
  console.log('✓ Fixed popup.html script path');
}

console.log('Post-build complete!');