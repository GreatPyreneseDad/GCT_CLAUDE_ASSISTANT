/**
 * Content script for GCT Coherence Monitor
 * Monitors LLM responses and displays coherence metrics
 */

// Inline the coherence analyzer to avoid import issues
class CoherenceAnalyzer {
  constructor() {
    this.history = [];
    this.maxHistory = 50;
    this.scoreLog = []; // Track scores over time
    this.responseStartTime = null;
    this.currentResponseId = null;
    this.conversationLog = []; // Track entire conversation
    this.conversationStartTime = Date.now();
    this.responseCount = 0;
  }

  analyzeResponse(text, context, responseId = null) {
    const metrics = this.calculateMetrics(text, context);
    const insights = this.generateInsights(metrics, text);
    
    const timestamp = Date.now();
    
    // Track new response
    if (responseId && responseId !== this.currentResponseId) {
      // Save previous response data if exists
      if (this.currentResponseId && this.scoreLog.length > 0) {
        this.conversationLog.push({
          responseId: this.currentResponseId,
          responseNumber: this.responseCount,
          scores: [...this.scoreLog],
          finalMetrics: this.scoreLog[this.scoreLog.length - 1],
          duration: this.scoreLog[this.scoreLog.length - 1].time
        });
      }
      
      this.currentResponseId = responseId;
      this.responseStartTime = timestamp;
      this.scoreLog = [];
      this.responseCount++;
    }
    
    // Log score for time series
    const conversationElapsed = (timestamp - this.conversationStartTime) / 1000; // seconds
    const responseElapsed = this.responseStartTime ? (timestamp - this.responseStartTime) / 1000 : 0;
    
    const scoreEntry = {
      time: responseElapsed,
      conversationTime: conversationElapsed,
      score: metrics.overall,
      psi: metrics.psi,
      rho: metrics.rho,
      q: metrics.q,
      f: metrics.f,
      textLength: text.length,
      responseNumber: this.responseCount
    };
    
    this.scoreLog.push(scoreEntry);
    
    // Calculate derivative if we have enough data
    const derivative = this.calculateDerivative();
    const conversationDerivative = this.calculateConversationDerivative();
    
    const result = {
      metrics,
      insights,
      timestamp,
      scoreLog: this.scoreLog,
      derivative,
      conversationLog: this.conversationLog,
      conversationDerivative,
      responseCount: this.responseCount
    };

    this.history.push(result);
    if (this.history.length > this.maxHistory) {
      this.history.shift();
    }

    return result;
  }

  calculateMetrics(text, context) {
    const psi = this.calculateInternalConsistency(text);
    const rho = this.calculateWisdomIntegration(text);
    const q = this.calculateActionability(text);
    const f = this.calculateSocialAwareness(text);
    const overall = this.calculateOverallCoherence(psi, rho, q, f);
    const confidence = Math.min(1, text.length / 500) * 0.8 + 0.2;

    return { psi, rho, q, f, overall, confidence };
  }

  calculateInternalConsistency(text) {
    let score = 0.7;
    const contradictionPatterns = [
      /but actually|however|on the other hand|that said|although/gi,
      /not sure|might be|could be|perhaps|maybe/gi
    ];
    
    for (const pattern of contradictionPatterns) {
      const matches = text.match(pattern);
      if (matches) {
        score -= matches.length * 0.05;
      }
    }

    const logicalPatterns = [
      /therefore|thus|consequently|as a result|because/gi,
      /first|second|third|finally|in conclusion/gi
    ];
    
    for (const pattern of logicalPatterns) {
      const matches = text.match(pattern);
      if (matches) {
        score += matches.length * 0.03;
      }
    }

    return Math.max(0, Math.min(1, score));
  }

  calculateWisdomIntegration(text) {
    let score = 0.5;
    const wisdomPatterns = [
      /learn|learned|learning|understand|understanding|realize|realized/gi,
      /experience|experienced|insight|perspective|wisdom/gi,
      /grow|growth|develop|evolve|improve|progress/gi
    ];

    for (const pattern of wisdomPatterns) {
      const matches = text.match(pattern);
      if (matches) {
        score += matches.length * 0.08;
      }
    }

    return Math.max(0, Math.min(1, score));
  }

