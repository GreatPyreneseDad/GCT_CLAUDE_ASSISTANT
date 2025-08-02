# Coherence Development Prediction Module
# Predicts individual coherence development trajectories and optimal interventions

import numpy as np
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
import warnings
warnings.filterwarnings('ignore')

# Import core types and enhancement modules
from gct_backend import CoherenceProfile, CoherenceVariables
from temporal_coherence import TemporalPattern, CircadianType
from coherence_recovery import RecoveryPlan, RecoveryIntervention
from ai_coherence_interaction import AIInteractionType
from cultural_calibration import CulturalContext

@dataclass
class DevelopmentTrajectory:
    """Predicted coherence development path"""
    user_id: str
    baseline_profile: CoherenceProfile
    predicted_profiles: List[CoherenceProfile]  # Weekly predictions
    confidence_intervals: List[Tuple[float, float]]  # (lower, upper) bounds
    breakthrough_windows: List[Tuple[datetime, float]]  # (time, probability)
    setback_risks: List[Tuple[datetime, str, float]]  # (time, type, probability)
    optimal_interventions: List[Tuple[datetime, RecoveryIntervention]]
    expected_milestones: Dict[str, datetime]  # milestone -> expected date

@dataclass
class PersonalizedDevelopmentPlan:
    """Actionable development plan based on predictions"""
    trajectory: DevelopmentTrajectory
    immediate_actions: List[RecoveryIntervention]
    weekly_protocols: Dict[int, List[RecoveryIntervention]]  # week -> interventions
    monthly_assessments: List[str]
    support_requirements: Dict[str, str]  # type -> description
    success_probability: float

