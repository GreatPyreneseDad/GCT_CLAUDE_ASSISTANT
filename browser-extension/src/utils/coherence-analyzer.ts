/**
 * Real-time coherence analyzer for LLM outputs
 * Evaluates text using GCT principles
 */

export interface CoherenceMetrics {
  psi: number;      // Internal consistency
  rho: number;      // Wisdom/learning integration
  q: number;        // Actionability/practical value
  f: number;        // Social/relational awareness
  overall: number;  // Composite coherence score
  confidence: number;
}

export interface AnalysisResult {
  metrics: CoherenceMetrics;
  insights: {
    strengths: string[];
    concerns: string[];
    trajectory: 'improving' | 'stable' | 'declining';
  };
  timestamp: number;
}

export class CoherenceAnalyzer {
  private history: AnalysisResult[] = [];
  private readonly maxHistory = 50;

  /**
   * Analyze a single LLM response for coherence
   */
  analyzeResponse(text: string, context?: string): AnalysisResult {
    const metrics = this.calculateMetrics(text, context);
    const insights = this.generateInsights(metrics, text);
    
    const result: AnalysisResult = {
      metrics,
      insights,
      timestamp: Date.now()
    };

    // Add to history for trajectory analysis
    this.history.push(result);
    if (this.history.length > this.maxHistory) {
      this.history.shift();
    }

    return result;
  }

  /**
   * Calculate GCT metrics from text
   */
  private calculateMetrics(text: string, context?: string): CoherenceMetrics {
    // Internal Consistency (Ψ) - Check for contradictions, logical flow
    const psi = this.calculateInternalConsistency(text);
    
    // Wisdom Integration (ρ) - References to learning, growth, adaptation
    const rho = this.calculateWisdomIntegration(text);
    
    // Actionability (q) - Practical advice, clear steps, problem-solving
    const q = this.calculateActionability(text);
    
    // Social Awareness (f) - Consideration of others, relational understanding
    const f = this.calculateSocialAwareness(text);
    
    // Calculate overall coherence using GCT formula
    const overall = this.calculateOverallCoherence(psi, rho, q, f);
    
    // Confidence based on text length and complexity
    const confidence = Math.min(1, text.length / 500) * 0.8 + 0.2;

    return { psi, rho, q, f, overall, confidence };
  }

  private calculateInternalConsistency(text: string): number {
    let score = 0.7; // Base score

    // Check for contradiction indicators
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

    // Check for logical connectors (positive signal)
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

    // Check for consistent terminology
    const sentences = text.split(/[.!?]+/);
    if (sentences.length > 1) {
      const keywords = this.extractKeywords(text);
      const keywordConsistency = this.measureKeywordConsistency(sentences, keywords);
      score = score * 0.7 + keywordConsistency * 0.3;
    }

    return Math.max(0, Math.min(1, score));
  }

  private calculateWisdomIntegration(text: string): number {
    let score = 0.5; // Base score

    // Patterns indicating learning and growth
    const wisdomPatterns = [
      /learn|learned|learning|understand|understanding|realize|realized/gi,
      /experience|experienced|insight|perspective|wisdom/gi,
      /grow|growth|develop|evolve|improve|progress/gi,
      /reflect|reflection|consider|reconsider|rethink/gi
    ];

    for (const pattern of wisdomPatterns) {
      const matches = text.match(pattern);
      if (matches) {
        score += matches.length * 0.08;
      }
    }

    // Check for nuanced thinking
    const nuancePatterns = [
      /it depends|context matters|in some cases|generally|typically/gi,
      /multiple factors|various aspects|different perspectives/gi
    ];

    for (const pattern of nuancePatterns) {
      const matches = text.match(pattern);
      if (matches) {
        score += matches.length * 0.06;
      }
    }

    return Math.max(0, Math.min(1, score));
  }

  private calculateActionability(text: string): number {
    let score = 0.5; // Base score

    // Action-oriented patterns
    const actionPatterns = [
      /you can|you should|try to|consider|I recommend|I suggest/gi,
      /step \d|first|next|then|finally|to do this/gi,
      /example|for instance|specifically|in practice|practically/gi,
      /solution|solve|approach|method|technique|strategy/gi
    ];

    for (const pattern of actionPatterns) {
      const matches = text.match(pattern);
      if (matches) {
        score += matches.length * 0.07;
      }
    }

    // Check for specific, concrete language
    const specificityPatterns = [
      /\d+|percent|percentage|number|amount|quantity/gi,
      /specific|particular|exact|precise|clear|concrete/gi
    ];

    for (const pattern of specificityPatterns) {
      const matches = text.match(pattern);
      if (matches) {
        score += matches.length * 0.04;
      }
    }

    return Math.max(0, Math.min(1, score));
  }