  calculateActionability(text) {
    let score = 0.5;
    const actionPatterns = [
      /you can|you should|try to|consider|I recommend|I suggest/gi,
      /step \d|first|next|then|finally|to do this/gi,
      /example|for instance|specifically|in practice|practically/gi
    ];

    for (const pattern of actionPatterns) {
      const matches = text.match(pattern);
      if (matches) {
        score += matches.length * 0.07;
      }
    }

    return Math.max(0, Math.min(1, score));
  }

  calculateSocialAwareness(text) {
    let score = 0.5;
    const socialPatterns = [
      /people|person|individual|everyone|someone|others/gi,
      /community|society|group|team|together|collective/gi,
      /relationship|connection|communication|interaction/gi,
      /help|support|assist|collaborate|cooperate/gi
    ];

    for (const pattern of socialPatterns) {
      const matches = text.match(pattern);
      if (matches) {
        score += matches.length * 0.06;
      }
    }

    return Math.max(0, Math.min(1, score));
  }

  calculateOverallCoherence(psi, rho, q, f) {
    const coherence = psi + (rho * psi) + q + (f * psi);
    return coherence / 4;
  }

  generateInsights(metrics, text) {
    const strengths = [];
    const concerns = [];

    if (metrics.psi > 0.7) strengths.push('Highly consistent and logical');
    if (metrics.rho > 0.7) strengths.push('Shows wisdom and learning');
    if (metrics.q > 0.7) strengths.push('Provides actionable guidance');
    if (metrics.f > 0.7) strengths.push('Socially aware and considerate');

    if (metrics.psi < 0.4) concerns.push('Contains contradictions or unclear logic');
    if (metrics.rho < 0.4) concerns.push('Lacks depth or learning integration');
    if (metrics.q < 0.4) concerns.push('Too abstract or impractical');
    if (metrics.f < 0.4) concerns.push('Limited social consideration');

    const trajectory = this.analyzeTrajectory();

    return { strengths, concerns, trajectory };
  }

  analyzeTrajectory() {
    if (this.history.length < 3) return 'stable';

    const recentScores = this.history.slice(-5).map(h => h.metrics.overall);
    const avgRecent = recentScores.reduce((a, b) => a + b, 0) / recentScores.length;
    
    const olderScores = this.history.slice(-10, -5).map(h => h.metrics.overall);
    if (olderScores.length === 0) return 'stable';
    
    const avgOlder = olderScores.reduce((a, b) => a + b, 0) / olderScores.length;

    if (avgRecent > avgOlder + 0.1) return 'improving';
    if (avgRecent < avgOlder - 0.1) return 'declining';
    return 'stable';
  }
  
  calculateDerivative() {
    if (this.scoreLog.length < 2) return { current: 0, average: 0, trend: 'stable' };
    
    // Calculate instantaneous derivative (last 2 points)
    const n = this.scoreLog.length;
    const current = this.scoreLog[n-1];
    const previous = this.scoreLog[n-2];
    const dt = current.time - previous.time;
    const instantaneous = dt > 0 ? (current.score - previous.score) / dt : 0;
    
    // Calculate average derivative over last 5 points
    let avgDerivative = 0;
    if (this.scoreLog.length >= 5) {
      const recentPoints = this.scoreLog.slice(-5);
      let sum = 0;
      for (let i = 1; i < recentPoints.length; i++) {
        const dt = recentPoints[i].time - recentPoints[i-1].time;
        if (dt > 0) {
          sum += (recentPoints[i].score - recentPoints[i-1].score) / dt;
        }
      }
      avgDerivative = sum / (recentPoints.length - 1);
    } else {
      avgDerivative = instantaneous;
    }
    
    // Determine trend
    let trend = 'stable';
    if (avgDerivative > 0.01) trend = 'improving';
    else if (avgDerivative < -0.01) trend = 'declining';
    
    return {
      current: instantaneous,
      average: avgDerivative,
      trend
    };
  }
  
