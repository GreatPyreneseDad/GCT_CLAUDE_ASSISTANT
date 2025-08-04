# GCT Assistant - Complete Implementation
# Grounded Coherence Theory for Personal and Communication Assessment

"""
CORE GCT FRAMEWORK IMPLEMENTATION

This implementation provides a complete GCT assessment and analysis system
with four tiers of functionality:

1. Basic Assessment (15-20 minutes)
2. Professional Assessment (45-60 minutes) 
3. Advanced Analysis (2-3 hours)
4. Continuous Tracking and Communication Analysis

Database Schema, API endpoints, and frontend integration included.
"""

import math
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
import json
import sqlite3
from contextlib import contextmanager
import logging

# Import shared types
from gct_types import (
    AssessmentTier, 
    CoherenceVariables, 
    CoherenceProfile, 
    CommunicationAnalysis
)

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# DATABASE SCHEMA AND MANAGEMENT
# ============================================================================

class GCTDatabase:
    """SQLite database for GCT assessments and tracking"""
    
    def __init__(self, db_path: str = "gct_data.db"):
        self.db_path = db_path
        self.init_database()
    
    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
    def init_database(self):
        """Initialize database schema"""
        with self.get_connection() as conn:
            # Users table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    age INTEGER,
                    cultural_context TEXT,
                    consent_research BOOLEAN DEFAULT FALSE
                )
            """)
            
            # Coherence assessments
            conn.execute("""
                CREATE TABLE IF NOT EXISTS coherence_assessments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    tier TEXT NOT NULL,
                    psi REAL NOT NULL,
                    rho REAL NOT NULL,
                    q REAL NOT NULL,
                    f REAL NOT NULL,
                    static_coherence REAL NOT NULL,
                    coherence_velocity REAL,
                    context TEXT,
                    individual_optimization TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)
            
            # Communication analyses
            conn.execute("""
                CREATE TABLE IF NOT EXISTS communication_analyses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    text_hash TEXT NOT NULL,
                    consistency_score REAL NOT NULL,
                    wisdom_indicators REAL NOT NULL,
                    moral_activation REAL NOT NULL,
                    social_awareness REAL NOT NULL,
                    authenticity_score REAL NOT NULL,
                    red_flags TEXT,
                    analysis_context TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)
            
            # Relationship mappings
            conn.execute("""
                CREATE TABLE IF NOT EXISTS relationship_mappings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_a_id TEXT NOT NULL,
                    user_b_id TEXT NOT NULL,
                    compatibility_score REAL NOT NULL,
                    influence_dynamics TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_a_id) REFERENCES users (id),
                    FOREIGN KEY (user_b_id) REFERENCES users (id)
                )
            """)
            
            conn.commit()
    
    def save_assessment(self, profile: CoherenceProfile):
        """Save coherence assessment to database"""
        with self.get_connection() as conn:
            conn.execute("""
                INSERT INTO coherence_assessments 
                (user_id, tier, psi, rho, q, f, static_coherence, coherence_velocity, 
                 context, individual_optimization)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                profile.user_id,
                profile.assessment_tier.value,
                profile.variables.psi,
                profile.variables.rho,
                profile.variables.q,
                profile.variables.f,
                profile.static_coherence,
                profile.coherence_velocity,
                profile.context,
                json.dumps(profile.individual_optimization)
            ))
            conn.commit()

# ============================================================================
# CORE ASSESSMENT ALGORITHMS
# ============================================================================

