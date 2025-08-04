document.addEventListener('DOMContentLoaded', function() {
  const statusIndicator = document.getElementById('status-indicator');
  const statusText = document.getElementById('status-text');
  const toggleButton = document.getElementById('toggle-button');
  const metricsDiv = document.getElementById('metrics');
  const messageCount = document.getElementById('message-count');
  const avgQuality = document.getElementById('avg-quality');
  
  let isActive = false;
  let currentTab = null;

  // Check current status
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    currentTab = tabs[0];
    
    // Check if extension is active on this tab
    chrome.storage.local.get([`active_${currentTab.id}`], function(result) {
      isActive = result[`active_${currentTab.id}`] || false;
      updateUI();
    });
    
    // Check if this is a supported chat interface
    chrome.tabs.sendMessage(currentTab.id, {action: 'checkSupport'}, function(response) {
      if (chrome.runtime.lastError) {
        statusText.textContent = 'No chat interface detected';
        toggleButton.disabled = true;
        toggleButton.textContent = 'Not Available';
      } else if (response && response.supported) {
        statusText.textContent = `Detected: ${response.platform}`;
        toggleButton.disabled = false;
      } else {
        statusText.textContent = 'No chat interface detected';
        toggleButton.disabled = true;
        toggleButton.textContent = 'Not Available';
      }
    });
  });

  // Toggle button handler
  toggleButton.addEventListener('click', function() {
    isActive = !isActive;
    
    // Save state
    chrome.storage.local.set({[`active_${currentTab.id}`]: isActive});
    
    // Send message to content script
    chrome.tabs.sendMessage(currentTab.id, {
      action: 'toggle',
      enabled: isActive
    });
    
    updateUI();
  });

  // Update UI based on state
  function updateUI() {
    if (isActive) {
      statusIndicator.classList.add('active');
      statusIndicator.classList.remove('inactive');
      statusText.textContent = 'Analyzing conversations';
      toggleButton.textContent = 'Stop Analyzing';
      toggleButton.classList.add('stop');
      metricsDiv.style.display = 'grid';
      
      // Request current stats
      chrome.tabs.sendMessage(currentTab.id, {action: 'getStats'}, function(response) {
        if (response) {
          messageCount.textContent = response.messageCount || '0';
          avgQuality.textContent = response.averageQuality ? 
            `${Math.round(response.averageQuality * 100)}%` : '--%';
        }
      });
    } else {
      statusIndicator.classList.remove('active');
      statusIndicator.classList.add('inactive');
      statusText.textContent = 'Not analyzing';
      toggleButton.textContent = 'Start Analyzing';
      toggleButton.classList.remove('stop');
      metricsDiv.style.display = 'none';
    }
  }

  // Listen for updates from content script
  chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.type === 'statsUpdate' && sender.tab.id === currentTab.id) {
      messageCount.textContent = request.messageCount || '0';
      avgQuality.textContent = request.averageQuality ? 
        `${Math.round(request.averageQuality * 100)}%` : '--%';
    }
  });
});