  calculateConversationDerivative() {
    // Get all scores from conversation including current
    const allScores = [];
    
    // Add completed responses
    this.conversationLog.forEach(response => {
      response.scores.forEach(score => {
        allScores.push(score);
      });
    });
    
    // Add current response scores
    this.scoreLog.forEach(score => {
      allScores.push(score);
    });
    
    if (allScores.length < 2) return { current: 0, average: 0, trend: 'stable' };
    
    // Calculate conversation-wide derivative
    const n = allScores.length;
    const current = allScores[n-1];
    const previous = allScores[n-2];
    const dt = current.conversationTime - previous.conversationTime;
    const instantaneous = dt > 0 ? (current.score - previous.score) / dt : 0;
    
    // Calculate average over last 10 points
    let avgDerivative = 0;
    if (allScores.length >= 10) {
      const recentPoints = allScores.slice(-10);
      let sum = 0;
      for (let i = 1; i < recentPoints.length; i++) {
        const dt = recentPoints[i].conversationTime - recentPoints[i-1].conversationTime;
        if (dt > 0) {
          sum += (recentPoints[i].score - recentPoints[i-1].score) / dt;
        }
      }
      avgDerivative = sum / (recentPoints.length - 1);
    } else {
      avgDerivative = instantaneous;
    }
    
    // Determine trend
    let trend = 'stable';
    if (avgDerivative > 0.005) trend = 'improving';
    else if (avgDerivative < -0.005) trend = 'declining';
    
    return {
      current: instantaneous,
      average: avgDerivative,
      trend
    };
  }
  
  exportData() {
    const exportObj = {
      metadata: {
        exportTime: new Date().toISOString(),
        conversationStartTime: new Date(this.conversationStartTime).toISOString(),
        responseCount: this.responseCount,
        totalDataPoints: this.conversationLog.reduce((sum, r) => sum + r.scores.length, 0) + this.scoreLog.length
      },
      conversationLog: this.conversationLog,
      currentResponse: {
        responseId: this.currentResponseId,
        responseNumber: this.responseCount,
        scores: this.scoreLog
      },
      summary: this.generateSummaryStats()
    };
    
    return exportObj;
  }
  
  generateSummaryStats() {
    const allScores = [];
    
    // Collect all scores
    this.conversationLog.forEach(response => {
      response.scores.forEach(score => allScores.push(score.score));
    });
    this.scoreLog.forEach(score => allScores.push(score.score));
    
    if (allScores.length === 0) return null;
    
    const avg = allScores.reduce((a, b) => a + b, 0) / allScores.length;
    const min = Math.min(...allScores);
    const max = Math.max(...allScores);
    const variance = allScores.reduce((sum, score) => sum + Math.pow(score - avg, 2), 0) / allScores.length;
    const stdDev = Math.sqrt(variance);
    
    return {
      averageCoherence: avg,
      minCoherence: min,
      maxCoherence: max,
      standardDeviation: stdDev,
      totalDataPoints: allScores.length,
      conversationDuration: (Date.now() - this.conversationStartTime) / 1000 // seconds
    };
  }
}

// Simple LLM platform detector
class LLMDetector {
  constructor() {
    this.platforms = {
      chatgpt: {
        urlPattern: /chat\.openai\.com/,
        messageSelector: '[data-message-author-role="assistant"]',
        name: 'ChatGPT'
      },
      claude: {
        urlPattern: /claude\.ai/,
        messageSelector: 'div.font-claude-message, div[data-testid*="message"], div[class*="prose"]:not([class*="human"])',
        name: 'Claude'
      },
      gemini: {
        urlPattern: /gemini\.google\.com/,
        messageSelector: '.model-response',
        name: 'Google Gemini'
      },
      perplexity: {
        urlPattern: /perplexity\.ai/,
        messageSelector: '.prose.break-words',
        name: 'Perplexity'
      }
    };
  }

