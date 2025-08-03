# Coherence-AI Interaction Modeling
# Tracks how AI interactions affect human coherence over time

import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import hashlib

# Import core types
from gct_types import CoherenceProfile, CommunicationAnalysis

class AIInteractionType(Enum):
    INFORMATIONAL = "informational"      # Fact-seeking, knowledge queries
    CREATIVE = "creative"                # Creative collaboration, ideation
    EMOTIONAL = "emotional"              # Emotional support, validation seeking
    DECISION_SUPPORT = "decision"        # Help with decisions, analysis
    SOCIAL_PROXY = "social_proxy"        # Using AI as social interaction substitute
    SELF_REFLECTION = "self_reflection"  # Using AI for self-understanding
    TASK_COMPLETION = "task_completion"  # Delegation of work/thinking

@dataclass
class AIInteraction:
    """Single interaction with an AI system"""
    timestamp: datetime
    interaction_type: AIInteractionType
    duration_minutes: int
    user_coherence_before: float
    user_coherence_after: Optional[float]
    ai_response_coherence: float  # Coherence of AI's response
    dependency_indicators: Dict[str, float]
    authenticity_preserved: bool
    user_satisfaction: Optional[float]

@dataclass
class AICoherenceImpact:
    """Analysis of AI's impact on user coherence"""
    overall_impact: float  # Positive or negative
    variable_impacts: Dict[str, float]  # Impact on each coherence variable
    dependency_score: float  # 0-1, higher = more dependent
    authenticity_drift: float  # How much AI changes authentic expression
    coherence_volatility: float  # Increased variability in coherence
    recommendations: List[str]

