# Coherence Recovery Protocols Module
# Specific interventions for recovering from low coherence states (howlround)

import numpy as np
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

# Import core types from main module
from gct_backend import CoherenceProfile, CoherenceVariables

class RecoveryUrgency(Enum):
    CRITICAL = "critical"      # Coherence < 1.0, immediate intervention needed
    HIGH = "high"              # Coherence 1.0-1.5, rapid intervention recommended
    MODERATE = "moderate"      # Coherence 1.5-2.0, structured recovery plan
    LOW = "low"                # Coherence > 2.0, optimization rather than recovery

@dataclass
class RecoveryIntervention:
    """Specific intervention to improve coherence"""
    variable_target: str  # 'psi', 'rho', 'q', 'f'
    intervention_type: str
    description: str
    expected_impact: float
    time_required_minutes: int
    difficulty_level: int  # 1-5
    prerequisites: List[str]

@dataclass
class RecoveryPlan:
    """Personalized coherence recovery plan"""
    urgency: RecoveryUrgency
    current_state_analysis: Dict[str, str]
    immediate_interventions: List[RecoveryIntervention]
    daily_interventions: List[RecoveryIntervention]
    weekly_interventions: List[RecoveryIntervention]
    expected_recovery_days: int
    warning_signs: List[str]
    success_metrics: Dict[str, float]

