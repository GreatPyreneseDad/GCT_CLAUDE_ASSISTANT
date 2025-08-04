/**
 * Detects which LLM platform we're on and provides appropriate selectors
 */

export class LLMDetector {
  private platforms = {
    chatgpt: {
      urlPattern: /chat\.openai\.com/,
      messageSelector: '[data-message-author-role="assistant"]',
      containerSelector: '.flex.flex-col.items-start',
      name: 'ChatGPT'
    },
    claude: {
      urlPattern: /claude\.ai/,
      messageSelector: 'div[data-test="assistant-message"]',
      containerSelector: '.prose',
      name: 'Claude'
    },
    bard: {
      urlPattern: /bard\.google\.com/,
      messageSelector: '.model-response-text',
      containerSelector: '.conversation-container',
      name: 'Google Bard'
    },
    gemini: {
      urlPattern: /gemini\.google\.com/,
      messageSelector: '.model-response',
      containerSelector: '.conversation-turn',
      name: 'Google Gemini'
    },
    poe: {
      urlPattern: /poe\.com/,
      messageSelector: '.Message_botMessageBubble__aYctV',
      containerSelector: '.ChatMessageList_container__7M0gM',
      name: 'Poe'
    },
    perplexity: {
      urlPattern: /perplexity\.ai/,
      messageSelector: '.prose.break-words',
      containerSelector: '.flex.flex-col',
      name: 'Perplexity'
    }
  };

  detectPlatform(): string | null {
    const url = window.location.href;
    
    for (const [key, platform] of Object.entries(this.platforms)) {
      if (platform.urlPattern.test(url)) {
        return key;
      }
    }
    
    return null;
  }

  getMessageSelector(platform: string): string | null {
    return this.platforms[platform]?.messageSelector || null;
  }

  getContainerSelector(platform: string): string | null {
    return this.platforms[platform]?.containerSelector || null;
  }

  getPlatformName(platform: string): string {
    return this.platforms[platform]?.name || 'Unknown';
  }

  /**
   * Get all supported platforms
   */
  getSupportedPlatforms(): string[] {
    return Object.values(this.platforms).map(p => p.name);
  }

  /**
   * Check if current page is a supported LLM platform
   */
  isSupported(): boolean {
    return this.detectPlatform() !== null;
  }
}