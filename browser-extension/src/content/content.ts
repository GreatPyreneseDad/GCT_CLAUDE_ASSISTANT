/**
 * Content script that monitors LLM responses and displays coherence metrics
 */

import { CoherenceAnalyzer } from '../utils/coherence-analyzer';
import { createCoherenceWidget } from './widget';
import { LLMDetector } from './llm-detector';

class CoherenceMonitor {
  private analyzer: CoherenceAnalyzer;
  private widget: ReturnType<typeof createCoherenceWidget>;
  private detector: LLMDetector;
  private observer: MutationObserver | null = null;
  private lastAnalyzedText: string = '';
  private isEnabled: boolean = true;

  constructor() {
    this.analyzer = new CoherenceAnalyzer();
    this.detector = new LLMDetector();
    this.widget = createCoherenceWidget();
    this.init();
  }

  private async init() {
    // Check if extension is enabled
    const settings = await chrome.storage.sync.get(['enabled']);
    this.isEnabled = settings.enabled !== false;

    if (!this.isEnabled) return;

    // Detect which LLM platform we're on
    const platform = this.detector.detectPlatform();
    if (!platform) {
      console.log('GCT Monitor: Not on a supported LLM platform');
      return;
    }

    console.log(`GCT Monitor: Detected ${platform} platform`);

    // Inject widget into page
    this.widget.inject();

    // Start monitoring for new messages
    this.startMonitoring(platform);

    // Listen for settings changes
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

  private startMonitoring(platform: string) {
    // Stop any existing observer
    this.stopMonitoring();

    // Get the appropriate selector for the platform
    const selector = this.detector.getMessageSelector(platform);
    if (!selector) return;

    // Create mutation observer to watch for new messages
    this.observer = new MutationObserver((mutations) => {
      for (const mutation of mutations) {
        if (mutation.type === 'childList') {
          // Check for new LLM messages
          const newMessages = this.findNewLLMMessages(mutation.addedNodes, selector);
          newMessages.forEach(msg => this.analyzeMessage(msg));
        }
      }
    });

    // Start observing
    const targetNode = document.body;
    this.observer.observe(targetNode, {
      childList: true,
      subtree: true
    });

    // Analyze existing messages
    const existingMessages = document.querySelectorAll(selector);
    const lastMessage = existingMessages[existingMessages.length - 1];
    if (lastMessage) {
      this.analyzeMessage(lastMessage as HTMLElement);
    }
  }

  private stopMonitoring() {
    if (this.observer) {
      this.observer.disconnect();
      this.observer = null;
    }
  }

  private findNewLLMMessages(nodes: NodeList, selector: string): HTMLElement[] {
    const messages: HTMLElement[] = [];
    
    nodes.forEach(node => {
      if (node.nodeType === Node.ELEMENT_NODE) {
        const element = node as HTMLElement;
        
        // Check if this node matches our selector
        if (element.matches(selector)) {
          messages.push(element);
        }
        
        // Check descendants
        const descendantMessages = element.querySelectorAll(selector);
        descendantMessages.forEach(msg => messages.push(msg as HTMLElement));
      }
    });

    return messages;
  }

  private analyzeMessage(element: HTMLElement) {
    const text = element.textContent || '';
    
    // Skip if too short or same as last analyzed
    if (text.length < 50 || text === this.lastAnalyzedText) return;
    
    this.lastAnalyzedText = text;

    // Get context (previous message if available)
    const context = this.getPreviousMessage(element);

    // Analyze coherence
    const result = this.analyzer.analyzeResponse(text, context);

    // Update widget
    this.widget.update(result);

    // Store analysis for popup
    this.storeAnalysis(result);

    // Add visual indicator to the message
    this.addCoherenceIndicator(element, result.metrics.overall);
  }

  private getPreviousMessage(element: HTMLElement): string | undefined {
    // Try to find the previous message in the conversation
    const allMessages = Array.from(document.querySelectorAll(
      this.detector.getMessageSelector(this.detector.detectPlatform() || '') || ''
    ));
    
    const currentIndex = allMessages.indexOf(element);
    if (currentIndex > 0) {
      const prevElement = allMessages[currentIndex - 1] as HTMLElement;
      return prevElement.textContent || undefined;
    }
    
    return undefined;
  }

  private addCoherenceIndicator(element: HTMLElement, score: number) {
    // Remove any existing indicator
    const existing = element.querySelector('.gct-indicator');
    if (existing) existing.remove();

    // Create indicator
    const indicator = document.createElement('div');
    indicator.className = 'gct-indicator';
    indicator.style.cssText = `
      position: absolute;
      top: 8px;
      right: 8px;
      width: 12px;
      height: 12px;
      border-radius: 50%;
      background: ${this.getScoreColor(score)};
      opacity: 0.8;
      cursor: pointer;
      z-index: 10;
    `;
    
    indicator.title = `Coherence: ${(score * 100).toFixed(0)}%`;
    
    // Make parent relative if needed
    if (getComputedStyle(element).position === 'static') {
      element.style.position = 'relative';
    }
    
    element.appendChild(indicator);
  }

  private getScoreColor(score: number): string {
    if (score >= 0.8) return '#10b981'; // Green
    if (score >= 0.6) return '#f59e0b'; // Yellow
    if (score >= 0.4) return '#f97316'; // Orange
    return '#ef4444'; // Red
  }

  private async storeAnalysis(result: any) {
    // Store recent analyses for the popup
    const storage = await chrome.storage.local.get(['analyses']);
    const analyses = storage.analyses || [];
    
    analyses.push({
      ...result,
      url: window.location.href,
      platform: this.detector.detectPlatform()
    });
    
    // Keep only last 100 analyses
    if (analyses.length > 100) {
      analyses.shift();
    }
    
    await chrome.storage.local.set({ analyses });
  }
}

// Initialize monitor when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => new CoherenceMonitor());
} else {
  new CoherenceMonitor();
}