  detectPlatform() {
    const url = window.location.href;
    for (const [key, platform] of Object.entries(this.platforms)) {
      if (platform.urlPattern.test(url)) {
        return key;
      }
    }
    return null;
  }

  getMessageSelector(platform) {
    return this.platforms[platform]?.messageSelector || null;
  }
}

// Create the floating widget
function createCoherenceWidget() {
  let container = null;
  let shadowRoot = null;
  let isMinimized = false;
  let currentAnalysis = null;

  const styles = `
    .widget-container {
      position: fixed;
      bottom: 20px;
      right: 20px;
      width: 380px;
      background: white;
      border-radius: 12px;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      font-size: 14px;
      z-index: 999999;
      transition: all 0.3s ease;
      pointer-events: all;
    }
    .widget-header {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      padding: 12px 16px;
      border-radius: 12px 12px 0 0;
      display: flex;
      align-items: center;
      justify-content: space-between;
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
      font-weight: 700;
    }
    .score-green { color: #10b981; }
    .score-yellow { color: #f59e0b; }
    .score-orange { color: #f97316; }
    .score-red { color: #ef4444; }
    .dimensions {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      margin-bottom: 16px;
    }
    .dimension-card {
      background: #f3f4f6;
      padding: 12px;
      border-radius: 8px;
    }
    .dimension-label {
      font-size: 11px;
      color: #6b7280;
      margin-bottom: 4px;
    }
    .dimension-score {
      font-size: 18px;
      font-weight: 600;
    }
    .close-btn {
      background: rgba(255, 255, 255, 0.2);
      border: none;
      color: white;
      width: 24px;
      height: 24px;
      border-radius: 4px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .close-btn:hover {
      background: rgba(255, 255, 255, 0.3);
    }
    .graph-container {
      margin-top: 16px;
      height: 120px;
      background: #f9fafb;
      border-radius: 8px;
      position: relative;
      overflow: hidden;
    }
    .graph-canvas {
      width: 100%;
      height: 100%;
    }
    .derivative-info {
      margin-top: 12px;
      padding: 12px;
      background: #f3f4f6;
      border-radius: 8px;
      font-size: 12px;
    }
    .derivative-value {
      font-weight: 600;
      font-size: 16px;
    }
    .trend-improving { color: #10b981; }
    .trend-declining { color: #ef4444; }
    .trend-stable { color: #6b7280; }
    .conversation-stats {
      margin-top: 12px;
      padding: 12px;
      background: #e5e7eb;
      border-radius: 8px;
      font-size: 12px;
    }
    .stat-row {
      display: flex;
      justify-content: space-between;
      margin-bottom: 4px;
    }
    .stat-label {
      color: #4b5563;
    }
    .stat-value {
      font-weight: 600;
      color: #1f2937;
    }
    .export-btn {
      background: #667eea;
      color: white;
      border: none;
      padding: 8px 16px;
      border-radius: 6px;
      font-size: 12px;
      cursor: pointer;
      width: 100%;
      margin-top: 12px;
      transition: background 0.2s;
    }
    .export-btn:hover {
      background: #5a56d6;
    }
    .tab-buttons {
      display: flex;
      gap: 8px;
      margin-bottom: 12px;
    }
    .tab-btn {
      flex: 1;
      padding: 6px;
      background: #f3f4f6;
      border: none;
      border-radius: 6px;
      font-size: 12px;
      cursor: pointer;
      transition: all 0.2s;
    }
    .tab-btn.active {
      background: #667eea;
      color: white;
    }
  `;

  function getScoreColor(score) {
    if (score >= 0.8) return 'score-green';
    if (score >= 0.6) return 'score-yellow';
    if (score >= 0.4) return 'score-orange';
    return 'score-red';
  }

  let activeTab = 'response'; // 'response' or 'conversation'
  
  function render() {
    if (!shadowRoot || !currentAnalysis) return;

    const derivative = currentAnalysis.derivative || { current: 0, average: 0, trend: 'stable' };
    const convDerivative = currentAnalysis.conversationDerivative || { current: 0, average: 0, trend: 'stable' };
    const activeDerivative = activeTab === 'response' ? derivative : convDerivative;
    const trendClass = `trend-${activeDerivative.trend}`;
    const trendSymbol = activeDerivative.trend === 'improving' ? '↑' : 
                       activeDerivative.trend === 'declining' ? '↓' : '→';

    shadowRoot.innerHTML = `
      <style>${styles}</style>
      <div class="widget-container">
        <div class="widget-header">
          <div>GCT Monitor</div>
          <button class="close-btn" id="close-btn">✕</button>
        </div>
        <div class="widget-body">
          <div class="score-main">
            <div class="score-value ${getScoreColor(currentAnalysis.metrics.overall)}">
              ${(currentAnalysis.metrics.overall * 100).toFixed(0)}%
            </div>
            <div>Current Coherence</div>
          </div>
          <div class="dimensions">
            <div class="dimension-card">
              <div class="dimension-label">Consistency (Ψ)</div>
              <div class="dimension-score ${getScoreColor(currentAnalysis.metrics.psi)}">
                ${(currentAnalysis.metrics.psi * 100).toFixed(0)}%
              </div>
            </div>
            <div class="dimension-card">
              <div class="dimension-label">Wisdom (ρ)</div>
              <div class="dimension-score ${getScoreColor(currentAnalysis.metrics.rho)}">
                ${(currentAnalysis.metrics.rho * 100).toFixed(0)}%
              </div>
            </div>
            <div class="dimension-card">
              <div class="dimension-label">Action (q)</div>
              <div class="dimension-score ${getScoreColor(currentAnalysis.metrics.q)}">
                ${(currentAnalysis.metrics.q * 100).toFixed(0)}%
              </div>
            </div>
            <div class="dimension-card">
              <div class="dimension-label">Social (f)</div>
              <div class="dimension-score ${getScoreColor(currentAnalysis.metrics.f)}">
                ${(currentAnalysis.metrics.f * 100).toFixed(0)}%
              </div>
            </div>
          </div>
          <div class="tab-buttons">
            <button class="tab-btn ${activeTab === 'response' ? 'active' : ''}" id="response-tab">Current Response</button>
            <button class="tab-btn ${activeTab === 'conversation' ? 'active' : ''}" id="conversation-tab">Full Conversation</button>
          </div>
          <div class="graph-container">
            <canvas class="graph-canvas" id="coherence-graph"></canvas>
          </div>
          <div class="derivative-info">
            <div>${activeTab === 'response' ? 'Response' : 'Conversation'} Rate of Change</div>
            <div class="derivative-value ${trendClass}">
              ${trendSymbol} ${(activeDerivative.average * 100).toFixed(2)}%/s
            </div>
            <div style="margin-top: 4px; color: #6b7280;">
              Trend: <span class="${trendClass}">${activeDerivative.trend}</span>
            </div>
          </div>
          <div class="conversation-stats">
            <div class="stat-row">
              <span class="stat-label">Responses:</span>
              <span class="stat-value">${currentAnalysis.responseCount || 1}</span>
            </div>
            <div class="stat-row">
              <span class="stat-label">Data Points:</span>
              <span class="stat-value">${getAllDataPoints().length}</span>
            </div>
            <div class="stat-row">
              <span class="stat-label">Avg Coherence:</span>
              <span class="stat-value">${getAverageCoherence()}%</span>
            </div>
          </div>
          <button class="export-btn" id="export-btn">Export Data for Analysis</button>
        </div>
      </div>
    `;

    // Draw the graph
    setTimeout(() => {
      drawGraph();
      
      // Attach event listeners after DOM is ready
      const closeBtn = shadowRoot.getElementById('close-btn');
      if (closeBtn) {
        closeBtn.addEventListener('click', () => {
          console.log('GCT Monitor: Close button clicked');
          hide();
        });
      }
      
      const exportBtn = shadowRoot.getElementById('export-btn');
      if (exportBtn) {
        exportBtn.addEventListener('click', (e) => {
          e.preventDefault();
          e.stopPropagation();
          console.log('GCT Monitor: Export button clicked');
          exportData();
        });
      }
      
      const responseTab = shadowRoot.getElementById('response-tab');
      const conversationTab = shadowRoot.getElementById('conversation-tab');
      if (responseTab && conversationTab) {
        responseTab.addEventListener('click', (e) => {
          e.preventDefault();
          e.stopPropagation();
          console.log('GCT Monitor: Response tab clicked');
          activeTab = 'response';
          render();
        });
        conversationTab.addEventListener('click', (e) => {
          e.preventDefault();
          e.stopPropagation();
          console.log('GCT Monitor: Conversation tab clicked');
          activeTab = 'conversation';
          render();
        });
      }
    }, 0);
  }
  
  function getAllDataPoints() {
    if (!currentAnalysis) return [];
    const allPoints = [];
    
    if (currentAnalysis.conversationLog) {
      currentAnalysis.conversationLog.forEach(response => {
        response.scores.forEach(score => allPoints.push(score));
      });
    }
    
    if (currentAnalysis.scoreLog) {
      currentAnalysis.scoreLog.forEach(score => allPoints.push(score));
    }
    
    return allPoints;
  }
  
  function getAverageCoherence() {
    const allPoints = getAllDataPoints();
    if (allPoints.length === 0) return 0;
    
    const sum = allPoints.reduce((acc, point) => acc + point.score, 0);
    return (sum / allPoints.length * 100).toFixed(1);
  }
  
  function exportData() {
    console.log('GCT Monitor: Export data function called');
    if (!currentAnalysis || !window.analyzer) {
      console.error('GCT Monitor: Missing analyzer or analysis data');
      return;
    }
    
    try {
      const data = window.analyzer.exportData();
      const jsonStr = JSON.stringify(data, null, 2);
      const blob = new Blob([jsonStr], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      
      const a = document.createElement('a');
      a.href = url;
      a.download = `gct-coherence-data-${new Date().toISOString().replace(/[:.]/g, '-')}.json`;
      a.style.display = 'none';
      document.body.appendChild(a);
      a.click();
      
      setTimeout(() => {
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
      }, 100);
      
      console.log('GCT Monitor: Data exported successfully');
    } catch (error) {
      console.error('GCT Monitor: Export failed', error);
    }
  }
  
  function drawGraph() {
    if (!shadowRoot || !currentAnalysis) return;
    
    const canvas = shadowRoot.getElementById('coherence-graph');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width * window.devicePixelRatio;
    canvas.height = rect.height * window.devicePixelRatio;
    ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
    
    // Get data based on active tab
    let data;
    if (activeTab === 'response') {
      data = currentAnalysis.scoreLog || [];
    } else {
      data = getAllDataPoints();
    }
    
    if (data.length < 2) return;
    
    const padding = 10;
    const width = rect.width - 2 * padding;
    const height = rect.height - 2 * padding;
    
    // Find min/max for scaling
    const timeField = activeTab === 'response' ? 'time' : 'conversationTime';
    const times = data.map(d => d[timeField]);
    const scores = data.map(d => d.score);
    const minTime = Math.min(...times);
    const maxTime = Math.max(...times);
    const minScore = Math.min(...scores) * 0.9;
    const maxScore = Math.max(...scores) * 1.1;
    
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
    
    // Draw response boundaries in conversation view
    if (activeTab === 'conversation' && currentAnalysis.conversationLog) {
      ctx.strokeStyle = '#ddd6fe';
      ctx.lineWidth = 1;
      ctx.setLineDash([5, 5]);
      
      currentAnalysis.conversationLog.forEach((response, idx) => {
        if (response.scores.length > 0) {
          const lastScore = response.scores[response.scores.length - 1];
          const x = padding + ((lastScore.conversationTime - minTime) / (maxTime - minTime)) * width;
          ctx.beginPath();
          ctx.moveTo(x, padding);
          ctx.lineTo(x, height + padding);
          ctx.stroke();
          
          // Label
          ctx.fillStyle = '#9333ea';
          ctx.font = '10px sans-serif';
          ctx.fillText(`R${idx + 1}`, x + 2, padding + 10);
        }
      });
      ctx.setLineDash([]);
    }
    
    // Draw line
    ctx.strokeStyle = '#667eea';
    ctx.lineWidth = 2;
    ctx.beginPath();
    
    data.forEach((point, i) => {
      const x = padding + ((point[timeField] - minTime) / (maxTime - minTime)) * width;
      const y = padding + height - ((point.score - minScore) / (maxScore - minScore)) * height;
      
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
      const x = padding + ((point[timeField] - minTime) / (maxTime - minTime)) * width;
      const y = padding + height - ((point.score - minScore) / (maxScore - minScore)) * height;
      
      ctx.beginPath();
      ctx.arc(x, y, 2, 0, 2 * Math.PI);
      ctx.fill();
    });
  }

  function inject() {
    container = document.createElement('div');
    container.id = 'gct-coherence-widget';
    container.style.position = 'fixed';
    container.style.zIndex = '2147483647'; // Maximum z-index
    document.body.appendChild(container);

    shadowRoot = container.attachShadow({ mode: 'open' });
    
    // Add a test widget immediately to verify it's working
    const testHTML = `
      <style>
        .test-widget {
          position: fixed;
          bottom: 20px;
          right: 20px;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          padding: 20px;
          border-radius: 12px;
          font-family: sans-serif;
          box-shadow: 0 10px 25px rgba(0,0,0,0.2);
          pointer-events: all;
        }
      </style>
      <div class="test-widget">
        <h3>GCT Monitor Active!</h3>
        <p>Waiting for AI response...</p>
      </div>
    `;
    shadowRoot.innerHTML = testHTML;
  }

  function update(analysis) {
    currentAnalysis = analysis;
    render();
  }

  function show() {
    if (container) {
      container.style.display = 'block';
    }
  }

  function hide() {
    if (container) {
      container.style.display = 'none';
    }
  }

  return { inject, update, show, hide };
}

// Main monitor class
class CoherenceMonitor {
  constructor() {
    this.analyzer = new CoherenceAnalyzer();
    this.detector = new LLMDetector();
    this.widget = createCoherenceWidget();
    this.observer = null;
    this.lastAnalyzedText = '';
    this.isEnabled = true;
    this.currentMessageElement = null;
    this.analysisInterval = null;
    this.messageId = null;
    
    // Make analyzer available for export
    window.analyzer = this.analyzer;
    
    this.init();
  }

  async init() {
    console.log('GCT Monitor: Initializing...');
    
    const settings = await chrome.storage.sync.get(['enabled']);
    this.isEnabled = settings.enabled !== false;
    console.log('GCT Monitor: Enabled?', this.isEnabled);

    if (!this.isEnabled) return;

    const platform = this.detector.detectPlatform();
    console.log('GCT Monitor: Current URL:', window.location.href);
    console.log('GCT Monitor: Detected platform:', platform);
    
    if (!platform) {
      console.log('GCT Monitor: Not on a supported LLM platform');
      return;
    }

    console.log(`GCT Monitor: Detected ${platform} platform`);

    this.widget.inject();
    this.widget.show(); // Force show for debugging
    console.log('GCT Monitor: Widget injected and shown');
    
    this.startMonitoring(platform);

    chrome.storage.onChanged.addListener((changes) => {
      if (changes.enabled) {
        this.isEnabled = changes.enabled.newValue;
        if (this.isEnabled) {
          this.widget.show();
          this.startMonitoring(platform);
        } else {
          this.widget.hide();
          this.stopMonitoring();
        }
      }
    });
  }

  startMonitoring(platform) {
    this.stopMonitoring();

    const selector = this.detector.getMessageSelector(platform);
    console.log('GCT Monitor: Using selector:', selector);
    if (!selector) return;

    this.observer = new MutationObserver((mutations) => {
      for (const mutation of mutations) {
        if (mutation.type === 'childList' || mutation.type === 'characterData') {
          const newMessages = this.findNewLLMMessages(mutation.addedNodes, selector);
          if (newMessages.length > 0) {
            console.log('GCT Monitor: Found new messages:', newMessages.length);
            // Start monitoring the newest message
            const latestMessage = newMessages[newMessages.length - 1];
            this.startStreamingAnalysis(latestMessage);
          }
        }
        
        // Check if current message is being updated
        if (this.currentMessageElement && mutation.target) {
          if (this.currentMessageElement.contains(mutation.target) ||
              mutation.target === this.currentMessageElement) {
            console.log('GCT Monitor: Current message updated');
          }
        }
      }
    });

    this.observer.observe(document.body, {
      childList: true,
      subtree: true,
      characterData: true
    });

    // Analyze existing messages
    const existingMessages = document.querySelectorAll(selector);
    console.log('GCT Monitor: Found existing messages:', existingMessages.length);
    const lastMessage = existingMessages[existingMessages.length - 1];
    if (lastMessage) {
      console.log('GCT Monitor: Starting streaming analysis of last message');
      this.startStreamingAnalysis(lastMessage);
    }
  }

  stopMonitoring() {
    if (this.observer) {
      this.observer.disconnect();
      this.observer = null;
    }
    if (this.analysisInterval) {
      clearInterval(this.analysisInterval);
      this.analysisInterval = null;
    }
  }

  findNewLLMMessages(nodes, selector) {
    const messages = [];
    
    nodes.forEach(node => {
      if (node.nodeType === Node.ELEMENT_NODE) {
        if (node.matches && node.matches(selector)) {
          messages.push(node);
        }
        
        if (node.querySelectorAll) {
          const descendantMessages = node.querySelectorAll(selector);
          descendantMessages.forEach(msg => messages.push(msg));
        }
      }
    });

    return messages;
  }

  startStreamingAnalysis(element) {
    // Stop any existing analysis
    if (this.analysisInterval) {
      clearInterval(this.analysisInterval);
    }
    
    // Set new message element and generate ID
    this.currentMessageElement = element;
    this.messageId = `msg_${Date.now()}`;
    console.log('GCT Monitor: Starting streaming analysis for message', this.messageId);
    
    // Analyze immediately
    this.analyzeCurrentMessage();
    
    // Set up continuous analysis every 500ms
    this.analysisInterval = setInterval(() => {
      this.analyzeCurrentMessage();
    }, 500);
  }
  
  analyzeCurrentMessage() {
    if (!this.currentMessageElement) return;
    
    const text = this.currentMessageElement.textContent || '';
    
    // Skip if text is too short or unchanged
    if (text.length < 50) {
      console.log('GCT Monitor: Text too short:', text.length);
      return;
    }
    
    // Check if text actually changed
    const textChanged = text !== this.lastAnalyzedText;
    if (!textChanged && this.analyzer.scoreLog.length > 0) {
      console.log('GCT Monitor: Text unchanged, skipping analysis');
      return;
    }
    
    this.lastAnalyzedText = text;
    console.log('GCT Monitor: Analyzing text length:', text.length);

    const result = this.analyzer.analyzeResponse(text, null, this.messageId);
    this.widget.update(result);
    this.widget.show();

    // Update badge
    chrome.runtime.sendMessage({
      type: 'UPDATE_BADGE',
      score: result.metrics.overall
    });
    
    // Log current state
    console.log('GCT Monitor: Score log length:', result.scoreLog.length);
    if (result.derivative) {
      console.log('GCT Monitor: Derivative:', result.derivative);
    }
  }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    window.gctMonitor = new CoherenceMonitor();
  });
} else {
  window.gctMonitor = new CoherenceMonitor();
}