class CoherenceCalculator:
    """Core mathematical framework for GCT calculations"""
    
    @staticmethod
    def calculate_internal_consistency(responses: Dict[str, Any]) -> float:
        """
        Calculate Ψ (Internal Consistency)
        Based on cross-situational moral consistency and belief-action alignment
        """
        if 'quick_assessment' in responses:
            # Tier 1: Simple averaging of 4 consistency questions
            consistency_scores = [
                responses.get('values_action_alignment', 5) / 10.0,
                responses.get('cross_context_consistency', 5) / 10.0,
                responses.get('belief_behavior_match', 5) / 10.0,
                responses.get('emotional_authenticity', 5) / 10.0
            ]
            return np.mean(consistency_scores)
        
        # Advanced calculation for higher tiers
        moral_scenarios = responses.get('moral_scenarios', {})
        behavioral_tracking = responses.get('behavioral_tracking', {})
        
        # Calculate cross-scenario consistency
        scenario_consistency = CoherenceCalculator._calculate_scenario_consistency(moral_scenarios)
        
        # Calculate belief-action alignment
        alignment_score = CoherenceCalculator._calculate_alignment_score(behavioral_tracking)
        
        # Weighted combination
        psi = 0.6 * scenario_consistency + 0.4 * alignment_score
        return max(0.0, min(1.0, psi))
    
    @staticmethod
    def calculate_accumulated_wisdom(responses: Dict[str, Any], age: Optional[int] = None) -> float:
        """
        Calculate ρ (Accumulated Wisdom)
        Age-adjusted learning from challenges and pattern recognition
        """
        if 'quick_assessment' in responses:
            # Tier 1: Simple averaging with age adjustment
            wisdom_scores = [
                responses.get('learning_from_setbacks', 5) / 10.0,
                responses.get('pattern_recognition', 5) / 10.0,
                responses.get('decision_improvement', 5) / 10.0,
                responses.get('resilience_growth', 5) / 10.0
            ]
            raw_wisdom = np.mean(wisdom_scores)
        else:
            # Advanced calculation
            learning_integration = responses.get('learning_integration_score', 0.5)
            pattern_recognition = responses.get('pattern_recognition_detailed', 0.5)
            decision_quality = responses.get('decision_quality_improvement', 0.5)
            raw_wisdom = (learning_integration + pattern_recognition + decision_quality) / 3.0
        
        # Age adjustment formula
        if age and age >= 18:
            # Peak learning capacity at 25-35, gradual decline after 65
            age_factor = min(1.0, 0.3 + (age - 18) * 0.04) if age < 35 else \
                        max(0.7, 1.1 - (age - 35) * 0.006)
            return raw_wisdom * age_factor
        
        return raw_wisdom
    
    @staticmethod
    def calculate_moral_activation_energy(responses: Dict[str, Any], 
                                        individual_optimization: bool = True) -> Tuple[float, Dict[str, float]]:
        """
        Calculate q (Moral Activation Energy) with biological optimization
        Individual parameter optimization based on personality and wisdom level
        """
        if 'quick_assessment' in responses:
            # Tier 1: Simple averaging
            activation_scores = [
                responses.get('injustice_response', 5) / 10.0,
                responses.get('moral_action_willingness', 5) / 10.0,
                responses.get('principle_consistency', 5) / 10.0,
                responses.get('costly_action_history', 5) / 10.0
            ]
            raw_activation = np.mean(activation_scores)
            base_params = {'K_m': 0.2, 'K_i': 0.8}
        else:
            # Advanced calculation
            injustice_sensitivity = responses.get('injustice_sensitivity', 0.5)
            moral_action_history = responses.get('moral_action_history', 0.5)
            principle_adherence = responses.get('principle_adherence', 0.5)
            raw_activation = (injustice_sensitivity + moral_action_history + principle_adherence) / 3.0
            
            # Individual parameter optimization
            if individual_optimization:
                base_params = CoherenceCalculator._optimize_individual_parameters(responses)
            else:
                base_params = {'K_m': 0.2, 'K_i': 0.8}
        
        # Biological optimization curve: q_optimal = K_i / (1 + exp(K_m * (threshold - raw_q)))
        threshold = 0.5  # Biological optimum point
        q_optimal = base_params['K_i'] / (1 + math.exp(base_params['K_m'] * (threshold - raw_activation)))
        
        return q_optimal, base_params
    
    @staticmethod
    def calculate_social_belonging(responses: Dict[str, Any]) -> float:
        """
        Calculate f (Social Belonging Architecture)
        Quality relationships, cultural resonance, network position
        """
        if 'quick_assessment' in responses:
            # Tier 1: Simple averaging
            belonging_scores = [
                responses.get('relationship_quality', 5) / 10.0,
                responses.get('cultural_resonance', 5) / 10.0,
                responses.get('social_support', 5) / 10.0,
                responses.get('community_contribution', 5) / 10.0
            ]
            return np.mean(belonging_scores)
        
        # Advanced calculation
        relationship_quality = responses.get('relationship_quality_detailed', 0.5)
        cultural_alignment = responses.get('cultural_alignment', 0.5)
        network_position = responses.get('network_position_score', 0.5)
        authentic_connection = responses.get('authentic_connection_capacity', 0.5)
        
        f = (relationship_quality + cultural_alignment + network_position + authentic_connection) / 4.0
        return max(0.0, min(1.0, f))
    
    @staticmethod
    def calculate_static_coherence(variables: CoherenceVariables) -> float:
        """
        Calculate static coherence: C = Ψ + (ρ × Ψ) + q_optimal + (f × Ψ)
        """
        return (variables.psi + 
                (variables.rho * variables.psi) + 
                variables.q + 
                (variables.f * variables.psi))
    
    @staticmethod
    def calculate_coherence_velocity(current_profile: CoherenceProfile, 
                                   previous_profile: Optional[CoherenceProfile]) -> Optional[float]:
        """
        Calculate dC/dt based on change between assessments
        """
        if not previous_profile:
            return None
        
        time_diff = (current_profile.timestamp - previous_profile.timestamp).total_seconds()
        if time_diff <= 0:
            return None
        
        coherence_diff = current_profile.static_coherence - previous_profile.static_coherence
        velocity = coherence_diff / (time_diff / (24 * 3600))  # Per day
        
        return velocity
    
    @staticmethod
    def _calculate_scenario_consistency(scenarios: Dict[str, Any]) -> float:
        """Calculate consistency across moral scenarios"""
        if not scenarios:
            return 0.5
        
        # Placeholder for actual moral scenario consistency calculation
        # In real implementation, this would analyze response patterns
        responses = list(scenarios.values())
        if len(responses) < 2:
            return 0.5
        
        # Calculate correlation/consistency across responses
        consistency = 1.0 - (np.std(responses) / (np.mean(responses) + 0.001))
        return max(0.0, min(1.0, consistency))
    
    @staticmethod
    def _calculate_alignment_score(behavioral_data: Dict[str, Any]) -> float:
        """Calculate belief-action alignment from behavioral tracking"""
        if not behavioral_data:
            return 0.5
        
        # Placeholder for actual behavioral alignment calculation
        stated_values = behavioral_data.get('stated_values', [])
        actual_behaviors = behavioral_data.get('actual_behaviors', [])
        
        if not stated_values or not actual_behaviors:
            return 0.5
        
        # Simple alignment calculation (in practice, this would be more sophisticated)
        alignment_scores = []
        for value, behavior in zip(stated_values, actual_behaviors):
            alignment_scores.append(1.0 - abs(value - behavior))
        
        return np.mean(alignment_scores) if alignment_scores else 0.5
    
    @staticmethod
    def _optimize_individual_parameters(responses: Dict[str, Any]) -> Dict[str, float]:
        """
        Optimize K_m and K_i parameters based on individual characteristics
        Enhanced GCT with wisdom-dependent optimization
        """
        # Base parameters
        K_m_base = 0.2
        K_i_base = 0.8
        
        # Individual adjustment factors
        personality_factors = responses.get('personality_assessment', {})
        wisdom_level = responses.get('accumulated_wisdom_detailed', 0.5)
        
        # Wisdom amplification effect: K_i_personal = K_i_base * (1 + 0.5 * ρ)
        K_i_personal = K_i_base * (1 + 0.5 * wisdom_level)
        
        # Personality-based K_m adjustment
        conscientiousness = personality_factors.get('conscientiousness', 0.5)
        emotional_stability = personality_factors.get('emotional_stability', 0.5)
        
        # More conscientious and emotionally stable individuals have steeper activation curves
        K_m_personal = K_m_base * (1 + 0.3 * (conscientiousness + emotional_stability) / 2)
        
        return {
            'K_m': min(1.0, K_m_personal),
            'K_i': min(1.0, K_i_personal)
        }

