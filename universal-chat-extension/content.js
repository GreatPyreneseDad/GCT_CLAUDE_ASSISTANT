/**
 * Universal Chat Coherence Analyzer
 * Detects and analyzes human conversations on any chat interface
 */

// Enhanced Coherence Analyzer for Human Conversations
class HumanConversationAnalyzer {
  constructor() {
    this.conversationHistory = [];
    this.participants = new Map();
    this.currentSession = {
      startTime: Date.now(),
      messages: [],
      turnTaking: [],
      responseLatencies: []
    };
  }

  analyzeMessage(text, sender, timestamp = Date.now()) {
    // Enhanced metrics for human conversation
    const metrics = {
      // Original GCT dimensions
      psi: this.calculateConsistency(text),
      rho: this.calculateContextualRelevance(text),
      q: this.calculateEngagement(text),
      f: this.calculateEmpathy(text),
      
      // Human conversation specific metrics
      clarity: this.calculateClarity(text),
      sentiment: this.analyzeSentiment(text),
      turnBalance: this.calculateTurnBalance(),
      responseTime: this.calculateResponseLatency(timestamp),
      topicCoherence: this.calculateTopicCoherence(text)
    };

    // Store message
    this.currentSession.messages.push({
      text,
      sender,
      timestamp,
      metrics
    });

    return {
      metrics,
      overall: this.calculateOverallScore(metrics),
      insights: this.generateInsights(metrics)
    };
  }

  calculateConsistency(text) {
    let score = 0.7;
    
    // Check for contradictions or backtracking
    const contradictionPatterns = [
      /actually no|wait no|never mind|forget what i said/gi,
      /i mean|or rather|what i meant was/gi
    ];
    
    contradictionPatterns.forEach(pattern => {
      const matches = text.match(pattern);
      if (matches) score -= matches.length * 0.05;
    });

    // Logical flow indicators
    const logicalPatterns = [
      /because|therefore|so|thus|since/gi,
      /first|second|finally|in conclusion/gi
    ];
    
    logicalPatterns.forEach(pattern => {
      const matches = text.match(pattern);
      if (matches) score += matches.length * 0.03;
    });

    return Math.max(0, Math.min(1, score));
  }

  calculateContextualRelevance(text) {
    let score = 0.6;
    
    // Check if message relates to recent conversation
    if (this.currentSession.messages.length > 1) {
      const recentTopics = this.extractTopics(
        this.currentSession.messages.slice(-5).map(m => m.text).join(' ')
      );
      
      const currentTopics = this.extractTopics(text);
      const overlap = this.calculateTopicOverlap(recentTopics, currentTopics);
      score = 0.4 + (overlap * 0.6);
    }

    return score;
  }

  calculateEngagement(text) {
    let score = 0.5;
    
    // Questions indicate engagement
    if (text.includes('?')) score += 0.2;
    
    // Active listening phrases
    const engagementPatterns = [
      /i see|i understand|tell me more|interesting|really/gi,
      /what do you think|how do you feel|can you explain/gi
    ];
    
    engagementPatterns.forEach(pattern => {
      const matches = text.match(pattern);
      if (matches) score += matches.length * 0.1;
    });

    // Length indicates effort
    if (text.length > 100) score += 0.1;
    if (text.length > 200) score += 0.1;

    return Math.min(1, score);
  }

  calculateEmpathy(text) {
    let score = 0.5;
    
    // Empathy indicators
    const empathyPatterns = [
      /i understand|i feel|sorry to hear|that must be/gi,
      /how are you|are you okay|take care|hope you/gi,
      /thank you|appreciate|grateful|means a lot/gi
    ];
    
    empathyPatterns.forEach(pattern => {
      const matches = text.match(pattern);
      if (matches) score += matches.length * 0.1;
    });

    // Emotional language
    const emotionWords = /happy|sad|excited|worried|glad|upset|frustrated|pleased/gi;
    const emotionMatches = text.match(emotionWords);
    if (emotionMatches) score += emotionMatches.length * 0.05;

    return Math.min(1, score);
  }