class CoherenceDevelopmentPredictor:
    """Predicts coherence development and optimizes intervention timing"""
    
    def __init__(self):
        # Individual development patterns
        self.development_archetypes = {
            'steady_builder': {
                'description': 'Consistent gradual improvement',
                'psi_rate': 0.02, 'rho_rate': 0.015, 'q_rate': 0.01, 'f_rate': 0.015,
                'volatility': 0.1,
                'breakthrough_probability': 0.05
            },
            'breakthrough_prone': {
                'description': 'Sudden jumps with plateaus',
                'psi_rate': 0.01, 'rho_rate': 0.02, 'q_rate': 0.015, 'f_rate': 0.01,
                'volatility': 0.3,
                'breakthrough_probability': 0.15
            },
            'cyclical_developer': {
                'description': 'Up and down cycles but trending upward',
                'psi_rate': 0.015, 'rho_rate': 0.01, 'q_rate': 0.02, 'f_rate': 0.02,
                'volatility': 0.25,
                'breakthrough_probability': 0.08
            },
            'resistant_learner': {
                'description': 'Slow start then acceleration',
                'psi_rate': 0.005, 'rho_rate': 0.025, 'q_rate': 0.005, 'f_rate': 0.01,
                'volatility': 0.15,
                'breakthrough_probability': 0.03
            }
        }
        
        # Life context modifiers
        self.context_modifiers = {
            'high_stress': {'rate_modifier': 0.5, 'volatility_modifier': 1.5},
            'supportive_environment': {'rate_modifier': 1.3, 'volatility_modifier': 0.8},
            'isolation': {'rate_modifier': 0.7, 'volatility_modifier': 1.2},
            'crisis': {'rate_modifier': 0.3, 'volatility_modifier': 2.0},
            'optimal_conditions': {'rate_modifier': 1.5, 'volatility_modifier': 0.7}
        }
        
        # Intervention effectiveness by personality
        self.intervention_personality_fit = {
            'introvert': {
                'reflection': 1.2,
                'social_activity': 0.7,
                'public_commitment': 0.6,
                'solitary_practice': 1.3
            },
            'extravert': {
                'reflection': 0.8,
                'social_activity': 1.3,
                'public_commitment': 1.2,
                'solitary_practice': 0.7
            },
            'analytical': {
                'reflection': 1.3,
                'social_activity': 0.9,
                'public_commitment': 0.8,
                'solitary_practice': 1.1
            },
            'intuitive': {
                'reflection': 0.9,
                'social_activity': 1.1,
                'public_commitment': 1.0,
                'solitary_practice': 0.9
            }
        }
    
    def identify_development_archetype(self,
                                     coherence_history: List[CoherenceProfile],
                                     personality_assessment: Optional[Dict[str, float]] = None) -> str:
        """
        Identify which development archetype best fits the individual
        """
        if len(coherence_history) < 3:
            # Default to steady builder without enough history
            return 'steady_builder'
        
        # Calculate development characteristics
        coherence_values = [p.static_coherence for p in coherence_history]
        
        # Calculate volatility
        if len(coherence_values) > 1:
            volatility = np.std(np.diff(coherence_values))
        else:
            volatility = 0.1
        
        # Calculate average improvement rate
        time_span = (coherence_history[-1].timestamp - coherence_history[0].timestamp).days
        if time_span > 0:
            total_improvement = coherence_values[-1] - coherence_values[0]
            daily_rate = total_improvement / time_span
        else:
            daily_rate = 0
        
        # Look for breakthrough patterns
        breakthroughs = 0
        for i in range(1, len(coherence_values)):
            if coherence_values[i] - coherence_values[i-1] > 0.2:
                breakthroughs += 1
        
        # Match to archetype
        if volatility > 0.25 and breakthroughs > 0:
            return 'breakthrough_prone'
        elif volatility > 0.2:
            return 'cyclical_developer'
        elif daily_rate < 0.001 and len(coherence_history) < 10:
            return 'resistant_learner'
        else:
            return 'steady_builder'
    
    def predict_development_trajectory(self,
                                     current_profile: CoherenceProfile,
                                     coherence_history: List[CoherenceProfile],
                                     life_context: Dict[str, any],
                                     support_system: Dict[str, any],
                                     time_horizon_weeks: int = 12) -> DevelopmentTrajectory:
        """
        Predict coherence development over specified time horizon
        """
        # Identify development archetype
        archetype = self.identify_development_archetype(coherence_history)
        archetype_params = self.development_archetypes[archetype]
        
        # Apply context modifiers
        context_modifier = self._calculate_context_modifier(life_context)
        
        # Generate weekly predictions
        predicted_profiles = []
        confidence_intervals = []
        current_variables = current_profile.variables
        
        for week in range(1, time_horizon_weeks + 1):
            # Calculate expected improvement
            week_improvement = self._calculate_weekly_improvement(
                current_variables,
                archetype_params,
                context_modifier,
                current_profile.individual_optimization
            )
            
            # Add stochastic variation
            noise = np.random.normal(0, archetype_params['volatility'] * 0.1, 4)
            
            # Update variables
            new_psi = max(0, min(1, current_variables.psi + week_improvement['psi'] + noise[0]))
            new_rho = max(0, min(1, current_variables.rho + week_improvement['rho'] + noise[1]))
            new_q = max(0, min(1, current_variables.q + week_improvement['q'] + noise[2]))
            new_f = max(0, min(1, current_variables.f + week_improvement['f'] + noise[3]))
            
            new_variables = CoherenceVariables(psi=new_psi, rho=new_rho, q=new_q, f=new_f)
            
            # Create predicted profile
            predicted_profile = CoherenceProfile(
                user_id=current_profile.user_id,
                variables=new_variables,
                static_coherence=self._calculate_coherence(new_variables),
                assessment_tier=current_profile.assessment_tier,
                timestamp=current_profile.timestamp + timedelta(weeks=week),
                individual_optimization=current_profile.individual_optimization
            )
            
            predicted_profiles.append(predicted_profile)
            
            # Calculate confidence interval
            uncertainty = archetype_params['volatility'] * np.sqrt(week)
            lower_bound = max(0, predicted_profile.static_coherence - uncertainty)
            upper_bound = min(4, predicted_profile.static_coherence + uncertainty)
            confidence_intervals.append((lower_bound, upper_bound))
            
            # Update for next iteration
            current_variables = new_variables
        
        # Identify breakthrough windows
        breakthrough_windows = self._identify_breakthrough_windows(
            predicted_profiles,
            archetype_params['breakthrough_probability']
        )
        
        # Identify setback risks
        setback_risks = self._identify_setback_risks(
            predicted_profiles,
            life_context,
            support_system
        )
        
        # Generate optimal interventions
        optimal_interventions = self._generate_optimal_interventions(
            current_profile,
            predicted_profiles,
            archetype
        )
        
        # Define expected milestones
        milestones = self._define_milestones(current_profile, predicted_profiles)
        
        return DevelopmentTrajectory(
            user_id=current_profile.user_id,
            baseline_profile=current_profile,
            predicted_profiles=predicted_profiles,
            confidence_intervals=confidence_intervals,
            breakthrough_windows=breakthrough_windows,
            setback_risks=setback_risks,
            optimal_interventions=optimal_interventions,
            expected_milestones=milestones
        )
    
    def generate_personalized_plan(self,
                                 trajectory: DevelopmentTrajectory,
                                 available_time_daily: int,
                                 personality_type: str,
                                 constraints: Dict[str, any]) -> PersonalizedDevelopmentPlan:
        """
        Generate actionable development plan from trajectory prediction
        """
        # Select immediate actions based on current needs
        immediate_actions = self._select_immediate_interventions(
            trajectory.baseline_profile,
            available_time_daily,
            personality_type
        )
        
        # Build weekly protocols
        weekly_protocols = {}
        for week in range(12):
            week_profile = trajectory.predicted_profiles[week] if week < len(trajectory.predicted_profiles) else None
            if week_profile:
                weekly_protocols[week + 1] = self._select_weekly_interventions(
                    week_profile,
                    trajectory.optimal_interventions,
                    available_time_daily,
                    personality_type
                )
        
        # Define monthly assessments
        monthly_assessments = [
            "Complete coherence assessment to track progress",
            "Review and adjust intervention effectiveness",
            "Identify new challenges or opportunities",
            "Celebrate improvements and milestones"
        ]
        
        # Determine support requirements
        support_requirements = self._determine_support_needs(
            trajectory,
            constraints
        )
        
        # Calculate success probability
        success_probability = self._calculate_success_probability(
            trajectory,
            constraints,
            support_requirements
        )
        
        return PersonalizedDevelopmentPlan(
            trajectory=trajectory,
            immediate_actions=immediate_actions,
            weekly_protocols=weekly_protocols,
            monthly_assessments=monthly_assessments,
            support_requirements=support_requirements,
            success_probability=success_probability
        )
    
    def _calculate_context_modifier(self, life_context: Dict[str, any]) -> Dict[str, float]:
        """Calculate how life context affects development rates"""
        # Start with neutral modifier
        rate_modifier = 1.0
        volatility_modifier = 1.0
        
        # Apply context effects
        if life_context.get('stress_level', 5) > 7:
            modifiers = self.context_modifiers['high_stress']
            rate_modifier *= modifiers['rate_modifier']
            volatility_modifier *= modifiers['volatility_modifier']
        
        if life_context.get('social_support', 5) > 7:
            modifiers = self.context_modifiers['supportive_environment']
            rate_modifier *= modifiers['rate_modifier']
            volatility_modifier *= modifiers['volatility_modifier']
        
        if life_context.get('major_transition', False):
            modifiers = self.context_modifiers['crisis']
            rate_modifier *= modifiers['rate_modifier']
            volatility_modifier *= modifiers['volatility_modifier']
        
        return {
            'rate_modifier': rate_modifier,
            'volatility_modifier': volatility_modifier
        }
    
    def _calculate_weekly_improvement(self,
                                    current_variables: CoherenceVariables,
                                    archetype_params: Dict[str, any],
                                    context_modifier: Dict[str, float],
                                    individual_optimization: Dict[str, float]) -> Dict[str, float]:
        """Calculate expected weekly improvement for each variable"""
        improvements = {}
        
        # Base rates from archetype
        base_rates = {
            'psi': archetype_params['psi_rate'],
            'rho': archetype_params['rho_rate'],
            'q': archetype_params['q_rate'],
            'f': archetype_params['f_rate']
        }
        
        # Apply context modifier
        for var, rate in base_rates.items():
            improvements[var] = rate * context_modifier['rate_modifier'] * 7  # Convert to weekly
            
            # Diminishing returns as variables approach 1.0
            current_value = getattr(current_variables, var)
            improvements[var] *= (1.0 - current_value)
            
            # Individual optimization effects
            if var == 'q' and 'K_i' in individual_optimization:
                improvements[var] *= (1 + individual_optimization['K_i'] * 0.2)
        
        return improvements
    
    def _calculate_coherence(self, variables: CoherenceVariables) -> float:
        """Calculate static coherence from variables"""
        return (variables.psi + 
                (variables.rho * variables.psi) + 
                variables.q + 
                (variables.f * variables.psi))
    
    def _identify_breakthrough_windows(self,
                                     predicted_profiles: List[CoherenceProfile],
                                     base_probability: float) -> List[Tuple[datetime, float]]:
        """Identify windows where breakthroughs are most likely"""
        breakthrough_windows = []
        
        for i, profile in enumerate(predicted_profiles):
            # Breakthrough probability increases when all variables are improving
            if i > 0:
                prev_profile = predicted_profiles[i-1]
                improvement_count = sum([
                    profile.variables.psi > prev_profile.variables.psi,
                    profile.variables.rho > prev_profile.variables.rho,
                    profile.variables.q > prev_profile.variables.q,
                    profile.variables.f > prev_profile.variables.f
                ])
                
                if improvement_count >= 3:
                    probability = base_probability * 1.5
                    breakthrough_windows.append((profile.timestamp, probability))
                elif improvement_count >= 2:
                    probability = base_probability
                    breakthrough_windows.append((profile.timestamp, probability))
        
        return breakthrough_windows
    
    def _identify_setback_risks(self,
                              predicted_profiles: List[CoherenceProfile],
                              life_context: Dict[str, any],
                              support_system: Dict[str, any]) -> List[Tuple[datetime, str, float]]:
        """Identify periods of elevated setback risk"""
        setback_risks = []
        
        # Known risk periods
        risk_factors = {
            'holiday_season': {'months': [11, 12], 'risk': 0.3, 'type': 'social_pressure'},
            'work_deadlines': {'risk': 0.25, 'type': 'stress_overload'},
            'isolation_risk': {'risk': 0.35, 'type': 'social_disconnection'},
            'health_issues': {'risk': 0.4, 'type': 'physical_limitation'}
        }
        
        for i, profile in enumerate(predicted_profiles):
            month = profile.timestamp.month
            
            # Holiday season risk
            if month in risk_factors['holiday_season']['months']:
                setback_risks.append((
                    profile.timestamp,
                    risk_factors['holiday_season']['type'],
                    risk_factors['holiday_season']['risk']
                ))
            
            # Low support system risk
            if support_system.get('quality', 5) < 3:
                if i % 4 == 0:  # Monthly check
                    setback_risks.append((
                        profile.timestamp,
                        risk_factors['isolation_risk']['type'],
                        risk_factors['isolation_risk']['risk']
                    ))
        
        return setback_risks
    
    def _generate_optimal_interventions(self,
                                      baseline: CoherenceProfile,
                                      predictions: List[CoherenceProfile],
                                      archetype: str) -> List[Tuple[datetime, RecoveryIntervention]]:
        """Generate optimally timed interventions"""
        interventions = []
        
        # Focus on lowest variable initially
        lowest_var = min(['psi', 'rho', 'q', 'f'], 
                        key=lambda v: getattr(baseline.variables, v))
        
        # Schedule intensive intervention for lowest variable in week 1
        interventions.append((
            baseline.timestamp + timedelta(weeks=1),
            RecoveryIntervention(
                variable_target=lowest_var,
                intervention_type='intensive_focus',
                description=f'Intensive work on {lowest_var}',
                expected_impact=0.1,
                time_required_minutes=60,
                difficulty_level=3,
                prerequisites=[]
            )
        ))
        
        # Add maintenance interventions
        for i in range(2, 12, 2):  # Every 2 weeks
            if i < len(predictions):
                interventions.append((
                    predictions[i].timestamp,
                    RecoveryIntervention(
                        variable_target='all',
                        intervention_type='integration',
                        description='Integration and reflection practice',
                        expected_impact=0.05,
                        time_required_minutes=45,
                        difficulty_level=2,
                        prerequisites=[]
                    )
                ))
        
        return interventions
    
    def _define_milestones(self,
                         baseline: CoherenceProfile,
                         predictions: List[CoherenceProfile]) -> Dict[str, datetime]:
        """Define expected milestone achievements"""
        milestones = {}
        
        # Coherence milestones
        coherence_targets = [2.0, 2.5, 3.0]
        for target in coherence_targets:
            if baseline.static_coherence < target:
                for profile in predictions:
                    if profile.static_coherence >= target:
                        milestones[f'coherence_{target}'] = profile.timestamp
                        break
        
        # Variable milestones
        variable_targets = {'psi': 0.7, 'rho': 0.6, 'q': 0.5, 'f': 0.6}
        for var, target in variable_targets.items():
            current_value = getattr(baseline.variables, var)
            if current_value < target:
                for profile in predictions:
                    if getattr(profile.variables, var) >= target:
                        milestones[f'{var}_{target}'] = profile.timestamp
                        break
        
        return milestones
    
    def _select_immediate_interventions(self,
                                      profile: CoherenceProfile,
                                      time_available: int,
                                      personality: str) -> List[RecoveryIntervention]:
        """Select best immediate interventions based on profile and personality"""
        # This would integrate with the recovery module
        # Simplified version here
        interventions = []
        
        # Focus on lowest variable
        variables = {'psi': profile.variables.psi, 
                    'rho': profile.variables.rho,
                    'q': profile.variables.q,
                    'f': profile.variables.f}
        lowest_var = min(variables.items(), key=lambda x: x[1])[0]
        
        interventions.append(
            RecoveryIntervention(
                variable_target=lowest_var,
                intervention_type='targeted_improvement',
                description=f'Focus intervention for {lowest_var}',
                expected_impact=0.05,
                time_required_minutes=min(time_available, 30),
                difficulty_level=2,
                prerequisites=[]
            )
        )
        
        return interventions
    
    def _select_weekly_interventions(self,
                                   profile: CoherenceProfile,
                                   scheduled: List[Tuple[datetime, RecoveryIntervention]],
                                   time_available: int,
                                   personality: str) -> List[RecoveryIntervention]:
        """Select interventions for a specific week"""
        # Check if there are scheduled interventions for this week
        week_interventions = [
            intervention for timestamp, intervention in scheduled
            if abs((timestamp - profile.timestamp).days) < 7
        ]
        
        return week_interventions[:3]  # Limit to 3 per week
    
    def _determine_support_needs(self,
                               trajectory: DevelopmentTrajectory,
                               constraints: Dict[str, any]) -> Dict[str, str]:
        """Determine what support is needed for success"""
        support_needs = {}
        
        # Check for high volatility
        if any(ci[1] - ci[0] > 1.0 for ci in trajectory.confidence_intervals):
            support_needs['stability_support'] = 'Regular check-ins with coach or therapist'
        
        # Check for low social variable
        if trajectory.baseline_profile.variables.f < 0.4:
            support_needs['social_support'] = 'Join supportive community or group'
        
        # Check for setback risks
        if len(trajectory.setback_risks) > 3:
            support_needs['risk_mitigation'] = 'Develop contingency plans for high-risk periods'
        
        return support_needs
    
    def _calculate_success_probability(self,
                                     trajectory: DevelopmentTrajectory,
                                     constraints: Dict[str, any],
                                     support: Dict[str, str]) -> float:
        """Calculate probability of achieving development goals"""
        base_probability = 0.6
        
        # Positive factors
        if len(support) >= 2:
            base_probability += 0.1
        
        if trajectory.baseline_profile.variables.rho > 0.5:
            base_probability += 0.05
        
        # Negative factors
        if constraints.get('time_available', 60) < 30:
            base_probability -= 0.1
        
        if len(trajectory.setback_risks) > 5:
            base_probability -= 0.1
        
        return max(0.1, min(0.95, base_probability))