# ============================================================================
# ASSESSMENT PROTOCOLS
# ============================================================================

class GCTAssessment:
    """Main assessment interface with tiered protocols"""
    
    def __init__(self, database: GCTDatabase):
        self.db = database
        self.calculator = CoherenceCalculator()
    
    def tier1_quick_assessment(self, user_id: str, responses: Dict[str, Any], 
                             age: Optional[int] = None) -> CoherenceProfile:
        """
        Tier 1: Basic Coherence Assessment (15-20 minutes)
        4 questions per variable, simple scoring
        """
        # Mark as quick assessment for simplified calculations
        responses['quick_assessment'] = True
        
        # Calculate variables
        psi = self.calculator.calculate_internal_consistency(responses)
        rho = self.calculator.calculate_accumulated_wisdom(responses, age)
        q, q_params = self.calculator.calculate_moral_activation_energy(responses, 
                                                                      individual_optimization=False)
        f = self.calculator.calculate_social_belonging(responses)
        
        variables = CoherenceVariables(psi=psi, rho=rho, q=q, f=f)
        static_coherence = self.calculator.calculate_static_coherence(variables)
        
        profile = CoherenceProfile(
            user_id=user_id,
            variables=variables,
            static_coherence=static_coherence,
            assessment_tier=AssessmentTier.BASIC,
            age=age,
            individual_optimization=q_params
        )
        
        # Save to database
        self.db.save_assessment(profile)
        
        return profile
    
    def tier2_professional_assessment(self, user_id: str, responses: Dict[str, Any], 
                                    age: Optional[int] = None) -> CoherenceProfile:
        """
        Tier 2: Professional Assessment (45-60 minutes)
        Detailed questions, individual optimization, basic derivative tracking
        """
        # Get previous assessment for velocity calculation
        previous_profile = self.get_latest_assessment(user_id)
        
        # Calculate variables with advanced methods
        psi = self.calculator.calculate_internal_consistency(responses)
        rho = self.calculator.calculate_accumulated_wisdom(responses, age)
        q, q_params = self.calculator.calculate_moral_activation_energy(responses, 
                                                                      individual_optimization=True)
        f = self.calculator.calculate_social_belonging(responses)
        
        variables = CoherenceVariables(psi=psi, rho=rho, q=q, f=f)
        static_coherence = self.calculator.calculate_static_coherence(variables)
        
        profile = CoherenceProfile(
            user_id=user_id,
            variables=variables,
            static_coherence=static_coherence,
            assessment_tier=AssessmentTier.PROFESSIONAL,
            age=age,
            individual_optimization=q_params
        )
        
        # Calculate velocity if previous assessment exists
        if previous_profile:
            profile.coherence_velocity = self.calculator.calculate_coherence_velocity(
                profile, previous_profile
            )
        
        # Save to database
        self.db.save_assessment(profile)
        
        return profile
    
    def get_latest_assessment(self, user_id: str) -> Optional[CoherenceProfile]:
        """Retrieve latest assessment for a user"""
        with self.db.get_connection() as conn:
            cursor = conn.execute("""
                SELECT * FROM coherence_assessments 
                WHERE user_id = ? 
                ORDER BY timestamp DESC 
                LIMIT 1
            """, (user_id,))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            # Reconstruct profile from database row
            variables = CoherenceVariables(
                psi=row['psi'],
                rho=row['rho'],
                q=row['q'],
                f=row['f']
            )
            
            return CoherenceProfile(
                user_id=row['user_id'],
                variables=variables,
                static_coherence=row['static_coherence'],
                coherence_velocity=row['coherence_velocity'],
                assessment_tier=AssessmentTier(row['tier']),
                timestamp=datetime.fromisoformat(row['timestamp']),
                individual_optimization=json.loads(row['individual_optimization'] or '{}')
            )

