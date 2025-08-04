// Background script for Universal Chat Analyzer

// Store conversation data per tab
const conversationData = new Map();

// Listen for messages from content scripts
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  switch (request.type) {
    case 'logMessage':
      // Store message data for the tab
      if (!conversationData.has(sender.tab.id)) {
        conversationData.set(sender.tab.id, {
          messages: [],
          startTime: Date.now(),
          platform: request.platform || 'Unknown'
        });
      }
      
      const tabData = conversationData.get(sender.tab.id);
      tabData.messages.push(request.data);
      
      // Keep only last 1000 messages per tab to prevent memory issues
      if (tabData.messages.length > 1000) {
        tabData.messages = tabData.messages.slice(-1000);
      }
      
      // Calculate and send updated stats
      const stats = calculateStats(tabData);
      chrome.tabs.sendMessage(sender.tab.id, {
        type: 'statsUpdate',
        ...stats
      });
      break;
      
    case 'clearData':
      conversationData.delete(sender.tab.id);
      break;
      
    case 'exportData':
      const data = conversationData.get(sender.tab.id);
      if (data) {
        sendResponse({
          success: true,
          data: {
            ...data,
            exportTime: new Date().toISOString(),
            stats: calculateStats(data)
          }
        });
      } else {
        sendResponse({ success: false, error: 'No data available' });
      }
      break;
  }
  
  return true; // Keep message channel open for async responses
});

// Clean up data when tab is closed
chrome.tabs.onRemoved.addListener((tabId) => {
  conversationData.delete(tabId);
  chrome.storage.local.remove(`active_${tabId}`);
});

// Calculate statistics for a conversation
function calculateStats(tabData) {
  if (!tabData || !tabData.messages || tabData.messages.length === 0) {
    return {
      messageCount: 0,
      averageQuality: 0,
      participants: 0
    };
  }
  
  const messages = tabData.messages;
  const totalQuality = messages.reduce((sum, msg) => {
    return sum + (msg.analysis?.overall || 0);
  }, 0);
  
  const participants = new Set(messages.map(m => m.sender)).size;
  
  return {
    messageCount: messages.length,
    averageQuality: totalQuality / messages.length,
    participants: participants,
    duration: Date.now() - tabData.startTime
  };
}

// Extension installation/update
chrome.runtime.onInstalled.addListener((details) => {
  if (details.reason === 'install') {
    console.log('Universal Chat Analyzer installed');
    // Could open a welcome page here
  } else if (details.reason === 'update') {
    console.log('Universal Chat Analyzer updated');
  }
});