  calculateClarity(text) {
    let score = 1.0;
    
    // Penalize unclear language
    const unclearPatterns = [
      /thing|stuff|whatever|you know|kind of|sort of/gi,
      /um|uh|er|hmm/gi
    ];
    
    unclearPatterns.forEach(pattern => {
      const matches = text.match(pattern);
      if (matches) score -= matches.length * 0.02;
    });

    // Reward clear structure
    const sentences = text.split(/[.!?]+/);
    const avgSentenceLength = text.length / sentences.length;
    
    // Optimal sentence length is 15-20 words
    if (avgSentenceLength > 150) score -= 0.2; // Too long
    if (avgSentenceLength < 30) score -= 0.1;  // Too short

    return Math.max(0, score);
  }

  analyzeSentiment(text) {
    // Simple sentiment analysis
    const positiveWords = /good|great|awesome|love|wonderful|excellent|happy|glad/gi;
    const negativeWords = /bad|terrible|hate|awful|horrible|sad|angry|frustrated/gi;
    
    const positiveCount = (text.match(positiveWords) || []).length;
    const negativeCount = (text.match(negativeWords) || []).length;
    
    if (positiveCount > negativeCount) return 'positive';
    if (negativeCount > positiveCount) return 'negative';
    return 'neutral';
  }

  calculateTurnBalance() {
    if (this.currentSession.messages.length < 4) return 0.5;
    
    const senderCounts = {};
    this.currentSession.messages.forEach(msg => {
      senderCounts[msg.sender] = (senderCounts[msg.sender] || 0) + 1;
    });
    
    const counts = Object.values(senderCounts);
    const max = Math.max(...counts);
    const min = Math.min(...counts);
    
    // Perfect balance = 1, complete imbalance = 0
    return 1 - ((max - min) / this.currentSession.messages.length);
  }

  calculateResponseLatency(timestamp) {
    if (this.currentSession.messages.length === 0) return 1;
    
    const lastMessage = this.currentSession.messages[this.currentSession.messages.length - 1];
    const latency = (timestamp - lastMessage.timestamp) / 1000; // seconds
    
    // Ideal response time: 5-30 seconds
    if (latency < 5) return 0.7;    // Too quick, might not be thoughtful
    if (latency < 30) return 1.0;   // Ideal
    if (latency < 120) return 0.8;  // Still good
    if (latency < 300) return 0.6;  // Getting slow
    return 0.4; // Too slow
  }

  calculateTopicCoherence(text) {
    // This would be more sophisticated in production
    return 0.7;
  }

  extractTopics(text) {
    // Simple keyword extraction
    const words = text.toLowerCase().split(/\W+/);
    const stopWords = new Set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for']);
    return words.filter(w => w.length > 3 && !stopWords.has(w));
  }

  calculateTopicOverlap(topics1, topics2) {
    const set1 = new Set(topics1);
    const set2 = new Set(topics2);
    const intersection = new Set([...set1].filter(x => set2.has(x)));
    return intersection.size / Math.max(set1.size, set2.size, 1);
  }

  calculateOverallScore(metrics) {
    // Weighted average for human conversations
    return (
      metrics.psi * 0.2 +
      metrics.rho * 0.2 +
      metrics.q * 0.2 +
      metrics.f * 0.2 +
      metrics.clarity * 0.1 +
      metrics.turnBalance * 0.1
    );
  }

  generateInsights(metrics) {
    const insights = [];
    
    if (metrics.psi > 0.8) insights.push("Clear and consistent communication");
    if (metrics.rho > 0.8) insights.push("Staying well on topic");
    if (metrics.q > 0.8) insights.push("Highly engaged conversation");
    if (metrics.f > 0.8) insights.push("Showing good empathy");
    if (metrics.clarity > 0.8) insights.push("Very clear expression");
    
    if (metrics.psi < 0.4) insights.push("Consider being more consistent");
    if (metrics.rho < 0.4) insights.push("Conversation may be drifting off-topic");
    if (metrics.q < 0.4) insights.push("Could show more engagement");
    if (metrics.f < 0.4) insights.push("Consider showing more empathy");
    
    return insights;
  }
}