# ============================================================================
# COMMUNICATION ANALYSIS
# ============================================================================

class CommunicationAnalyzer:
    """Analyze text/speech for coherence patterns and authenticity"""
    
    def __init__(self):
        self.consistency_keywords = [
            'always', 'never', 'consistently', 'reliable', 'predictable',
            'stable', 'constant', 'regular', 'systematic'
        ]
        
        self.wisdom_keywords = [
            'learned', 'experience', 'understand', 'realize', 'discovered',
            'pattern', 'reflection', 'insight', 'perspective', 'context'
        ]
        
        self.moral_keywords = [
            'should', 'ought', 'right', 'wrong', 'justice', 'fair', 'ethical',
            'principle', 'value', 'integrity', 'responsibility', 'duty'
        ]
        
        self.social_keywords = [
            'we', 'our', 'together', 'community', 'shared', 'collective',
            'relationship', 'connection', 'support', 'collaboration'
        ]
        
        self.manipulation_patterns = [
            'everybody knows', 'obviously', 'clearly', 'any reasonable person',
            'studies show', 'experts agree', 'it\'s been proven'
        ]
    
    def analyze_message_coherence(self, text: str, 
                                speaker_profile: Optional[CoherenceProfile] = None) -> CommunicationAnalysis:
        """
        Comprehensive analysis of message coherence and authenticity
        """
        text_lower = text.lower()
        
        # Calculate component scores
        consistency_score = self._assess_consistency_markers(text_lower)
        wisdom_indicators = self._assess_wisdom_markers(text_lower)
        moral_activation = self._assess_moral_content(text_lower)
        social_awareness = self._assess_social_sensitivity(text_lower)
        
        # Calculate overall authenticity score
        authenticity_score = self._calculate_authenticity_score(
            consistency_score, wisdom_indicators, moral_activation, social_awareness,
            speaker_profile
        )
        
        # Identify red flags
        red_flags = self._identify_manipulation_patterns(text_lower)
        
        # Generate enhancement suggestions
        enhancement_suggestions = self._suggest_improvements(
            text, consistency_score, wisdom_indicators, moral_activation, social_awareness
        )
        
        # Calculate confidence level based on text length and complexity
        confidence_level = self._calculate_confidence_level(text)
        
        return CommunicationAnalysis(
            text=text,
            consistency_score=consistency_score,
            wisdom_indicators=wisdom_indicators,
            moral_activation=moral_activation,
            social_awareness=social_awareness,
            authenticity_score=authenticity_score,
            red_flags=red_flags,
            enhancement_suggestions=enhancement_suggestions,
            confidence_level=confidence_level
        )
    
    def _assess_consistency_markers(self, text: str) -> float:
        """Assess internal consistency indicators in text"""
        word_count = len(text.split())
        if word_count == 0:
            return 0.0
        
        consistency_count = sum(1 for keyword in self.consistency_keywords if keyword in text)
        
        # Look for contradictory statements (simplified)
        contradictions = 0
        if 'but' in text or 'however' in text:
            contradictions += 0.1
        if 'although' in text or 'despite' in text:
            contradictions += 0.1
        
        # Base score from consistency keywords
        base_score = min(1.0, consistency_count / (word_count / 20))
        
        # Adjust for contradictions
        final_score = max(0.0, base_score - contradictions)
        
        return final_score
    
    def _assess_wisdom_markers(self, text: str) -> float:
        """Assess wisdom and learning indicators"""
        word_count = len(text.split())
        if word_count == 0:
            return 0.0
        
        wisdom_count = sum(1 for keyword in self.wisdom_keywords if keyword in text)
        
        # Look for reflective language patterns
        reflection_patterns = [
            'i learned', 'i realized', 'i understand', 'in my experience',
            'looking back', 'i\'ve found', 'i\'ve discovered'
        ]
        
        reflection_count = sum(1 for pattern in reflection_patterns if pattern in text)
        
        # Combined score
        total_score = (wisdom_count + reflection_count * 2) / (word_count / 15)
        return min(1.0, total_score)
    
    def _assess_moral_content(self, text: str) -> float:
        """Assess moral activation and ethical content"""
        word_count = len(text.split())
        if word_count == 0:
            return 0.0
        
        moral_count = sum(1 for keyword in self.moral_keywords if keyword in text)
        
        # Look for moral action language
        action_patterns = [
            'i will', 'we should', 'we must', 'it\'s important',
            'i believe', 'i stand for', 'we need to'
        ]
        
        action_count = sum(1 for pattern in action_patterns if pattern in text)
        
        total_score = (moral_count + action_count * 1.5) / (word_count / 20)
        return min(1.0, total_score)
    
    def _assess_social_sensitivity(self, text: str) -> float:
        """Assess social awareness and belonging architecture"""
        word_count = len(text.split())
        if word_count == 0:
            return 0.0
        
        social_count = sum(1 for keyword in self.social_keywords if keyword in text)
        
        # Look for perspective-taking language
        perspective_patterns = [
            'you might', 'others may', 'different viewpoints', 'i understand that',
            'from their perspective', 'considering', 'recognizing'
        ]
        
        perspective_count = sum(1 for pattern in perspective_patterns if pattern in text)
        
        total_score = (social_count + perspective_count * 2) / (word_count / 18)
        return min(1.0, total_score)
    
    def _calculate_authenticity_score(self, consistency: float, wisdom: float, 
                                    moral: float, social: float,
                                    speaker_profile: Optional[CoherenceProfile] = None) -> float:
        """Calculate overall authenticity likelihood"""
        # Base score from component average
        component_scores = [consistency, wisdom, moral, social]
        base_score = np.mean(component_scores)
        
        # If we have speaker profile, adjust based on coherence alignment
        if speaker_profile:
            profile_alignment = self._calculate_profile_alignment(
                consistency, wisdom, moral, social, speaker_profile
            )
            # Weight profile alignment at 30% of final score
            final_score = 0.7 * base_score + 0.3 * profile_alignment
        else:
            final_score = base_score
        
        return max(0.0, min(1.0, final_score))
    
    def _calculate_profile_alignment(self, consistency: float, wisdom: float,
                                   moral: float, social: float,
                                   profile: CoherenceProfile) -> float:
        """Calculate how well message aligns with speaker's coherence profile"""
        expected_consistency = profile.variables.psi
        expected_wisdom = profile.variables.rho
        expected_moral = profile.variables.q
        expected_social = profile.variables.f
        
        # Calculate alignment scores (how close message is to expected profile)
        consistency_align = 1.0 - abs(consistency - expected_consistency)
        wisdom_align = 1.0 - abs(wisdom - expected_wisdom)
        moral_align = 1.0 - abs(moral - expected_moral)
        social_align = 1.0 - abs(social - expected_social)
        
        return np.mean([consistency_align, wisdom_align, moral_align, social_align])
    
    def _identify_manipulation_patterns(self, text: str) -> List[str]:
        """Identify potential manipulation or howlround patterns"""
        red_flags = []
        
        # Check for manipulation language
        for pattern in self.manipulation_patterns:
            if pattern in text:
                red_flags.append(f"Manipulation pattern: '{pattern}'")
        
        # Check for excessive certainty without evidence
        certainty_words = ['definitely', 'absolutely', 'without doubt', 'certainly']
        evidence_words = ['because', 'evidence', 'research', 'data', 'study']
        
        certainty_count = sum(1 for word in certainty_words if word in text)
        evidence_count = sum(1 for word in evidence_words if word in text)
        
        if certainty_count > evidence_count and certainty_count > 1:
            red_flags.append("High certainty with insufficient evidence")
        
        # Check for emotional manipulation
        emotional_pressure = ['you should feel', 'any decent person', 'if you really cared']
        for pattern in emotional_pressure:
            if pattern in text:
                red_flags.append(f"Emotional pressure: '{pattern}'")
        
        return red_flags
    
    def _suggest_improvements(self, text: str, consistency: float, wisdom: float,
                            moral: float, social: float) -> List[str]:
        """Suggest improvements to increase coherence"""
        suggestions = []
        
        if consistency < 0.4:
            suggestions.append("Consider being more consistent in your language and position")
        
        if wisdom < 0.3:
            suggestions.append("Share specific experiences or learning that inform your perspective")
        
        if moral < 0.3:
            suggestions.append("Clarify the values or principles underlying your position")
        
        if social < 0.3:
            suggestions.append("Acknowledge different perspectives and show awareness of others' views")
        
        # Check for overall coherence
        overall_score = np.mean([consistency, wisdom, moral, social])
        if overall_score < 0.5:
            suggestions.append("Consider grounding your message in specific examples and personal experience")
        
        return suggestions
    
    def _calculate_confidence_level(self, text: str) -> float:
        """Calculate confidence in analysis based on text characteristics"""
        word_count = len(text.split())
        
        # More words generally mean higher confidence (up to a point)
        length_confidence = min(1.0, word_count / 50)
        
        # Presence of specific language patterns increases confidence
        pattern_indicators = [
            'i think', 'i believe', 'in my view', 'from my experience',
            'i feel', 'it seems', 'i would say'
        ]
        
        pattern_count = sum(1 for pattern in pattern_indicators if pattern in text.lower())
        pattern_confidence = min(1.0, pattern_count / 3)
        
        # Average the confidence factors
        overall_confidence = (length_confidence + pattern_confidence) / 2
        
        return max(0.3, overall_confidence)  # Minimum 30% confidence

