export interface CoherenceVariables {
  psi: number;  // Internal Consistency
  rho: number;  // Accumulated Wisdom
  q: number;    // Moral Activation Energy
  f: number;    // Social Belonging Architecture
}

export interface CoherenceProfile {
  user_id: string;
  variables: CoherenceVariables;
  static_coherence: number;
  coherence_velocity?: number;
  assessment_tier: 'basic' | 'professional' | 'advanced';
  timestamp: string;
  individual_optimization?: Record<string, number>;
  insights?: AssessmentInsights;
}

export interface AssessmentInsights {
  overall_coherence_level: 'high' | 'moderate' | 'developing';
  strongest_area: string;
  development_area: string;
  key_recommendations: string[];
  leadership_readiness?: 'high' | 'moderate' | 'developing';
  innovation_timing?: string;
}

export interface CommunicationAnalysis {
  consistency_score: number;
  wisdom_indicators: number;
  moral_activation: number;
  social_awareness: number;
  authenticity_score: number;
  red_flags: string[];
  enhancement_suggestions: string[];
  confidence_level: number;
}

export interface RelationshipAnalysis {
  overall_compatibility: number;
  variable_compatibility: {
    internal_consistency: number;
    accumulated_wisdom: number;
    moral_activation: number;
    social_belonging: number;
  };
  transmission_dynamics: {
    a_to_b_influence: number;
    b_to_a_influence: number;
    influence_asymmetry: number;
    dominant_influencer: 'A' | 'B';
    mutual_influence: number;
  };
  growth_opportunities: string[];
  potential_conflicts: string[];
  relationship_recommendations: string[];
}