class CoherenceRecoveryProtocol:
    """Generate and track coherence recovery plans"""
    
    def __init__(self):
        # Intervention library organized by variable
        self.interventions = {
            'psi': [  # Internal Consistency
                RecoveryIntervention(
                    variable_target='psi',
                    intervention_type='reflection',
                    description='Write 3 pages about a time your actions matched your values',
                    expected_impact=0.05,
                    time_required_minutes=30,
                    difficulty_level=2,
                    prerequisites=[]
                ),
                RecoveryIntervention(
                    variable_target='psi',
                    intervention_type='alignment_practice',
                    description='List 5 daily actions and rate their value alignment (1-10)',
                    expected_impact=0.03,
                    time_required_minutes=15,
                    difficulty_level=1,
                    prerequisites=[]
                ),
                RecoveryIntervention(
                    variable_target='psi',
                    intervention_type='consistency_ritual',
                    description='Create and follow a morning ritual that embodies your core values',
                    expected_impact=0.08,
                    time_required_minutes=45,
                    difficulty_level=3,
                    prerequisites=['basic_self_awareness']
                ),
            ],
            'rho': [  # Accumulated Wisdom
                RecoveryIntervention(
                    variable_target='rho',
                    intervention_type='pattern_recognition',
                    description='Identify 3 recurring life patterns and their lessons',
                    expected_impact=0.06,
                    time_required_minutes=45,
                    difficulty_level=3,
                    prerequisites=[]
                ),
                RecoveryIntervention(
                    variable_target='rho',
                    intervention_type='failure_integration',
                    description='Write about a failure and extract 5 specific learnings',
                    expected_impact=0.07,
                    time_required_minutes=40,
                    difficulty_level=4,
                    prerequisites=['emotional_stability']
                ),
                RecoveryIntervention(
                    variable_target='rho',
                    intervention_type='wisdom_dialogue',
                    description='Have a deep conversation with someone 10+ years older',
                    expected_impact=0.04,
                    time_required_minutes=60,
                    difficulty_level=2,
                    prerequisites=['social_comfort']
                ),
            ],
            'q': [  # Moral Activation Energy
                RecoveryIntervention(
                    variable_target='q',
                    intervention_type='micro_courage',
                    description='Take one small action today that scares you but aligns with values',
                    expected_impact=0.04,
                    time_required_minutes=30,
                    difficulty_level=3,
                    prerequisites=[]
                ),
                RecoveryIntervention(
                    variable_target='q',
                    intervention_type='moral_inventory',
                    description='List 3 injustices you witness and one actionable response',
                    expected_impact=0.05,
                    time_required_minutes=25,
                    difficulty_level=2,
                    prerequisites=[]
                ),
                RecoveryIntervention(
                    variable_target='q',
                    intervention_type='principle_activation',
                    description='Publicly state a principle you believe in and act on it today',
                    expected_impact=0.08,
                    time_required_minutes=20,
                    difficulty_level=4,
                    prerequisites=['social_courage']
                ),
            ],
            'f': [  # Social Belonging
                RecoveryIntervention(
                    variable_target='f',
                    intervention_type='authentic_connection',
                    description='Share something vulnerable with a trusted friend',
                    expected_impact=0.06,
                    time_required_minutes=45,
                    difficulty_level=4,
                    prerequisites=['trusted_relationship']
                ),
                RecoveryIntervention(
                    variable_target='f',
                    intervention_type='community_contribution',
                    description='Offer genuine help to someone in your community',
                    expected_impact=0.05,
                    time_required_minutes=60,
                    difficulty_level=2,
                    prerequisites=[]
                ),
                RecoveryIntervention(
                    variable_target='f',
                    intervention_type='belonging_ritual',
                    description='Participate fully in a group activity without holding back',
                    expected_impact=0.04,
                    time_required_minutes=90,
                    difficulty_level=3,
                    prerequisites=['group_access']
                ),
            ]
        }
        
        # Howlround-specific interventions
        self.emergency_interventions = [
            RecoveryIntervention(
                variable_target='all',
                intervention_type='grounding',
                description='5-4-3-2-1 sensory grounding: Name 5 things you see, 4 you hear, 3 you touch, 2 you smell, 1 you taste',
                expected_impact=0.02,
                time_required_minutes=5,
                difficulty_level=1,
                prerequisites=[]
            ),
            RecoveryIntervention(
                variable_target='all',
                intervention_type='coherence_anchor',
                description='Recall and write about your most coherent moment in detail',
                expected_impact=0.03,
                time_required_minutes=20,
                difficulty_level=2,
                prerequisites=[]
            ),
            RecoveryIntervention(
                variable_target='all',
                intervention_type='reality_check',
                description='Call someone who knows you well and ask "Am I being myself?"',
                expected_impact=0.04,
                time_required_minutes=30,
                difficulty_level=3,
                prerequisites=['trusted_contact']
            ),
        ]
    
    def assess_recovery_urgency(self, profile: CoherenceProfile) -> RecoveryUrgency:
        """Determine how urgent coherence recovery is"""
        if profile.static_coherence < 1.0:
            return RecoveryUrgency.CRITICAL
        elif profile.static_coherence < 1.5:
            return RecoveryUrgency.HIGH
        elif profile.static_coherence < 2.0:
            return RecoveryUrgency.MODERATE
        else:
            return RecoveryUrgency.LOW
    
    def identify_recovery_targets(self, profile: CoherenceProfile) -> List[Tuple[str, float]]:
        """Identify which variables need most attention"""
        variables = {
            'psi': profile.variables.psi,
            'rho': profile.variables.rho,
            'q': profile.variables.q,
            'f': profile.variables.f
        }
        
        # Sort by how far below optimal each variable is
        optimal_targets = {'psi': 0.7, 'rho': 0.6, 'q': 0.5, 'f': 0.6}
        deficits = [(var, optimal_targets[var] - value) for var, value in variables.items()]
        deficits.sort(key=lambda x: x[1], reverse=True)
        
        return deficits
    
    def generate_recovery_plan(self, 
                             profile: CoherenceProfile,
                             available_time_daily: int = 60,
                             constraints: Optional[Dict[str, any]] = None) -> RecoveryPlan:
        """
        Generate personalized recovery plan based on profile and constraints
        """
        urgency = self.assess_recovery_urgency(profile)
        recovery_targets = self.identify_recovery_targets(profile)
        
        # Analyze current state
        current_state_analysis = self._analyze_coherence_state(profile)
        
        # Select interventions based on urgency and targets
        immediate_interventions = []
        daily_interventions = []
        weekly_interventions = []
        
        if urgency in [RecoveryUrgency.CRITICAL, RecoveryUrgency.HIGH]:
            # Add emergency interventions first
            immediate_interventions.extend(self.emergency_interventions[:2])
        
        # Add targeted interventions for lowest variables
        time_used_daily = 0
        for variable, deficit in recovery_targets:
            if deficit > 0.1:  # Significant deficit
                # Find suitable interventions
                suitable = [i for i in self.interventions[variable] 
                           if i.time_required_minutes <= available_time_daily - time_used_daily
                           and self._check_prerequisites(i, constraints)]
                
                if suitable:
                    # Add most impactful intervention that fits time constraint
                    best_intervention = max(suitable, key=lambda x: x.expected_impact)
                    if urgency == RecoveryUrgency.CRITICAL:
                        immediate_interventions.append(best_intervention)
                    else:
                        daily_interventions.append(best_intervention)
                    time_used_daily += best_intervention.time_required_minutes
        
        # Add weekly maintenance interventions
        for variable in ['psi', 'rho', 'q', 'f']:
            weekly_options = [i for i in self.interventions[variable] 
                            if i.difficulty_level <= 3 and i not in daily_interventions]
            if weekly_options:
                weekly_interventions.append(weekly_options[0])
        
        # Calculate expected recovery time
        total_deficit = sum(max(0, deficit) for _, deficit in recovery_targets)
        daily_impact = sum(i.expected_impact for i in daily_interventions)
        expected_recovery_days = int(total_deficit / (daily_impact + 0.01)) if daily_impact > 0 else 30
        
        # Generate warning signs
        warning_signs = self._generate_warning_signs(profile)
        
        # Set success metrics
        success_metrics = {
            'target_coherence': min(profile.static_coherence + 0.5, 2.5),
            'minimum_psi': max(profile.variables.psi + 0.1, 0.6),
            'daily_consistency': 0.8,  # Complete 80% of daily interventions
            'weekly_check_in': 1.0,    # Weekly progress assessment
        }
        
        return RecoveryPlan(
            urgency=urgency,
            current_state_analysis=current_state_analysis,
            immediate_interventions=immediate_interventions,
            daily_interventions=daily_interventions,
            weekly_interventions=weekly_interventions,
            expected_recovery_days=expected_recovery_days,
            warning_signs=warning_signs,
            success_metrics=success_metrics
        )
    
    def _analyze_coherence_state(self, profile: CoherenceProfile) -> Dict[str, str]:
        """Provide detailed analysis of current coherence state"""
        analysis = {}
        
        # Overall state
        if profile.static_coherence < 1.0:
            analysis['overall'] = "Critical howlround state - immediate intervention needed"
        elif profile.static_coherence < 1.5:
            analysis['overall'] = "Low coherence - structured recovery recommended"
        elif profile.static_coherence < 2.0:
            analysis['overall'] = "Moderate coherence - optimization opportunities"
        else:
            analysis['overall'] = "Good coherence - maintain and enhance"
        
        # Variable-specific analysis
        if profile.variables.psi < 0.4:
            analysis['consistency'] = "Severe values-action misalignment causing internal conflict"
        elif profile.variables.psi < 0.6:
            analysis['consistency'] = "Moderate inconsistency between beliefs and behaviors"
        
        if profile.variables.rho < 0.3:
            analysis['wisdom'] = "Limited integration of life experiences"
        elif profile.variables.rho < 0.5:
            analysis['wisdom'] = "Some pattern recognition but missing deeper lessons"
        
        if profile.variables.q < 0.3:
            analysis['moral_energy'] = "Low activation - difficulty acting on principles"
        elif profile.variables.q < 0.5:
            analysis['moral_energy'] = "Moderate activation - selective principle adherence"
        
        if profile.variables.f < 0.3:
            analysis['belonging'] = "Significant social disconnection or isolation"
        elif profile.variables.f < 0.5:
            analysis['belonging'] = "Limited authentic connections"
        
        return analysis
    
    def _check_prerequisites(self, 
                           intervention: RecoveryIntervention,
                           constraints: Optional[Dict[str, any]]) -> bool:
        """Check if user meets prerequisites for intervention"""
        if not constraints:
            return True
        
        for prereq in intervention.prerequisites:
            if prereq not in constraints.get('available_resources', []):
                return False
        
        return True
    
    def _generate_warning_signs(self, profile: CoherenceProfile) -> List[str]:
        """Generate personalized warning signs of coherence decline"""
        warning_signs = []
        
        # Universal warning signs
        warning_signs.extend([
            "Feeling like you're 'performing' rather than being authentic",
            "Increased irritability or emotional reactivity",
            "Difficulty making decisions that normally come easily",
            "Sense of disconnection from your usual values",
        ])
        
        # Variable-specific warning signs
        if profile.variables.psi < 0.5:
            warning_signs.append("Saying one thing but consistently doing another")
        
        if profile.variables.rho < 0.5:
            warning_signs.append("Repeating mistakes without learning")
        
        if profile.variables.q < 0.5:
            warning_signs.append("Avoiding situations that require moral courage")
        
        if profile.variables.f < 0.5:
            warning_signs.append("Withdrawing from meaningful relationships")
        
        return warning_signs
    
    def track_recovery_progress(self,
                              initial_profile: CoherenceProfile,
                              current_profile: CoherenceProfile,
                              plan: RecoveryPlan,
                              interventions_completed: List[str]) -> Dict[str, any]:
        """
        Track progress on recovery plan
        """
        # Calculate improvement
        coherence_improvement = current_profile.static_coherence - initial_profile.static_coherence
        psi_improvement = current_profile.variables.psi - initial_profile.variables.psi
        rho_improvement = current_profile.variables.rho - initial_profile.variables.rho
        q_improvement = current_profile.variables.q - initial_profile.variables.q
        f_improvement = current_profile.variables.f - initial_profile.variables.f
        
        # Calculate completion rate
        total_interventions = len(plan.immediate_interventions) + len(plan.daily_interventions)
        completion_rate = len(interventions_completed) / total_interventions if total_interventions > 0 else 0
        
        # Assess progress
        on_track = coherence_improvement > 0 and completion_rate > 0.7
        
        # Generate insights
        insights = []
        if coherence_improvement > 0.2:
            insights.append("Excellent progress - coherence improving significantly")
        elif coherence_improvement > 0.1:
            insights.append("Good progress - steady coherence improvement")
        elif coherence_improvement > 0:
            insights.append("Some progress - continue with interventions")
        else:
            insights.append("Limited progress - consider adjusting approach")
        
        # Variable-specific insights
        improvements = {
            'psi': (psi_improvement, "internal consistency"),
            'rho': (rho_improvement, "wisdom integration"),
            'q': (q_improvement, "moral activation"),
            'f': (f_improvement, "social belonging")
        }
        
        best_improvement = max(improvements.items(), key=lambda x: x[1][0])
        worst_improvement = min(improvements.items(), key=lambda x: x[1][0])
        
        if best_improvement[1][0] > 0.05:
            insights.append(f"Strongest improvement in {best_improvement[1][1]}")
        if worst_improvement[1][0] < 0.02:
            insights.append(f"Focus more on {worst_improvement[1][1]} interventions")
        
        return {
            'coherence_improvement': coherence_improvement,
            'variable_improvements': {
                'psi': psi_improvement,
                'rho': rho_improvement,
                'q': q_improvement,
                'f': f_improvement
            },
            'completion_rate': completion_rate,
            'on_track': on_track,
            'insights': insights,
            'days_in_recovery': (datetime.now() - initial_profile.timestamp).days,
            'projected_completion': plan.expected_recovery_days - (datetime.now() - initial_profile.timestamp).days
        }