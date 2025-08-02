# Cross-Cultural Coherence Calibration Module
# Adjusts GCT measurements for cultural context and expression patterns

import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

# Import core types
from gct_backend import CoherenceVariables, CoherenceProfile

class CulturalContext(Enum):
    INDIVIDUALIST_WESTERN = "individualist_western"
    COLLECTIVIST_EASTERN = "collectivist_eastern"
    MEDITERRANEAN = "mediterranean"
    LATIN_AMERICAN = "latin_american"
    NORDIC = "nordic"
    AFRICAN = "african"
    MIDDLE_EASTERN = "middle_eastern"
    INDIGENOUS = "indigenous"
    MULTICULTURAL = "multicultural"

@dataclass
class CulturalCalibration:
    """Cultural adjustment parameters for coherence measurement"""
    context: CulturalContext
    expression_modifiers: Dict[str, float]  # How each variable is expressed
    value_priorities: Dict[str, float]      # Cultural importance of each variable
    communication_style: Dict[str, any]     # Direct vs indirect, etc.
    social_structure: str                   # hierarchical, egalitarian, etc.

class CulturalCoherenceCalibrator:
    """Calibrates coherence measurements for cultural context"""
    
    def __init__(self):
        # Cultural expression patterns
        self.cultural_patterns = {
            CulturalContext.INDIVIDUALIST_WESTERN: {
                'expression_modifiers': {
                    'psi': 1.0,   # Direct expression of consistency expected
                    'rho': 0.9,   # Individual wisdom valued but less collective
                    'q': 1.1,     # High individual moral activation expected
                    'f': 0.8      # Lower collective belonging emphasis
                },
                'value_priorities': {
                    'psi': 0.3,   # Authenticity highly valued
                    'rho': 0.2,   # Individual achievement/learning
                    'q': 0.3,     # Personal responsibility
                    'f': 0.2      # Chosen relationships
                },
                'communication_style': {
                    'directness': 0.8,
                    'emotional_expression': 0.7,
                    'conflict_approach': 'direct',
                    'self_promotion': 0.8
                },
                'social_structure': 'individualist_egalitarian'
            },
            CulturalContext.COLLECTIVIST_EASTERN: {
                'expression_modifiers': {
                    'psi': 0.7,   # Indirect expression, context-dependent
                    'rho': 1.1,   # Collective wisdom highly valued
                    'q': 0.8,     # Group harmony over individual activation
                    'f': 1.3      # Very high belonging emphasis
                },
                'value_priorities': {
                    'psi': 0.2,   # Harmony over individual consistency
                    'rho': 0.3,   # Ancestral and collective wisdom
                    'q': 0.1,     # Measured group-oriented action
                    'f': 0.4      # Group belonging paramount
                },
                'communication_style': {
                    'directness': 0.3,
                    'emotional_expression': 0.4,
                    'conflict_approach': 'indirect',
                    'self_promotion': 0.2
                },
                'social_structure': 'collectivist_hierarchical'
            },
            CulturalContext.MEDITERRANEAN: {
                'expression_modifiers': {
                    'psi': 0.9,
                    'rho': 1.0,
                    'q': 1.0,
                    'f': 1.1
                },
                'value_priorities': {
                    'psi': 0.25,
                    'rho': 0.25,
                    'q': 0.2,
                    'f': 0.3
                },
                'communication_style': {
                    'directness': 0.6,
                    'emotional_expression': 0.9,
                    'conflict_approach': 'passionate',
                    'self_promotion': 0.6
                },
                'social_structure': 'family_centered'
            },
            CulturalContext.LATIN_AMERICAN: {
                'expression_modifiers': {
                    'psi': 0.85,
                    'rho': 0.95,
                    'q': 0.9,
                    'f': 1.2
                },
                'value_priorities': {
                    'psi': 0.2,
                    'rho': 0.25,
                    'q': 0.25,
                    'f': 0.3
                },
                'communication_style': {
                    'directness': 0.5,
                    'emotional_expression': 0.85,
                    'conflict_approach': 'relational',
                    'self_promotion': 0.5
                },
                'social_structure': 'extended_family'
            },
            CulturalContext.NORDIC: {
                'expression_modifiers': {
                    'psi': 1.1,   # Very high consistency expected
                    'rho': 1.0,
                    'q': 0.9,     # Understated moral action
                    'f': 0.9      # Reserved but deep connections
                },
                'value_priorities': {
                    'psi': 0.35,
                    'rho': 0.25,
                    'q': 0.2,
                    'f': 0.2
                },
                'communication_style': {
                    'directness': 0.7,
                    'emotional_expression': 0.3,
                    'conflict_approach': 'pragmatic',
                    'self_promotion': 0.1
                },
                'social_structure': 'egalitarian_reserved'
            },
            CulturalContext.AFRICAN: {
                'expression_modifiers': {
                    'psi': 0.8,
                    'rho': 1.2,   # Ubuntu philosophy - collective wisdom
                    'q': 0.95,
                    'f': 1.3      # Community central
                },
                'value_priorities': {
                    'psi': 0.15,
                    'rho': 0.3,
                    'q': 0.2,
                    'f': 0.35
                },
                'communication_style': {
                    'directness': 0.5,
                    'emotional_expression': 0.8,
                    'conflict_approach': 'communal',
                    'self_promotion': 0.4
                },
                'social_structure': 'ubuntu_communal'
            },
            CulturalContext.MIDDLE_EASTERN: {
                'expression_modifiers': {
                    'psi': 0.85,
                    'rho': 1.1,
                    'q': 1.0,
                    'f': 1.15
                },
                'value_priorities': {
                    'psi': 0.2,
                    'rho': 0.3,
                    'q': 0.25,
                    'f': 0.25
                },
                'communication_style': {
                    'directness': 0.4,
                    'emotional_expression': 0.7,
                    'conflict_approach': 'honor_based',
                    'self_promotion': 0.3
                },
                'social_structure': 'traditional_hierarchical'
            },
            CulturalContext.INDIGENOUS: {
                'expression_modifiers': {
                    'psi': 0.9,
                    'rho': 1.3,   # Deep ancestral wisdom
                    'q': 0.95,
                    'f': 1.2
                },
                'value_priorities': {
                    'psi': 0.2,
                    'rho': 0.35,
                    'q': 0.15,
                    'f': 0.3
                },
                'communication_style': {
                    'directness': 0.4,
                    'emotional_expression': 0.6,
                    'conflict_approach': 'circular',
                    'self_promotion': 0.1
                },
                'social_structure': 'circular_egalitarian'
            },
            CulturalContext.MULTICULTURAL: {
                'expression_modifiers': {
                    'psi': 0.95,
                    'rho': 1.0,
                    'q': 0.95,
                    'f': 1.0
                },
                'value_priorities': {
                    'psi': 0.25,
                    'rho': 0.25,
                    'q': 0.25,
                    'f': 0.25
                },
                'communication_style': {
                    'directness': 0.6,
                    'emotional_expression': 0.6,
                    'conflict_approach': 'adaptive',
                    'self_promotion': 0.5
                },
                'social_structure': 'hybrid_flexible'
            }
        }
        
        # Question interpretation adjustments
        self.question_adjustments = {
            'values_action_alignment': {
                CulturalContext.COLLECTIVIST_EASTERN: 'group_harmony_alignment',
                CulturalContext.AFRICAN: 'community_values_alignment',
                CulturalContext.INDIGENOUS: 'ancestral_values_alignment'
            },
            'moral_action_willingness': {
                CulturalContext.COLLECTIVIST_EASTERN: 'group_benefit_action',
                CulturalContext.NORDIC: 'quiet_principled_action',
                CulturalContext.MEDITERRANEAN: 'family_honor_action'
            },
            'relationship_quality': {
                CulturalContext.INDIVIDUALIST_WESTERN: 'chosen_relationship_depth',
                CulturalContext.COLLECTIVIST_EASTERN: 'role_fulfillment_quality',
                CulturalContext.AFRICAN: 'community_integration_quality'
            }
        }
    
    def calibrate_assessment_questions(self,
                                     standard_questions: List[Dict[str, any]],
                                     cultural_context: CulturalContext) -> List[Dict[str, any]]:
        """
        Adjust assessment questions for cultural appropriateness
        """
        calibrated_questions = []
        
        for question in standard_questions:
            calibrated_q = question.copy()
            
            # Check if this question needs cultural adjustment
            if question['key'] in self.question_adjustments:
                if cultural_context in self.question_adjustments[question['key']]:
                    # Modify the question text and interpretation
                    adjustment_key = self.question_adjustments[question['key']][cultural_context]
                    calibrated_q['cultural_key'] = adjustment_key
                    calibrated_q['text'] = self._get_culturally_adjusted_text(
                        question['key'], 
                        cultural_context
                    )
            
            calibrated_questions.append(calibrated_q)
        
        return calibrated_questions
    
    def calibrate_coherence_measurement(self,
                                      raw_profile: CoherenceProfile,
                                      cultural_context: CulturalContext,
                                      response_style: Optional[Dict[str, float]] = None) -> CoherenceProfile:
        """
        Adjust coherence measurements for cultural expression patterns
        """
        pattern = self.cultural_patterns[cultural_context]
        
        # Apply expression modifiers
        calibrated_variables = CoherenceVariables(
            psi=self._calibrate_variable(raw_profile.variables.psi, 'psi', pattern, response_style),
            rho=self._calibrate_variable(raw_profile.variables.rho, 'rho', pattern, response_style),
            q=self._calibrate_variable(raw_profile.variables.q, 'q', pattern, response_style),
            f=self._calibrate_variable(raw_profile.variables.f, 'f', pattern, response_style)
        )
        
        # Recalculate coherence with cultural weights
        weighted_coherence = self._calculate_culturally_weighted_coherence(
            calibrated_variables,
            pattern['value_priorities']
        )
        
        # Create calibrated profile
        calibrated_profile = CoherenceProfile(
            user_id=raw_profile.user_id,
            variables=calibrated_variables,
            static_coherence=weighted_coherence,
            coherence_velocity=raw_profile.coherence_velocity,
            assessment_tier=raw_profile.assessment_tier,
            timestamp=raw_profile.timestamp,
            age=raw_profile.age,
            context=f"{raw_profile.context}_calibrated_{cultural_context.value}",
            individual_optimization=raw_profile.individual_optimization
        )
        
        return calibrated_profile
    
    def _calibrate_variable(self,
                          raw_value: float,
                          variable_name: str,
                          cultural_pattern: Dict[str, any],
                          response_style: Optional[Dict[str, float]]) -> float:
        """
        Calibrate individual variable for cultural expression
        """
        # Apply cultural expression modifier
        expression_adjusted = raw_value / cultural_pattern['expression_modifiers'][variable_name]
        
        # Adjust for response style if known
        if response_style:
            # Some cultures tend toward extreme responses, others toward middle
            if response_style.get('extremity_bias', 0) > 0.7:
                # Compress extreme responses
                expression_adjusted = 0.5 + (expression_adjusted - 0.5) * 0.8
            elif response_style.get('modesty_bias', 0) > 0.7:
                # Expand modest responses
                expression_adjusted = 0.5 + (expression_adjusted - 0.5) * 1.2
        
        # Ensure within bounds
        return max(0.0, min(1.0, expression_adjusted))
    
    def _calculate_culturally_weighted_coherence(self,
                                               variables: CoherenceVariables,
                                               value_priorities: Dict[str, float]) -> float:
        """
        Calculate coherence with cultural value weighting
        """
        # Normalize priorities
        total_priority = sum(value_priorities.values())
        normalized_priorities = {k: v/total_priority for k, v in value_priorities.items()}
        
        # Weighted coherence calculation
        weighted_coherence = (
            variables.psi * (1 + normalized_priorities['psi']) +
            (variables.rho * variables.psi) * (1 + normalized_priorities['rho']) +
            variables.q * (1 + normalized_priorities['q']) +
            (variables.f * variables.psi) * (1 + normalized_priorities['f'])
        )
        
        return weighted_coherence
    
    def _get_culturally_adjusted_text(self,
                                    question_key: str,
                                    cultural_context: CulturalContext) -> str:
        """
        Return culturally appropriate question text
        """
        cultural_questions = {
            ('values_action_alignment', CulturalContext.COLLECTIVIST_EASTERN): 
                "Rate how well your actions maintain harmony with family and community expectations",
            ('values_action_alignment', CulturalContext.AFRICAN):
                "Rate how well your actions serve your community's collective wellbeing",
            ('moral_action_willingness', CulturalContext.NORDIC):
                "How often do you quietly act on principles without seeking recognition?",
            ('relationship_quality', CulturalContext.COLLECTIVIST_EASTERN):
                "Rate how well you fulfill your roles and obligations to family and society",
            # Add more cultural adaptations as needed
        }
        
        return cultural_questions.get((question_key, cultural_context), 
                                    "Rate this aspect of your experience")
    
    def analyze_cross_cultural_coherence(self,
                                       profiles_by_culture: Dict[CulturalContext, List[CoherenceProfile]]) -> Dict[str, any]:
        """
        Analyze coherence patterns across cultures
        """
        analysis = {
            'cultural_averages': {},
            'universal_patterns': [],
            'cultural_specific_patterns': [],
            'coherence_expression_map': {}
        }
        
        # Calculate averages by culture
        for culture, profiles in profiles_by_culture.items():
            if profiles:
                avg_coherence = np.mean([p.static_coherence for p in profiles])
                avg_variables = {
                    'psi': np.mean([p.variables.psi for p in profiles]),
                    'rho': np.mean([p.variables.rho for p in profiles]),
                    'q': np.mean([p.variables.q for p in profiles]),
                    'f': np.mean([p.variables.f for p in profiles])
                }
                
                analysis['cultural_averages'][culture.value] = {
                    'coherence': avg_coherence,
                    'variables': avg_variables,
                    'sample_size': len(profiles)
                }
        
        # Identify universal patterns
        all_profiles = [p for profiles in profiles_by_culture.values() for p in profiles]
        if len(all_profiles) > 100:
            # Look for correlations that hold across cultures
            psi_values = [p.variables.psi for p in all_profiles]
            coherence_values = [p.static_coherence for p in all_profiles]
            
            if np.corrcoef(psi_values, coherence_values)[0, 1] > 0.7:
                analysis['universal_patterns'].append(
                    "Internal consistency strongly predicts coherence across all cultures"
                )
        
        # Identify culture-specific patterns
        for culture, profiles in profiles_by_culture.items():
            if len(profiles) > 20:
                pattern = self.cultural_patterns[culture]
                
                # Check if cultural values align with observed patterns
                f_values = [p.variables.f for p in profiles]
                if pattern['value_priorities']['f'] > 0.3 and np.mean(f_values) > 0.7:
                    analysis['cultural_specific_patterns'].append(
                        f"{culture.value}: High social belonging aligns with cultural values"
                    )
        
        return analysis
    
    def generate_cultural_insights(self,
                                 profile: CoherenceProfile,
                                 cultural_context: CulturalContext) -> List[str]:
        """
        Generate culturally-aware insights and recommendations
        """
        insights = []
        pattern = self.cultural_patterns[cultural_context]
        
        # Check alignment with cultural values
        value_priorities = pattern['value_priorities']
        
        # Variable-specific insights
        if cultural_context == CulturalContext.COLLECTIVIST_EASTERN:
            if profile.variables.f < 0.5:
                insights.append("Your social belonging is below cultural expectations - consider deepening family/community ties")
            if profile.variables.q > 0.8:
                insights.append("Your high moral activation may need tempering with group harmony considerations")
        
        elif cultural_context == CulturalContext.INDIVIDUALIST_WESTERN:
            if profile.variables.psi < 0.5:
                insights.append("Work on aligning actions with personal values - authenticity is highly valued in your culture")
            if profile.variables.f > 0.8 and profile.variables.q < 0.4:
                insights.append("Consider whether group belonging is limiting individual moral expression")
        
        elif cultural_context == CulturalContext.NORDIC:
            if profile.variables.q > 0.7:
                insights.append("Remember that understated action is valued - effectiveness over visibility")
            if profile.variables.psi < 0.7:
                insights.append("Consistency and reliability are core cultural values - focus on follow-through")
        
        # Communication style insights
        comm_style = pattern['communication_style']
        if comm_style['directness'] < 0.5 and profile.variables.psi > 0.8:
            insights.append("Your high consistency may be expressed too directly for cultural norms")
        
        return insights