class AICoherenceAnalyzer:
    """Analyze how AI interactions affect human coherence"""
    
    def __init__(self):
        self.interaction_patterns = {
            AIInteractionType.INFORMATIONAL: {
                'typical_rho_impact': 0.02,   # Can increase wisdom through learning
                'typical_psi_impact': 0.0,     # Neutral on consistency
                'typical_q_impact': -0.01,     # Slight decrease in activation
                'typical_f_impact': -0.02,     # Reduces human connection time
                'dependency_risk': 0.3
            },
            AIInteractionType.CREATIVE: {
                'typical_rho_impact': 0.01,
                'typical_psi_impact': 0.01,    # Can improve consistency through exploration
                'typical_q_impact': -0.02,     # May reduce independent moral activation
                'typical_f_impact': -0.01,
                'dependency_risk': 0.5
            },
            AIInteractionType.EMOTIONAL: {
                'typical_rho_impact': -0.02,   # May prevent real emotional processing
                'typical_psi_impact': -0.03,   # Can create false consistency
                'typical_q_impact': -0.04,     # Reduces real-world activation
                'typical_f_impact': -0.05,     # Major risk to social belonging
                'dependency_risk': 0.8
            },
            AIInteractionType.DECISION_SUPPORT: {
                'typical_rho_impact': -0.03,   # Reduces independent wisdom building
                'typical_psi_impact': 0.02,    # Can improve decision consistency
                'typical_q_impact': -0.03,     # Reduces autonomous moral reasoning
                'typical_f_impact': -0.01,
                'dependency_risk': 0.7
            },
            AIInteractionType.SOCIAL_PROXY: {
                'typical_rho_impact': -0.04,
                'typical_psi_impact': -0.04,
                'typical_q_impact': -0.05,
                'typical_f_impact': -0.08,     # Severe impact on real belonging
                'dependency_risk': 0.9
            },
            AIInteractionType.SELF_REFLECTION: {
                'typical_rho_impact': 0.03,    # Can enhance self-understanding
                'typical_psi_impact': 0.04,    # Improves self-consistency awareness
                'typical_q_impact': 0.01,
                'typical_f_impact': 0.0,
                'dependency_risk': 0.4
            },
            AIInteractionType.TASK_COMPLETION: {
                'typical_rho_impact': -0.04,   # Reduces learning opportunities
                'typical_psi_impact': -0.02,
                'typical_q_impact': -0.03,
                'typical_f_impact': -0.02,
                'dependency_risk': 0.6
            }
        }
        
        # Threshold effects
        self.dependency_thresholds = {
            'low': 0.3,
            'moderate': 0.5,
            'high': 0.7,
            'severe': 0.85
        }
    
    def classify_interaction(self, 
                           conversation_text: str,
                           user_intent: Optional[str] = None) -> AIInteractionType:
        """
        Classify the type of AI interaction based on content
        """
        text_lower = conversation_text.lower()
        
        # Keywords for each interaction type
        emotional_keywords = ['feel', 'feeling', 'upset', 'anxious', 'depressed', 'lonely', 
                            'scared', 'worried', 'comfort', 'support', 'understand me']
        decision_keywords = ['should i', 'what do you think', 'help me decide', 'which option',
                           'pros and cons', 'recommend', 'advise', 'best choice']
        creative_keywords = ['create', 'generate', 'imagine', 'design', 'brainstorm', 
                           'idea', 'innovative', 'creative', 'invent']
        social_keywords = ['friend', 'talk to me', 'conversation', 'chat', 'companion',
                         'someone to talk to', 'discuss', 'share with you']
        reflection_keywords = ['understand myself', 'who am i', 'my values', 'self-discovery',
                             'personal growth', 'analyze my', 'pattern in my']
        task_keywords = ['do this for me', 'complete', 'write my', 'finish my', 
                       'handle this', 'take care of', 'automate']
        
        # Count keyword matches
        keyword_counts = {
            AIInteractionType.EMOTIONAL: sum(1 for k in emotional_keywords if k in text_lower),
            AIInteractionType.DECISION_SUPPORT: sum(1 for k in decision_keywords if k in text_lower),
            AIInteractionType.CREATIVE: sum(1 for k in creative_keywords if k in text_lower),
            AIInteractionType.SOCIAL_PROXY: sum(1 for k in social_keywords if k in text_lower),
            AIInteractionType.SELF_REFLECTION: sum(1 for k in reflection_keywords if k in text_lower),
            AIInteractionType.TASK_COMPLETION: sum(1 for k in task_keywords if k in text_lower),
        }
        
        # Get type with most keyword matches
        max_type = max(keyword_counts.items(), key=lambda x: x[1])
        
        # Default to informational if no strong signal
        if max_type[1] == 0:
            return AIInteractionType.INFORMATIONAL
        
        return max_type[0]
    
    def analyze_interaction_impact(self,
                                 interaction_type: AIInteractionType,
                                 duration_minutes: int,
                                 ai_response_analysis: CommunicationAnalysis,
                                 user_profile_before: CoherenceProfile) -> Dict[str, float]:
        """
        Predict the impact of a specific AI interaction on user coherence
        """
        base_impacts = self.interaction_patterns[interaction_type]
        
        # Adjust impacts based on duration (longer = stronger effect)
        duration_multiplier = min(duration_minutes / 30, 2.0)  # Cap at 2x for long conversations
        
        # Adjust based on AI response coherence
        ai_coherence_modifier = ai_response_analysis.authenticity_score - 0.5  # -0.5 to 0.5
        
        # Calculate variable-specific impacts
        impacts = {}
        impacts['psi'] = base_impacts['typical_psi_impact'] * duration_multiplier * (1 + ai_coherence_modifier)
        impacts['rho'] = base_impacts['typical_rho_impact'] * duration_multiplier * (1 + ai_coherence_modifier)
        impacts['q'] = base_impacts['typical_q_impact'] * duration_multiplier
        impacts['f'] = base_impacts['typical_f_impact'] * duration_multiplier
        
        # Dependency accumulation
        impacts['dependency'] = base_impacts['dependency_risk'] * (duration_minutes / 60)
        
        # Check for concerning patterns
        if interaction_type == AIInteractionType.EMOTIONAL and duration_minutes > 60:
            # Long emotional support sessions create stronger negative impacts
            impacts['f'] *= 1.5
            impacts['dependency'] *= 1.5
        
        if interaction_type == AIInteractionType.DECISION_SUPPORT and user_profile_before.variables.rho < 0.4:
            # Low-wisdom users are more negatively affected by decision outsourcing
            impacts['rho'] *= 1.5
            
        return impacts
    
    def track_cumulative_impact(self,
                              interaction_history: List[AIInteraction],
                              initial_profile: CoherenceProfile,
                              current_profile: CoherenceProfile) -> AICoherenceImpact:
        """
        Analyze cumulative impact of AI interactions on coherence
        """
        if not interaction_history:
            return AICoherenceImpact(
                overall_impact=0,
                variable_impacts={},
                dependency_score=0,
                authenticity_drift=0,
                coherence_volatility=0,
                recommendations=["No AI interactions to analyze"]
            )
        
        # Calculate total impacts
        cumulative_impacts = {'psi': 0, 'rho': 0, 'q': 0, 'f': 0, 'dependency': 0}
        interaction_types_count = {}
        
        for interaction in interaction_history:
            impacts = self.analyze_interaction_impact(
                interaction.interaction_type,
                interaction.duration_minutes,
                CommunicationAnalysis(
                    text="",
                    consistency_score=0.5,
                    wisdom_indicators=0.5,
                    moral_activation=0.5,
                    social_awareness=0.5,
                    authenticity_score=interaction.ai_response_coherence,
                    red_flags=[],
                    enhancement_suggestions=[],
                    confidence_level=0.8
                ),
                initial_profile
            )
            
            for key in cumulative_impacts:
                cumulative_impacts[key] += impacts.get(key, 0)
            
            # Track interaction types
            interaction_types_count[interaction.interaction_type] = \
                interaction_types_count.get(interaction.interaction_type, 0) + 1
        
        # Calculate actual vs predicted changes
        actual_changes = {
            'psi': current_profile.variables.psi - initial_profile.variables.psi,
            'rho': current_profile.variables.rho - initial_profile.variables.rho,
            'q': current_profile.variables.q - initial_profile.variables.q,
            'f': current_profile.variables.f - initial_profile.variables.f,
        }
        
        # Calculate overall impact
        overall_impact = current_profile.static_coherence - initial_profile.static_coherence
        
        # Calculate dependency score
        total_interactions = len(interaction_history)
        days_span = (interaction_history[-1].timestamp - interaction_history[0].timestamp).days + 1
        interactions_per_day = total_interactions / days_span if days_span > 0 else total_interactions
        
        dependency_score = min(1.0, cumulative_impacts['dependency'] / total_interactions)
        
        # Adjust for frequency
        if interactions_per_day > 5:
            dependency_score = min(1.0, dependency_score * 1.5)
        
        # Calculate authenticity drift
        authenticity_preserving_types = [AIInteractionType.SELF_REFLECTION, AIInteractionType.INFORMATIONAL]
        authenticity_reducing_types = [AIInteractionType.EMOTIONAL, AIInteractionType.SOCIAL_PROXY]
        
        preserving_count = sum(interaction_types_count.get(t, 0) for t in authenticity_preserving_types)
        reducing_count = sum(interaction_types_count.get(t, 0) for t in authenticity_reducing_types)
        
        authenticity_drift = (reducing_count - preserving_count) / total_interactions if total_interactions > 0 else 0
        
        # Calculate coherence volatility
        if len(interaction_history) > 10:
            coherence_values = [i.user_coherence_before for i in interaction_history if i.user_coherence_before]
            coherence_volatility = np.std(coherence_values) if coherence_values else 0
        else:
            coherence_volatility = 0
        
        # Generate recommendations
        recommendations = self._generate_ai_usage_recommendations(
            dependency_score,
            authenticity_drift,
            interaction_types_count,
            actual_changes
        )
        
        return AICoherenceImpact(
            overall_impact=overall_impact,
            variable_impacts=actual_changes,
            dependency_score=dependency_score,
            authenticity_drift=authenticity_drift,
            coherence_volatility=coherence_volatility,
            recommendations=recommendations
        )
    
    def _generate_ai_usage_recommendations(self,
                                         dependency_score: float,
                                         authenticity_drift: float,
                                         interaction_types: Dict[AIInteractionType, int],
                                         coherence_changes: Dict[str, float]) -> List[str]:
        """
        Generate specific recommendations for healthier AI interaction
        """
        recommendations = []
        
        # Dependency-based recommendations
        if dependency_score > self.dependency_thresholds['high']:
            recommendations.append("⚠️ High AI dependency detected - schedule AI-free days")
            recommendations.append("Practice making decisions without AI consultation for 48 hours")
        elif dependency_score > self.dependency_thresholds['moderate']:
            recommendations.append("Moderate AI reliance - balance with human interactions")
        
        # Authenticity recommendations
        if authenticity_drift > 0.3:
            recommendations.append("AI interactions may be reducing authentic self-expression")
            recommendations.append("Spend time journaling without AI to reconnect with your voice")
        elif authenticity_drift < -0.2:
            recommendations.append("Good job using AI for self-reflection rather than replacement")
        
        # Type-specific recommendations
        total_interactions = sum(interaction_types.values())
        if total_interactions > 0:
            # Check for problematic patterns
            emotional_percent = interaction_types.get(AIInteractionType.EMOTIONAL, 0) / total_interactions
            social_percent = interaction_types.get(AIInteractionType.SOCIAL_PROXY, 0) / total_interactions
            decision_percent = interaction_types.get(AIInteractionType.DECISION_SUPPORT, 0) / total_interactions
            
            if emotional_percent > 0.3:
                recommendations.append("High emotional AI use - consider human support or therapy")
                recommendations.append("AI cannot replace genuine emotional connection")
            
            if social_percent > 0.2:
                recommendations.append("Using AI as social proxy - seek real human connections")
                recommendations.append("Join a group activity this week to practice authentic belonging")
            
            if decision_percent > 0.4:
                recommendations.append("Over-reliance on AI for decisions - trust your own judgment more")
                recommendations.append("Make your next 3 decisions without AI input")
        
        # Coherence-specific recommendations
        if coherence_changes['rho'] < -0.1:
            recommendations.append("AI use is reducing wisdom accumulation - embrace difficult experiences")
        
        if coherence_changes['f'] < -0.1:
            recommendations.append("AI interactions are impacting social belonging - prioritize human time")
        
        if coherence_changes['q'] < -0.1:
            recommendations.append("Moral activation declining - take real-world action on your values")
        
        # Positive reinforcement
        if dependency_score < self.dependency_thresholds['low'] and authenticity_drift < 0.1:
            recommendations.append("✓ Healthy AI usage pattern - maintaining good boundaries")
        
        return recommendations
    
    def predict_ai_coherence_trajectory(self,
                                      current_profile: CoherenceProfile,
                                      planned_ai_usage: Dict[AIInteractionType, int],
                                      days_forward: int = 30) -> Dict[str, any]:
        """
        Predict how planned AI usage will affect coherence over time
        """
        # Calculate daily impacts
        daily_impacts = {'psi': 0, 'rho': 0, 'q': 0, 'f': 0}
        daily_dependency_increase = 0
        
        for interaction_type, daily_count in planned_ai_usage.items():
            type_impacts = self.interaction_patterns[interaction_type]
            
            # Assume 30-minute average interactions
            for var in ['psi', 'rho', 'q', 'f']:
                key = f'typical_{var}_impact'
                daily_impacts[var] += type_impacts[key] * daily_count
            
            daily_dependency_increase += type_impacts['dependency_risk'] * daily_count * 0.1
        
        # Project forward
        projected_profile = CoherenceProfile(
            user_id=current_profile.user_id,
            variables=CoherenceVariables(
                psi=max(0, min(1, current_profile.variables.psi + daily_impacts['psi'] * days_forward)),
                rho=max(0, min(1, current_profile.variables.rho + daily_impacts['rho'] * days_forward)),
                q=max(0, min(1, current_profile.variables.q + daily_impacts['q'] * days_forward)),
                f=max(0, min(1, current_profile.variables.f + daily_impacts['f'] * days_forward))
            ),
            static_coherence=0,  # Will calculate
            assessment_tier=current_profile.assessment_tier
        )
        
        # Recalculate coherence
        projected_profile.static_coherence = (
            projected_profile.variables.psi + 
            (projected_profile.variables.rho * projected_profile.variables.psi) + 
            projected_profile.variables.q + 
            (projected_profile.variables.f * projected_profile.variables.psi)
        )
        
        # Calculate risks
        projected_dependency = min(1.0, daily_dependency_increase * days_forward)
        coherence_change = projected_profile.static_coherence - current_profile.static_coherence
        
        # Generate warnings
        warnings = []
        if projected_dependency > 0.7:
            warnings.append("High risk of AI dependency with this usage pattern")
        
        if coherence_change < -0.3:
            warnings.append("Significant coherence decline predicted")
        
        if projected_profile.variables.f < 0.3:
            warnings.append("Social belonging at risk - increase human interaction")
        
        return {
            'current_coherence': current_profile.static_coherence,
            'projected_coherence': projected_profile.static_coherence,
            'coherence_change': coherence_change,
            'projected_dependency': projected_dependency,
            'variable_changes': {
                'psi': projected_profile.variables.psi - current_profile.variables.psi,
                'rho': projected_profile.variables.rho - current_profile.variables.rho,
                'q': projected_profile.variables.q - current_profile.variables.q,
                'f': projected_profile.variables.f - current_profile.variables.f,
            },
            'warnings': warnings,
            'recommendation': self._generate_usage_optimization(planned_ai_usage, daily_impacts)
        }
    
    def _generate_usage_optimization(self,
                                   planned_usage: Dict[AIInteractionType, int],
                                   daily_impacts: Dict[str, float]) -> str:
        """
        Suggest optimized AI usage pattern
        """
        total_daily_interactions = sum(planned_usage.values())
        
        if total_daily_interactions > 10:
            return "Reduce total AI interactions to under 5 per day for healthier balance"
        
        # Find most problematic interaction types
        negative_types = []
        for itype, count in planned_usage.items():
            if count > 0:
                pattern = self.interaction_patterns[itype]
                total_negative = sum(pattern[f'typical_{var}_impact'] for var in ['psi', 'rho', 'q', 'f'] 
                                   if pattern[f'typical_{var}_impact'] < 0)
                if total_negative < -0.05:
                    negative_types.append((itype, total_negative))
        
        if negative_types:
            worst_type = min(negative_types, key=lambda x: x[1])[0]
            return f"Reduce {worst_type.value} interactions - highest negative impact on coherence"
        
        return "Current AI usage pattern is relatively balanced - maintain awareness"