// Universal Chat Detector
class UniversalChatDetector {
  constructor() {
    this.chatPatterns = [
      // Generic patterns that work across platforms
      {
        name: 'Generic Message List',
        messageSelector: '[class*="message"], [class*="msg"], [class*="chat"]',
        senderSelector: '[class*="sender"], [class*="author"], [class*="name"], [class*="user"]',
        textSelector: '[class*="text"], [class*="content"], [class*="body"]',
        timeSelector: '[class*="time"], [class*="timestamp"], [class*="date"]'
      },
      // Specific platform patterns
      {
        name: 'WhatsApp Web',
        urlPattern: /web.whatsapp.com/,
        messageSelector: 'div[class*="message-"]',
        senderSelector: 'span[class*="copyable-text"]',
        textSelector: 'span[class*="copyable-text"] span',
        isSelf: (element) => element.closest('[class*="message-out"]') !== null
      },
      {
        name: 'Facebook Messenger',
        urlPattern: /messenger.com|facebook.com\/messages/,
        messageSelector: 'div[class*="__fb-dark-mode"]',
        textSelector: 'div[dir="auto"]',
        senderSelector: 'div[class*="__fb-dark-mode"]'
      },
      {
        name: 'Slack',
        urlPattern: /slack.com/,
        messageSelector: 'div[class*="c-message_kit__message"]',
        senderSelector: 'button[class*="c-message__sender_link"]',
        textSelector: 'div[class*="c-message__body"]'
      },
      {
        name: 'Discord',
        urlPattern: /discord.com/,
        messageSelector: 'li[class*="message-"]',
        senderSelector: 'span[class*="username-"]',
        textSelector: 'div[class*="messageContent-"]'
      },
      {
        name: 'Teams',
        urlPattern: /teams.microsoft.com/,
        messageSelector: 'div[data-tid="messageBodyContent"]',
        senderSelector: 'span[data-tid="messageAuthor"]',
        textSelector: 'div[data-tid="messageBodyContent"]'
      }
    ];
    
    this.currentPattern = null;
  }

  detectChatInterface() {
    // First try URL-based detection
    const url = window.location.href;
    for (const pattern of this.chatPatterns) {
      if (pattern.urlPattern && pattern.urlPattern.test(url)) {
        console.log('Chat Analyzer: Detected platform by URL:', pattern.name);
        return pattern;
      }
    }
    
    // Then try generic detection
    for (const pattern of this.chatPatterns) {
      if (!pattern.urlPattern) {
        const messages = document.querySelectorAll(pattern.messageSelector);
        if (messages.length > 0) {
          console.log('Chat Analyzer: Detected chat interface:', pattern.name);
          return pattern;
        }
      }
    }
    
    return null;
  }

  extractMessageInfo(element, pattern) {
    const info = {
      text: '',
      sender: 'Unknown',
      timestamp: Date.now(),
      isSelf: false
    };
    
    // Extract text
    if (pattern.textSelector) {
      const textElement = element.querySelector(pattern.textSelector);
      info.text = textElement ? textElement.textContent.trim() : element.textContent.trim();
    } else {
      info.text = element.textContent.trim();
    }
    
    // Extract sender
    if (pattern.senderSelector) {
      const senderElement = element.querySelector(pattern.senderSelector);
      info.sender = senderElement ? senderElement.textContent.trim() : 'Unknown';
    }
    
    // Determine if self
    if (pattern.isSelf) {
      info.isSelf = pattern.isSelf(element);
    } else {
      // Generic self-detection based on common patterns
      info.isSelf = element.classList.toString().includes('self') ||
                    element.classList.toString().includes('out') ||
                    element.classList.toString().includes('me');
    }
    
    return info;
  }
}

// Main Chat Monitor
class UniversalChatMonitor {
  constructor() {
    this.analyzer = new HumanConversationAnalyzer();
    this.detector = new UniversalChatDetector();
    this.observer = null;
    this.widget = null;
    this.processedMessages = new Set();
    this.enabled = false;
  }