  private calculateSocialAwareness(text: string): number {
    let score = 0.5; // Base score

    // Social consideration patterns
    const socialPatterns = [
      /people|person|individual|everyone|someone|others/gi,
      /community|society|group|team|together|collective/gi,
      /relationship|connection|communication|interaction/gi,
      /empathy|understand|perspective|feeling|emotion/gi,
      /help|support|assist|collaborate|cooperate/gi
    ];

    for (const pattern of socialPatterns) {
      const matches = text.match(pattern);
      if (matches) {
        score += matches.length * 0.06;
      }
    }

    // Check for inclusive language
    const inclusivePatterns = [
      /we|us|our|together|collectively|shared/gi,
      /diverse|different|various|multiple perspectives/gi
    ];

    for (const pattern of inclusivePatterns) {
      const matches = text.match(pattern);
      if (matches) {
        score += matches.length * 0.05;
      }
    }

    return Math.max(0, Math.min(1, score));
  }

  private calculateOverallCoherence(psi: number, rho: number, q: number, f: number): number {
    // GCT formula: C = ψ + (ρ × ψ) + q + (f × ψ)
    const coherence = psi + (rho * psi) + q + (f * psi);
    // Normalize to 0-1 range (max theoretical value is 4)
    return coherence / 4;
  }

  private generateInsights(metrics: CoherenceMetrics, text: string): AnalysisResult['insights'] {
    const strengths: string[] = [];
    const concerns: string[] = [];

    // Analyze strengths
    if (metrics.psi > 0.7) strengths.push('Highly consistent and logical');
    if (metrics.rho > 0.7) strengths.push('Shows wisdom and learning');
    if (metrics.q > 0.7) strengths.push('Provides actionable guidance');
    if (metrics.f > 0.7) strengths.push('Socially aware and considerate');

    // Analyze concerns
    if (metrics.psi < 0.4) concerns.push('Contains contradictions or unclear logic');
    if (metrics.rho < 0.4) concerns.push('Lacks depth or learning integration');
    if (metrics.q < 0.4) concerns.push('Too abstract or impractical');
    if (metrics.f < 0.4) concerns.push('Limited social consideration');

    // Determine trajectory
    const trajectory = this.analyzeTrajectory();

    return { strengths, concerns, trajectory };
  }

  private analyzeTrajectory(): 'improving' | 'stable' | 'declining' {
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

  private extractKeywords(text: string): string[] {
    // Simple keyword extraction
    const words = text.toLowerCase().match(/\b\w{4,}\b/g) || [];
    const wordFreq = new Map<string, number>();
    
    for (const word of words) {
      wordFreq.set(word, (wordFreq.get(word) || 0) + 1);
    }

    return Array.from(wordFreq.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10)
      .map(([word]) => word);
  }

  private measureKeywordConsistency(sentences: string[], keywords: string[]): number {
    let consistencyScore = 0;
    const keywordUsage = new Map<string, number>();

    for (const sentence of sentences) {
      const sentenceLower = sentence.toLowerCase();
      for (const keyword of keywords) {
        if (sentenceLower.includes(keyword)) {
          keywordUsage.set(keyword, (keywordUsage.get(keyword) || 0) + 1);
        }
      }
    }

    // Calculate consistency based on keyword distribution
    const usedKeywords = Array.from(keywordUsage.values());
    if (usedKeywords.length > 0) {
      const avgUsage = usedKeywords.reduce((a, b) => a + b, 0) / usedKeywords.length;
      const variance = usedKeywords.reduce((acc, val) => acc + Math.pow(val - avgUsage, 2), 0) / usedKeywords.length;
      consistencyScore = 1 - Math.min(1, variance / avgUsage);
    }

    return consistencyScore;
  }

  /**
   * Get conversation-level metrics
   */
  getConversationMetrics(): {
    averageCoherence: number;
    trend: 'improving' | 'stable' | 'declining';
    volatility: number;
  } {
    if (this.history.length === 0) {
      return { averageCoherence: 0, trend: 'stable', volatility: 0 };
    }

    const scores = this.history.map(h => h.metrics.overall);
    const averageCoherence = scores.reduce((a, b) => a + b, 0) / scores.length;
    
    // Calculate volatility (standard deviation)
    const variance = scores.reduce((acc, val) => acc + Math.pow(val - averageCoherence, 2), 0) / scores.length;
    const volatility = Math.sqrt(variance);

    const trend = this.analyzeTrajectory();

    return { averageCoherence, trend, volatility };
  }

  /**
   * Reset analysis history
   */
  reset(): void {
    this.history = [];
  }
}