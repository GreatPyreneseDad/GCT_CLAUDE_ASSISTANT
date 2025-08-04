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
      responseLatencies: [],
      scoreLog: [] // Track scores over time
    };
    this.messageCount = 0;
  }

  analyzeMessage(text, sender, timestamp = Date.now()) {
    this.messageCount++;
    
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

    const overall = this.calculateOverallScore(metrics);
    const elapsed = (timestamp - this.currentSession.startTime) / 1000; // seconds

    // Store message
    const messageData = {
      text,
      sender,
      timestamp,
      metrics,
      overall
    };
    
    this.currentSession.messages.push(messageData);
    
    // Add to score log for graphing
    this.currentSession.scoreLog.push({
      time: elapsed,
      score: overall,
      psi: metrics.psi,
      rho: metrics.rho,
      q: metrics.q,
      f: metrics.f,
      messageCount: this.messageCount
    });

    return {
      metrics,
      overall,
      insights: this.generateInsights(metrics),
      scoreLog: this.currentSession.scoreLog,
      messageCount: this.messageCount
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
  
  isAdvertisement(element) {
    // Check if element or its parents contain ad indicators
    const adIndicators = [
      'sponsored', 'ad', 'advertisement', 'promo', 'promoted',
      'suggested', 'recommended'
    ];
    
    const elementText = element.textContent.toLowerCase();
    const elementClasses = element.className ? element.className.toLowerCase() : '';
    
    // Check element and its parents for ad indicators
    let currentElement = element;
    for (let i = 0; i < 5; i++) { // Check up to 5 parent levels
      if (!currentElement) break;
      
      const classes = currentElement.className ? currentElement.className.toLowerCase() : '';
      const id = currentElement.id ? currentElement.id.toLowerCase() : '';
      
      for (const indicator of adIndicators) {
        if (classes.includes(indicator) || id.includes(indicator)) {
          return true;
        }
      }
      
      currentElement = currentElement.parentElement;
    }
    
    // Check for common ad patterns in text
    if (elementText.includes('sponsored') || 
        elementText.includes('promoted') ||
        elementText.startsWith('ad ')) {
      return true;
    }
    
    return false;
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
    
    // Show widget if enabled
    if (this.enabled) {
      this.widget.show();
      this.startMonitoring();
    }
    
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
    // Create floating widget with shadow DOM for isolation
    const container = document.createElement('div');
    container.id = 'chat-coherence-widget';
    container.style.cssText = `
      position: fixed;
      bottom: 20px;
      left: 20px;
      width: 380px;
      z-index: 2147483647;
    `;
    
    // Use shadow DOM for style isolation
    const shadowRoot = container.attachShadow({ mode: 'open' });
    
    shadowRoot.innerHTML = `
      <style>
        * { box-sizing: border-box; }
        .widget-container {
          background: white;
          border-radius: 12px;
          box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
          font-family: -apple-system, sans-serif;
          font-size: 14px;
          overflow: hidden;
        }
        .widget-header {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          padding: 12px 16px;
          display: flex;
          justify-content: space-between;
          align-items: center;
        }
        .close-btn {
          background: rgba(255,255,255,0.2);
          border: none;
          color: white;
          padding: 4px 8px;
          border-radius: 4px;
          cursor: pointer;
        }
        .widget-body {
          padding: 16px;
        }
        .score-main {
          text-align: center;
          margin-bottom: 16px;
        }
        .score-value {
          font-size: 36px;
          font-weight: bold;
        }
        .metrics-grid {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 8px;
          margin-bottom: 16px;
        }
        .metric-card {
          background: #f3f4f6;
          padding: 12px;
          border-radius: 8px;
        }
        .metric-label {
          font-size: 11px;
          color: #6b7280;
          margin-bottom: 4px;
        }
        .metric-value {
          font-size: 18px;
          font-weight: 600;
        }
        .graph-container {
          margin-top: 16px;
          height: 120px;
          background: #f9fafb;
          border-radius: 8px;
          position: relative;
        }
        .graph-canvas {
          width: 100%;
          height: 100%;
        }
        .stats-row {
          display: flex;
          justify-content: space-between;
          margin: 8px 0;
          font-size: 12px;
        }
        .insights {
          margin-top: 16px;
          font-size: 12px;
          color: #666;
        }
        .export-btn {
          width: 100%;
          margin-top: 16px;
          background: #667eea;
          color: white;
          border: none;
          padding: 8px;
          border-radius: 6px;
          cursor: pointer;
        }
        .export-btn:hover {
          background: #5a56d6;
        }
      </style>
      <div class="widget-container">
        <div class="widget-header">
          <div>Chat Quality Monitor</div>
          <button class="close-btn" id="widget-close">×</button>
        </div>
        <div class="widget-body">
          <div class="score-main">
            <div class="score-value" id="overall-score">--</div>
            <div>Conversation Quality</div>
          </div>
          <div class="metrics-grid" id="metrics-grid">
            <!-- Metrics will be inserted here -->
          </div>
          <div class="graph-container">
            <canvas class="graph-canvas" id="coherence-graph"></canvas>
          </div>
          <div class="stats-row">
            <span>Messages: <strong id="message-count">0</strong></span>
            <span>Duration: <strong id="duration">0:00</strong></span>
          </div>
          <div class="insights" id="insights">
            <!-- Insights will be inserted here -->
          </div>
          <button class="export-btn" id="export-btn">
            Export Conversation Analysis
          </button>
        </div>
      </div>
    `;
    
    document.body.appendChild(container);
    
    this.widget = {
      container,
      shadowRoot,
      show: () => {
        container.style.display = 'block';
        setTimeout(() => this.drawGraph(), 100);
      },
      hide: () => container.style.display = 'none',
      update: (analysis) => this.updateWidget(analysis)
    };
    
    // Event listeners
    shadowRoot.getElementById('widget-close').addEventListener('click', () => {
      this.widget.hide();
      this.enabled = false;
      chrome.storage.local.set({[`active_${chrome.runtime.id}`]: false});
    });
    
    shadowRoot.getElementById('export-btn').addEventListener('click', () => {
      this.exportAnalysis();
    });
  }

  updateWidget(analysis) {
    if (!this.widget.shadowRoot) return;
    
    const overall = (analysis.overall * 100).toFixed(0);
    const scoreElement = this.widget.shadowRoot.getElementById('overall-score');
    if (scoreElement) {
      scoreElement.textContent = overall + '%';
      scoreElement.style.color = this.getScoreColor(analysis.overall);
    }
    
    // Update metrics
    const metricsGrid = this.widget.shadowRoot.getElementById('metrics-grid');
    if (metricsGrid) {
      metricsGrid.innerHTML = `
        <div class="metric-card">
          <div class="metric-label">Consistency</div>
          <div class="metric-value">${(analysis.metrics.psi * 100).toFixed(0)}%</div>
        </div>
        <div class="metric-card">
          <div class="metric-label">Relevance</div>
          <div class="metric-value">${(analysis.metrics.rho * 100).toFixed(0)}%</div>
        </div>
        <div class="metric-card">
          <div class="metric-label">Engagement</div>
          <div class="metric-value">${(analysis.metrics.q * 100).toFixed(0)}%</div>
        </div>
        <div class="metric-card">
          <div class="metric-label">Empathy</div>
          <div class="metric-value">${(analysis.metrics.f * 100).toFixed(0)}%</div>
        </div>
      `;
    }
    
    // Update stats
    const messageCount = this.widget.shadowRoot.getElementById('message-count');
    if (messageCount) {
      messageCount.textContent = analysis.messageCount || '0';
    }
    
    const duration = this.widget.shadowRoot.getElementById('duration');
    if (duration && this.analyzer.currentSession.startTime) {
      const elapsed = Date.now() - this.analyzer.currentSession.startTime;
      const minutes = Math.floor(elapsed / 60000);
      const seconds = Math.floor((elapsed % 60000) / 1000);
      duration.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
    }
    
    // Update insights
    const insights = this.widget.shadowRoot.getElementById('insights');
    if (insights && analysis.insights && analysis.insights.length > 0) {
      insights.innerHTML = '<strong>Insights:</strong><br>' + analysis.insights.join('<br>');
    }
    
    // Draw graph
    this.drawGraph();
  }

  getScoreColor(score) {
    if (score >= 0.8) return '#10b981';
    if (score >= 0.6) return '#f59e0b';
    if (score >= 0.4) return '#f97316';
    return '#ef4444';
  }
  
  drawGraph() {
    if (!this.widget.shadowRoot || !this.analyzer.currentSession.scoreLog) return;
    
    const canvas = this.widget.shadowRoot.getElementById('coherence-graph');
    if (!canvas) return;
    
    const data = this.analyzer.currentSession.scoreLog;
    if (data.length < 2) return;
    
    const ctx = canvas.getContext('2d');
    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width;
    canvas.height = rect.height;
    
    const padding = 10;
    const width = rect.width - 2 * padding;
    const height = rect.height - 2 * padding;
    
    // Find min/max for scaling
    const times = data.map(d => d.time);
    const scores = data.map(d => d.score);
    const minTime = Math.min(...times);
    const maxTime = Math.max(...times);
    const minScore = Math.max(0, Math.min(...scores) - 0.1);
    const maxScore = Math.min(1, Math.max(...scores) + 0.1);
    
    // Clear canvas
    ctx.clearRect(0, 0, rect.width, rect.height);
    
    // Draw axes
    ctx.strokeStyle = '#e5e7eb';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(padding, padding);
    ctx.lineTo(padding, height + padding);
    ctx.lineTo(width + padding, height + padding);
    ctx.stroke();
    
    // Draw grid lines
    ctx.strokeStyle = '#f3f4f6';
    for (let i = 0; i <= 4; i++) {
      const y = padding + (i / 4) * height;
      ctx.beginPath();
      ctx.moveTo(padding, y);
      ctx.lineTo(width + padding, y);
      ctx.stroke();
    }
    
    // Draw line
    ctx.strokeStyle = '#667eea';
    ctx.lineWidth = 2;
    ctx.beginPath();
    
    data.forEach((point, i) => {
      const x = padding + ((point.time - minTime) / (maxTime - minTime || 1)) * width;
      const y = padding + height - ((point.score - minScore) / (maxScore - minScore || 1)) * height;
      
      if (i === 0) {
        ctx.moveTo(x, y);
      } else {
        ctx.lineTo(x, y);
      }
    });
    
    ctx.stroke();
    
    // Draw points
    ctx.fillStyle = '#667eea';
    data.forEach((point) => {
      const x = padding + ((point.time - minTime) / (maxTime - minTime || 1)) * width;
      const y = padding + height - ((point.score - minScore) / (maxScore - minScore || 1)) * height;
      
      ctx.beginPath();
      ctx.arc(x, y, 3, 0, 2 * Math.PI);
      ctx.fill();
    });
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
    // Check if it's an ad
    if (this.detector.isAdvertisement(element)) {
      console.log('Chat Analyzer: Skipping advertisement');
      return;
    }
    
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
    if (!this.analyzer || !this.analyzer.currentSession) {
      console.error('No data to export');
      return;
    }
    
    const session = this.analyzer.currentSession;
    const messages = session.messages;
    
    const data = {
      metadata: {
        platform: this.currentPattern ? this.currentPattern.name : 'Unknown',
        exportTime: new Date().toISOString(),
        sessionStart: new Date(session.startTime).toISOString(),
        duration: Date.now() - session.startTime,
        version: '1.0.0'
      },
      summary: {
        totalMessages: messages.length,
        participants: [...new Set(messages.map(m => m.sender))],
        averageQuality: messages.length > 0 ? 
          messages.reduce((sum, m) => sum + m.overall, 0) / messages.length : 0,
        qualityTrend: this.calculateQualityTrend(),
        highestScore: messages.length > 0 ? 
          Math.max(...messages.map(m => m.overall)) : 0,
        lowestScore: messages.length > 0 ? 
          Math.min(...messages.map(m => m.overall)) : 0
      },
      messages: messages,
      scoreTimeline: session.scoreLog,
      insights: this.generateConversationInsights()
    };
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `chat-analysis-${this.currentPattern ? this.currentPattern.name : 'unknown'}-${new Date().toISOString().split('T')[0]}.json`;
    a.style.display = 'none';
    document.body.appendChild(a);
    a.click();
    
    setTimeout(() => {
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }, 100);
    
    console.log('Analysis exported successfully');
  }
  
  calculateQualityTrend() {
    const scores = this.analyzer.currentSession.scoreLog;
    if (scores.length < 2) return 'neutral';
    
    const firstHalf = scores.slice(0, Math.floor(scores.length / 2));
    const secondHalf = scores.slice(Math.floor(scores.length / 2));
    
    const avgFirst = firstHalf.reduce((sum, s) => sum + s.score, 0) / firstHalf.length;
    const avgSecond = secondHalf.reduce((sum, s) => sum + s.score, 0) / secondHalf.length;
    
    if (avgSecond > avgFirst + 0.05) return 'improving';
    if (avgSecond < avgFirst - 0.05) return 'declining';
    return 'stable';
  }
  
  generateConversationInsights() {
    const messages = this.analyzer.currentSession.messages;
    if (messages.length === 0) return [];
    
    const insights = [];
    const avgQuality = messages.reduce((sum, m) => sum + m.overall, 0) / messages.length;
    
    if (avgQuality > 0.8) {
      insights.push('Excellent conversation quality overall');
    } else if (avgQuality < 0.4) {
      insights.push('Conversation quality could be improved');
    }
    
    // Check balance
    const senderCounts = {};
    messages.forEach(m => {
      senderCounts[m.sender] = (senderCounts[m.sender] || 0) + 1;
    });
    const counts = Object.values(senderCounts);
    const maxDiff = Math.max(...counts) - Math.min(...counts);
    if (maxDiff > messages.length * 0.3) {
      insights.push('Conversation is dominated by one participant');
    }
    
    return insights;
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