# ============================================================================
# RELATIONSHIP MAPPING
# ============================================================================

class RelationshipMapper:
    """Analyze coherence compatibility and dynamics between individuals"""
    
    def analyze_compatibility(self, profile_a: CoherenceProfile, 
                            profile_b: CoherenceProfile) -> Dict[str, Any]:
        """
        Analyze coherence compatibility between two individuals
        """
        # Calculate variable-specific compatibility
        psi_compatibility = 1.0 - abs(profile_a.variables.psi - profile_b.variables.psi)
        rho_compatibility = 1.0 - abs(profile_a.variables.rho - profile_b.variables.rho)
        q_compatibility = 1.0 - abs(profile_a.variables.q - profile_b.variables.q)
        f_compatibility = 1.0 - abs(profile_a.variables.f - profile_b.variables.f)
        
        # Overall compatibility score
        overall_compatibility = np.mean([psi_compatibility, rho_compatibility, 
                                       q_compatibility, f_compatibility])
        
        # Predict transmission dynamics based on GCT asymmetric transmission
        transmission_dynamics = self._predict_transmission_dynamics(profile_a, profile_b)
        
        # Identify growth opportunities
        growth_opportunities = self._identify_growth_opportunities(profile_a, profile_b)
        
        # Potential conflict areas
        conflict_areas = self._identify_potential_conflicts(profile_a, profile_b)
        
        return {
            'overall_compatibility': overall_compatibility,
            'variable_compatibility': {
                'internal_consistency': psi_compatibility,
                'accumulated_wisdom': rho_compatibility,
                'moral_activation': q_compatibility,
                'social_belonging': f_compatibility
            },
            'transmission_dynamics': transmission_dynamics,
            'growth_opportunities': growth_opportunities,
            'potential_conflicts': conflict_areas,
            'relationship_recommendations': self._generate_recommendations(
                overall_compatibility, transmission_dynamics, growth_opportunities
            )
        }
    
    def _predict_transmission_dynamics(self, profile_a: CoherenceProfile, 
                                     profile_b: CoherenceProfile) -> Dict[str, Any]:
        """
        Predict influence transmission based on GCT asymmetric dynamics
        High-ρ individuals receive fewer but transmit more influential messages
        """
        # Reception velocity: inversely related to ρ
        a_reception_velocity = 1.0 - profile_a.variables.rho * 0.8
        b_reception_velocity = 1.0 - profile_b.variables.rho * 0.8
        
        # Transmission velocity: positively related to ρ and q
        a_transmission_velocity = (profile_a.variables.rho * 0.6 + profile_a.variables.q * 0.4)
        b_transmission_velocity = (profile_b.variables.rho * 0.6 + profile_b.variables.q * 0.4)
        
        # Influence asymmetry
        a_to_b_influence = a_transmission_velocity * b_reception_velocity
        b_to_a_influence = b_transmission_velocity * a_reception_velocity
        
        return {
            'a_to_b_influence': a_to_b_influence,
            'b_to_a_influence': b_to_a_influence,
            'influence_asymmetry': abs(a_to_b_influence - b_to_a_influence),
            'dominant_influencer': 'A' if a_to_b_influence > b_to_a_influence else 'B',
            'mutual_influence': min(a_to_b_influence, b_to_a_influence)
        }
    
    def _identify_growth_opportunities(self, profile_a: CoherenceProfile, 
                                     profile_b: CoherenceProfile) -> List[str]:
        """Identify mutual growth opportunities"""
        opportunities = []
        
        # Wisdom sharing opportunities
        if profile_a.variables.rho > profile_b.variables.rho + 0.2:
            opportunities.append("A can mentor B in learning from experiences")
        elif profile_b.variables.rho > profile_a.variables.rho + 0.2:
            opportunities.append("B can mentor A in learning from experiences")
        
        # Moral activation balance
        if profile_a.variables.q > profile_b.variables.q + 0.2:
            opportunities.append("A can inspire B toward greater moral action")
        elif profile_b.variables.q > profile_a.variables.q + 0.2:
            opportunities.append("B can inspire A toward greater moral action")
        
        # Social integration support
        if profile_a.variables.f > profile_b.variables.f + 0.2:
            opportunities.append("A can help B build stronger social connections")
        elif profile_b.variables.f > profile_a.variables.f + 0.2:
            opportunities.append("B can help A build stronger social connections")
        
        # Consistency development
        if profile_a.variables.psi > profile_b.variables.psi + 0.2:
            opportunities.append("A can help B develop greater internal consistency")
        elif profile_b.variables.psi > profile_a.variables.psi + 0.2:
            opportunities.append("B can help A develop greater internal consistency")
        
        return opportunities
    
    def _identify_potential_conflicts(self, profile_a: CoherenceProfile, 
                                    profile_b: CoherenceProfile) -> List[str]:
        """Identify potential areas of conflict or tension"""
        conflicts = []
        
        # Moral activation mismatch
        q_diff = abs(profile_a.variables.q - profile_b.variables.q)
        if q_diff > 0.4:
            conflicts.append("Significant difference in moral activation - may clash on action timing")
        
        # Consistency vs. adaptability tension
        if profile_a.variables.psi > 0.8 and profile_b.variables.rho > 0.8:
            conflicts.append("High consistency vs. high wisdom may create rigidity vs. flexibility tension")
        
        # Social belonging mismatch
        f_diff = abs(profile_a.variables.f - profile_b.variables.f)
        if f_diff > 0.5:
            conflicts.append("Different social needs - one may overwhelm or underwhelm the other")
        
        # Overall coherence gap
        coherence_diff = abs(profile_a.static_coherence - profile_b.static_coherence)
        if coherence_diff > 1.0:
            conflicts.append("Significant overall coherence gap may create communication challenges")
        
        return conflicts
    
    def _generate_recommendations(self, compatibility: float, 
                                transmission_dynamics: Dict[str, Any],
                                growth_opportunities: List[str]) -> List[str]:
        """Generate specific relationship optimization recommendations"""
        recommendations = []
        
        if compatibility > 0.8:
            recommendations.append("High compatibility - focus on mutual growth and shared projects")
        elif compatibility > 0.6:
            recommendations.append("Good compatibility - work on areas of difference as growth opportunities")
        else:
            recommendations.append("Lower compatibility - focus on understanding differences and finding common ground")
        
        # Transmission-based recommendations
        if transmission_dynamics['influence_asymmetry'] > 0.3:
            dominant = transmission_dynamics['dominant_influencer']
            recommendations.append(f"Person {dominant} has stronger influence - be mindful of balance in decision-making")
        
        # Growth-based recommendations
        if len(growth_opportunities) > 2:
            recommendations.append("Many mutual growth opportunities - create structured learning exchanges")
        
        return recommendations

