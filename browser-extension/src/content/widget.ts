/**
 * Floating widget that displays real-time coherence metrics
 * Pure JavaScript/TypeScript implementation without React
 */

import { AnalysisResult } from '../utils/coherence-analyzer';

export function createCoherenceWidget() {
  let container: HTMLDivElement | null = null;
  let shadowRoot: ShadowRoot | null = null;
  let isMinimized = false;
  let currentAnalysis: AnalysisResult | null = null;
  let history: AnalysisResult[] = [];

  const styles = `
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    .widget-container {
      position: fixed;
      bottom: 20px;
      right: 20px;
      width: 320px;
      background: white;
      border-radius: 12px;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      font-size: 14px;
      z-index: 999999;
      transition: all 0.3s ease;
    }

    .widget-container.minimized {
      width: 200px;
    }

    .widget-header {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      padding: 12px 16px;
      border-radius: 12px 12px 0 0;
      display: flex;
      align-items: center;
      justify-content: space-between;
      cursor: move;
    }

    .widget-title {
      font-weight: 600;
      font-size: 14px;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .widget-controls {
      display: flex;
      gap: 8px;
    }

    .widget-btn {
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
      transition: background 0.2s;
    }

    .widget-btn:hover {
      background: rgba(255, 255, 255, 0.3);
    }

    .widget-body {
      padding: 16px;
      max-height: 400px;
      overflow-y: auto;
    }

    .widget-body.hidden {
      display: none;
    }

    .score-main {
      text-align: center;
      margin-bottom: 16px;
    }

    .score-value {
      font-size: 36px;
      font-weight: 700;
      margin-bottom: 4px;
    }

    .score-label {
      font-size: 12px;
      color: #6b7280;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 4px;
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

    .insights {
      margin-top: 16px;
      padding-top: 16px;
      border-top: 1px solid #e5e7eb;
    }

    .insights-title {
      font-size: 12px;
      font-weight: 600;
      color: #374151;
      margin-bottom: 8px;
    }

    .insight-item {
      font-size: 12px;
      color: #6b7280;
      margin-bottom: 4px;
      padding-left: 16px;
      position: relative;
    }

    .insight-item:before {
      content: '•';
      position: absolute;
      left: 0;
    }

    .insight-item.strength {
      color: #10b981;
    }

    .insight-item.concern {
      color: #f97316;
    }

    .history-chart {
      height: 40px;
      display: flex;
      align-items: flex-end;
      gap: 2px;
      margin-top: 16px;
      padding-top: 16px;
      border-top: 1px solid #e5e7eb;
    }

    .history-bar {
      flex: 1;
      background: #667eea;
      border-radius: 2px 2px 0 0;
      transition: height 0.3s;
      opacity: 0.6;
    }

    .footer {
      background: #f9fafb;
      padding: 8px 16px;
      border-radius: 0 0 12px 12px;
      font-size: 11px;
      color: #6b7280;
      text-align: center;
      border-top: 1px solid #e5e7eb;
    }

    .icon {
      width: 16px;
      height: 16px;
      display: inline-block;
    }

    .trend-up { color: #10b981; }
    .trend-down { color: #ef4444; }
    .trend-stable { color: #6b7280; }
  `;

  const icons = {
    activity: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg>',
    minimize: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"></line></svg>',
    expand: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 3 21 3 21 9"></polyline><polyline points="9 21 3 21 3 15"></polyline></svg>',
    close: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>',
    trendUp: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline></svg>',
    trendDown: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 18 13.5 8.5 8.5 13.5 1 6"></polyline></svg>',
    trendStable: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"></line></svg>'
  };

  function getScoreColor(score: number): string {
    if (score >= 0.8) return 'score-green';
    if (score >= 0.6) return 'score-yellow';
    if (score >= 0.4) return 'score-orange';
    return 'score-red';
  }

  function getTrendIcon(trend: string): string {
    switch (trend) {
      case 'improving': return `<span class="icon trend-up">${icons.trendUp}</span>`;
      case 'declining': return `<span class="icon trend-down">${icons.trendDown}</span>`;
      default: return `<span class="icon trend-stable">${icons.trendStable}</span>`;
    }
  }

  function render() {
    if (!shadowRoot || !currentAnalysis) return;

    const html = `
      <div class="widget-container ${isMinimized ? 'minimized' : ''}">
        <div class="widget-header">
          <div class="widget-title">
            <span class="icon">${icons.activity}</span>
            <span>GCT Monitor</span>
          </div>
          <div class="widget-controls">
            <button class="widget-btn" id="minimize-btn">
              <span class="icon">${isMinimized ? icons.expand : icons.minimize}</span>
            </button>
            <button class="widget-btn" id="close-btn">
              <span class="icon">${icons.close}</span>
            </button>
          </div>
        </div>
        
        <div class="widget-body ${isMinimized ? 'hidden' : ''}">
          <div class="score-main">
            <div class="score-value ${getScoreColor(currentAnalysis.metrics.overall)}">
              ${(currentAnalysis.metrics.overall * 100).toFixed(0)}%
            </div>
            <div class="score-label">
              Coherence ${getTrendIcon(currentAnalysis.insights.trajectory)}
            </div>
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

          ${currentAnalysis.insights.strengths.length > 0 || currentAnalysis.insights.concerns.length > 0 ? `
            <div class="insights">
              ${currentAnalysis.insights.strengths.length > 0 ? `
                <div class="insights-title">Strengths</div>
                ${currentAnalysis.insights.strengths.map(s => 
                  `<div class="insight-item strength">${s}</div>`
                ).join('')}
              ` : ''}
              
              ${currentAnalysis.insights.concerns.length > 0 ? `
                <div class="insights-title" style="margin-top: 8px;">Areas to Improve</div>
                ${currentAnalysis.insights.concerns.map(c => 
                  `<div class="insight-item concern">${c}</div>`
                ).join('')}
              ` : ''}
            </div>
          ` : ''}

          ${history.length > 1 ? `
            <div class="history-chart">
              ${history.slice(-20).map(h => 
                `<div class="history-bar" style="height: ${h.metrics.overall * 100}%"></div>`
              ).join('')}
            </div>
          ` : ''}
        </div>

        <div class="footer ${isMinimized ? 'hidden' : ''}">
          Confidence: ${(currentAnalysis.metrics.confidence * 100).toFixed(0)}%
        </div>
      </div>
    `;

    shadowRoot.innerHTML = `
      <style>${styles}</style>
      ${html}
    `;

    // Add event listeners
    const minimizeBtn = shadowRoot.getElementById('minimize-btn');
    const closeBtn = shadowRoot.getElementById('close-btn');

    if (minimizeBtn) {
      minimizeBtn.addEventListener('click', () => {
        isMinimized = !isMinimized;
        render();
      });
    }

    if (closeBtn) {
      closeBtn.addEventListener('click', () => {
        hide();
      });
    }
  }

  function inject() {
    // Create container
    container = document.createElement('div');
    container.id = 'gct-coherence-widget';
    container.style.position = 'fixed';
    container.style.zIndex = '999999';
    document.body.appendChild(container);

    // Create shadow root for style isolation
    shadowRoot = container.attachShadow({ mode: 'open' });
  }

  function update(analysis: AnalysisResult) {
    currentAnalysis = analysis;
    history.push(analysis);
    if (history.length > 50) {
      history.shift();
    }
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

  function destroy() {
    if (container) {
      container.remove();
    }
  }

  return {
    inject,
    update,
    show,
    hide,
    destroy
  };
}