  init() {
    console.log('Universal Chat Analyzer: Initializing...');
    
    // Check if we're on a chat interface
    const pattern = this.detector.detectChatInterface();
    if (!pattern) {
      console.log('Universal Chat Analyzer: No chat interface detected');
      return;
    }
    
    this.currentPattern = pattern;
    this.createWidget();
    this.startMonitoring();
    
    // Listen for enable/disable from popup
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
      if (request.action === 'toggle') {
        this.enabled = request.enabled;
        if (this.enabled) {
          this.widget.show();
          this.startMonitoring();
        } else {
          this.widget.hide();
          this.stopMonitoring();
        }
      }
    });
  }

  createWidget() {
    // Create floating widget similar to the AI version
    const container = document.createElement('div');
    container.id = 'chat-coherence-widget';
    container.style.cssText = `
      position: fixed;
      bottom: 20px;
      left: 20px;
      width: 320px;
      background: white;
      border-radius: 12px;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
      z-index: 999999;
      font-family: -apple-system, sans-serif;
      display: none;
    `;
    
    container.innerHTML = `
      <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                  color: white; padding: 12px 16px; border-radius: 12px 12px 0 0;
                  display: flex; justify-content: space-between; align-items: center;">
        <div>Chat Quality Monitor</div>
        <button id="widget-close" style="background: rgba(255,255,255,0.2); 
                border: none; color: white; padding: 4px 8px; 
                border-radius: 4px; cursor: pointer;">×</button>
      </div>
      <div id="widget-content" style="padding: 16px;">
        <div id="overall-score" style="text-align: center; margin-bottom: 16px;">
          <div style="font-size: 36px; font-weight: bold;">--</div>
          <div>Conversation Quality</div>
        </div>
        <div id="metrics-grid" style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
          <!-- Metrics will be inserted here -->
        </div>
        <div id="insights" style="margin-top: 16px; font-size: 12px; color: #666;">
          <!-- Insights will be inserted here -->
        </div>
        <button id="export-btn" style="width: 100%; margin-top: 16px; 
                background: #667eea; color: white; border: none; 
                padding: 8px; border-radius: 6px; cursor: pointer;">
          Export Conversation Analysis
        </button>
      </div>
    `;
    
    document.body.appendChild(container);
    this.widget = {
      container,
      show: () => container.style.display = 'block',
      hide: () => container.style.display = 'none',
      update: (analysis) => this.updateWidget(analysis)
    };
    
    // Event listeners
    document.getElementById('widget-close').addEventListener('click', () => {
      this.widget.hide();
      this.enabled = false;
    });
    
    document.getElementById('export-btn').addEventListener('click', () => {
      this.exportAnalysis();
    });
  }

  updateWidget(analysis) {
    const overall = (analysis.overall * 100).toFixed(0);
    document.getElementById('overall-score').innerHTML = `
      <div style="font-size: 36px; font-weight: bold; color: ${this.getScoreColor(analysis.overall)}">
        ${overall}%
      </div>
      <div>Conversation Quality</div>
    `;
    
    // Update metrics
    const metricsHtml = `
      <div class="metric-card" style="background: #f3f4f6; padding: 12px; border-radius: 8px;">
        <div style="font-size: 11px; color: #6b7280;">Consistency</div>
        <div style="font-size: 18px; font-weight: 600;">
          ${(analysis.metrics.psi * 100).toFixed(0)}%
        </div>
      </div>
      <div class="metric-card" style="background: #f3f4f6; padding: 12px; border-radius: 8px;">
        <div style="font-size: 11px; color: #6b7280;">Relevance</div>
        <div style="font-size: 18px; font-weight: 600;">
          ${(analysis.metrics.rho * 100).toFixed(0)}%
        </div>
      </div>
      <div class="metric-card" style="background: #f3f4f6; padding: 12px; border-radius: 8px;">
        <div style="font-size: 11px; color: #6b7280;">Engagement</div>
        <div style="font-size: 18px; font-weight: 600;">
          ${(analysis.metrics.q * 100).toFixed(0)}%
        </div>
      </div>
      <div class="metric-card" style="background: #f3f4f6; padding: 12px; border-radius: 8px;">
        <div style="font-size: 11px; color: #6b7280;">Empathy</div>
        <div style="font-size: 18px; font-weight: 600;">
          ${(analysis.metrics.f * 100).toFixed(0)}%
        </div>
      </div>
    `;
    document.getElementById('metrics-grid').innerHTML = metricsHtml;
    
    // Update insights
    if (analysis.insights && analysis.insights.length > 0) {
      document.getElementById('insights').innerHTML = 
        '<strong>Insights:</strong><br>' + analysis.insights.join('<br>');
    }
  }

  getScoreColor(score) {
    if (score >= 0.8) return '#10b981';
    if (score >= 0.6) return '#f59e0b';
    if (score >= 0.4) return '#f97316';
    return '#ef4444';
  }

  startMonitoring() {
    if (!this.currentPattern || !this.enabled) return;
    
    // Initial analysis of existing messages
    const messages = document.querySelectorAll(this.currentPattern.messageSelector);
    messages.forEach(msg => this.processMessage(msg));
    
    // Monitor for new messages
    this.observer = new MutationObserver((mutations) => {
      mutations.forEach(mutation => {
        mutation.addedNodes.forEach(node => {
          if (node.nodeType === Node.ELEMENT_NODE) {
            if (node.matches && node.matches(this.currentPattern.messageSelector)) {
              this.processMessage(node);
            }
            // Check descendants
            const messages = node.querySelectorAll(this.currentPattern.messageSelector);
            messages.forEach(msg => this.processMessage(msg));
          }
        });
      });
    });
    
    this.observer.observe(document.body, {
      childList: true,
      subtree: true
    });
  }

  stopMonitoring() {
    if (this.observer) {
      this.observer.disconnect();
      this.observer = null;
    }
  }

  processMessage(element) {
    // Avoid processing the same message twice
    const messageId = element.textContent + element.className;
    if (this.processedMessages.has(messageId)) return;
    this.processedMessages.add(messageId);
    
    const messageInfo = this.detector.extractMessageInfo(element, this.currentPattern);
    if (messageInfo.text.length < 3) return; // Skip very short messages
    
    const analysis = this.analyzer.analyzeMessage(
      messageInfo.text,
      messageInfo.isSelf ? 'You' : messageInfo.sender,
      messageInfo.timestamp
    );
    
    this.widget.update(analysis);
    
    // Send to background for logging
    chrome.runtime.sendMessage({
      type: 'logMessage',
      data: {
        ...messageInfo,
        analysis
      }
    });
  }

  exportAnalysis() {
    const data = {
      platform: this.currentPattern.name,
      sessionStart: new Date(this.analyzer.currentSession.startTime).toISOString(),
      messages: this.analyzer.currentSession.messages,
      summary: {
        totalMessages: this.analyzer.currentSession.messages.length,
        participants: [...new Set(this.analyzer.currentSession.messages.map(m => m.sender))],
        averageQuality: this.analyzer.currentSession.messages.reduce(
          (sum, m) => sum + this.analyzer.calculateOverallScore(m.metrics), 0
        ) / this.analyzer.currentSession.messages.length
      }
    };
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `chat-analysis-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  }
}

// Handle messages from popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  switch (request.action) {
    case 'checkSupport':
      const detector = new UniversalChatDetector();
      const pattern = detector.detectChatInterface();
      sendResponse({
        supported: pattern !== null,
        platform: pattern ? pattern.name : null
      });
      break;
      
    case 'toggle':
      if (window.chatMonitor) {
        window.chatMonitor.enabled = request.enabled;
        if (request.enabled) {
          window.chatMonitor.widget.show();
          window.chatMonitor.startMonitoring();
        } else {
          window.chatMonitor.widget.hide();
          window.chatMonitor.stopMonitoring();
        }
      } else if (request.enabled) {
        // Initialize if not already done
        window.chatMonitor = new UniversalChatMonitor();
        window.chatMonitor.enabled = true;
        window.chatMonitor.init();
      }
      break;
      
    case 'getStats':
      if (window.chatMonitor && window.chatMonitor.analyzer) {
        const messages = window.chatMonitor.analyzer.currentSession.messages;
        const avgQuality = messages.length > 0 ?
          messages.reduce((sum, m) => sum + window.chatMonitor.analyzer.calculateOverallScore(m.metrics), 0) / messages.length :
          0;
        sendResponse({
          messageCount: messages.length,
          averageQuality: avgQuality
        });
      } else {
        sendResponse({ messageCount: 0, averageQuality: 0 });
      }
      break;
  }
  return true;
});

// Initialize when ready (but don't auto-start)
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    // Check if we should auto-initialize based on saved state
    chrome.storage.local.get([`active_${chrome.runtime.id}`], (result) => {
      if (result[`active_${chrome.runtime.id}`]) {
        window.chatMonitor = new UniversalChatMonitor();
        window.chatMonitor.enabled = true;
        window.chatMonitor.init();
      }
    });
  });
} else {
  // Check if we should auto-initialize
  chrome.storage.local.get([`active_${chrome.runtime.id}`], (result) => {
    if (result[`active_${chrome.runtime.id}`]) {
      window.chatMonitor = new UniversalChatMonitor();
      window.chatMonitor.enabled = true;
      window.chatMonitor.init();
    }
  });
}