# ============================================================================
# API BACKEND (Flask/FastAPI structure for Render deployment)
# ============================================================================

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

def create_app(config_name='production'):
    """Factory function to create Flask app"""
    # Load environment variables
    if config_name == 'local':
        load_dotenv('.env.local')
    else:
        load_dotenv()
    
    app = Flask(__name__)
    
    # Configure based on environment
    if config_name == 'local':
        try:
            from local_config import LocalConfig
            app.config.from_object(LocalConfig)
            LocalConfig.init_app(app)
            # Configure CORS for local development
            CORS(app, origins=['http://localhost:3000', 'http://127.0.0.1:3000'])
        except ImportError:
            # Fallback if local_config doesn't exist
            CORS(app)
    else:
        CORS(app)  # Enable CORS for production
    
    # Initialize database
    db_path = os.getenv('DATABASE_PATH', 'gct_data.db')
    db = GCTDatabase(db_path)
    
    # Initialize core components
    assessment = GCTAssessment(db)
    comm_analyzer = CommunicationAnalyzer()
    relationship_mapper = RelationshipMapper()
    
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        return jsonify({'status': 'healthy', 'version': '1.0.0'})
    
    @app.route('/api/assessment/tier1', methods=['POST'])
    def tier1_assessment():
        """Tier 1 basic assessment endpoint"""
        try:
            data = request.get_json()
            user_id = data.get('user_id')
            responses = data.get('responses', {})
            age = data.get('age')
            
            if not user_id:
                return jsonify({'error': 'user_id required'}), 400
            
            profile = assessment.tier1_quick_assessment(user_id, responses, age)
            
            return jsonify({
                'success': True,
                'profile': {
                    'user_id': profile.user_id,
                    'variables': asdict(profile.variables),
                    'static_coherence': profile.static_coherence,
                    'assessment_tier': profile.assessment_tier.value,
                    'timestamp': profile.timestamp.isoformat(),
                    'insights': generate_tier1_insights(profile)
                }
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/assessment/tier2', methods=['POST'])
    def tier2_assessment():
        """Tier 2 professional assessment endpoint"""
        try:
            data = request.get_json()
            user_id = data.get('user_id')
            responses = data.get('responses', {})
            age = data.get('age')
            
            if not user_id:
                return jsonify({'error': 'user_id required'}), 400
            
            profile = assessment.tier2_professional_assessment(user_id, responses, age)
            
            return jsonify({
                'success': True,
                'profile': {
                    'user_id': profile.user_id,
                    'variables': asdict(profile.variables),
                    'static_coherence': profile.static_coherence,
                    'coherence_velocity': profile.coherence_velocity,
                    'assessment_tier': profile.assessment_tier.value,
                    'timestamp': profile.timestamp.isoformat(),
                    'individual_optimization': profile.individual_optimization,
                    'insights': generate_tier2_insights(profile)
                }
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/communication/analyze', methods=['POST'])
    def analyze_communication():
        """Communication analysis endpoint"""
        try:
            data = request.get_json()
            text = data.get('text', '')
            user_id = data.get('user_id')
            
            if not text:
                return jsonify({'error': 'text required'}), 400
            
            # Get speaker profile if available
            speaker_profile = None
            if user_id:
                speaker_profile = assessment.get_latest_assessment(user_id)
            
            analysis = comm_analyzer.analyze_message_coherence(text, speaker_profile)
            
            return jsonify({
                'success': True,
                'analysis': {
                    'consistency_score': analysis.consistency_score,
                    'wisdom_indicators': analysis.wisdom_indicators,
                    'moral_activation': analysis.moral_activation,
                    'social_awareness': analysis.social_awareness,
                    'authenticity_score': analysis.authenticity_score,
                    'red_flags': analysis.red_flags,
                    'enhancement_suggestions': analysis.enhancement_suggestions,
                    'confidence_level': analysis.confidence_level
                }
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/relationship/analyze', methods=['POST'])
    def analyze_relationship():
        """Relationship compatibility analysis endpoint"""
        try:
            data = request.get_json()
            user_a_id = data.get('user_a_id')
            user_b_id = data.get('user_b_id')
            
            if not user_a_id or not user_b_id:
                return jsonify({'error': 'Both user_a_id and user_b_id required'}), 400
            
            # Get profiles
            profile_a = assessment.get_latest_assessment(user_a_id)
            profile_b = assessment.get_latest_assessment(user_b_id)
            
            if not profile_a or not profile_b:
                return jsonify({'error': 'Assessment profiles required for both users'}), 400
            
            compatibility_analysis = relationship_mapper.analyze_compatibility(profile_a, profile_b)
            
            return jsonify({
                'success': True,
                'compatibility_analysis': compatibility_analysis
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/user/<user_id>/profile', methods=['GET'])
    def get_user_profile(user_id):
        """Get latest user profile"""
        try:
            profile = assessment.get_latest_assessment(user_id)
            
            if not profile:
                return jsonify({'error': 'No assessment found for user'}), 404
            
            return jsonify({
                'success': True,
                'profile': {
                    'user_id': profile.user_id,
                    'variables': asdict(profile.variables),
                    'static_coherence': profile.static_coherence,
                    'coherence_velocity': profile.coherence_velocity,
                    'assessment_tier': profile.assessment_tier.value,
                    'timestamp': profile.timestamp.isoformat()
                }
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # Import and register enhanced API endpoints
    # Delayed import to avoid circular dependency
    try:
        from gct_enhanced_api import enhanced_api
        app.register_blueprint(enhanced_api)
        logger.info('Enhanced API endpoints registered successfully')
    except ImportError as e:
        logger.warning(f'Enhanced API endpoints not available: {e}')
    
    # Import and register GPU-accelerated API endpoints
    try:
        from gpu_api_endpoints import gpu_api
        app.register_blueprint(gpu_api, url_prefix='/api')
        logger.info('GPU-accelerated API endpoints registered successfully')
    except ImportError as e:
        logger.warning(f'GPU-accelerated API endpoints not available: {e}')
    
    # Import and register Apple Intelligence bridge endpoints
    try:
        import sys
        sys.path.append('../integration')
        from gct_apple_intelligence_bridge import GCTAppleIntelligenceBridge, GCTAPIWrapper
        from flask import request
        
        bridge = GCTAppleIntelligenceBridge()
        wrapper = GCTAPIWrapper(bridge)
        wrapper.create_flask_endpoints(app)
        logger.info('Apple Intelligence bridge registered successfully')
    except ImportError as e:
        logger.warning(f'Apple Intelligence bridge not available: {e}')
    
    return app

# ============================================================================
# INSIGHT GENERATION
# ============================================================================

def generate_tier1_insights(profile: CoherenceProfile) -> Dict[str, Any]:
    """Generate basic insights for Tier 1 assessment"""
    insights = {
        'overall_coherence_level': 'high' if profile.static_coherence > 2.5 else 'moderate' if profile.static_coherence > 1.5 else 'developing',
        'strongest_area': max(asdict(profile.variables).items(), key=lambda x: x[1])[0],
        'development_area': min(asdict(profile.variables).items(), key=lambda x: x[1])[0],
        'key_recommendations': []
    }
    
    # Variable-specific insights
    if profile.variables.psi < 0.4:
        insights['key_recommendations'].append("Focus on aligning daily actions with stated values")
    
    if profile.variables.rho < 0.4:
        insights['key_recommendations'].append("Reflect more deeply on lessons from challenges")
    
    if profile.variables.q < 0.4:
        insights['key_recommendations'].append("Consider how to act more courageously on your principles")
    
    if profile.variables.f < 0.4:
        insights['key_recommendations'].append("Invest in building deeper, more authentic relationships")
    
    return insights

def generate_tier2_insights(profile: CoherenceProfile) -> Dict[str, Any]:
    """Generate detailed insights for Tier 2 assessment"""
    insights = generate_tier1_insights(profile)
    
    # Add advanced insights
    insights.update({
        'coherence_trajectory': 'improving' if profile.coherence_velocity and profile.coherence_velocity > 0 else 'stable' if profile.coherence_velocity == 0 else 'declining',
        'leadership_readiness': assess_leadership_readiness(profile),
        'innovation_timing': assess_innovation_timing(profile),
        'individual_optimization': profile.individual_optimization
    })
    
    return insights

def assess_leadership_readiness(profile: CoherenceProfile) -> str:
    """Assess readiness for leadership roles based on coherence profile"""
    if profile.static_coherence > 2.8 and profile.variables.q > 0.6 and profile.variables.rho > 0.6:
        return "high"
    elif profile.static_coherence > 2.0 and profile.variables.q > 0.4:
        return "moderate" 
    else:
        return "developing"

def assess_innovation_timing(profile: CoherenceProfile) -> str:
    """Assess optimal timing for innovation and creative work"""
    if profile.coherence_velocity and abs(profile.coherence_velocity) > 0.1:
        return "transition_period_high_creativity"
    elif profile.static_coherence > 2.5:
        return "stable_period_good_for_implementation"
    else:
        return "development_period_focus_on_foundation"

# ============================================================================
# MAIN APPLICATION ENTRY POINT
# ============================================================================

if __name__ == '__main__':
    # For local development
    app = create_app('local')
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

# For production deployment
app = create_app('production')