# Coherence Contagion Modeling
# Models how coherence spreads and influences groups

import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import networkx as nx

# Import core types
from gct_backend import CoherenceProfile, CoherenceVariables

class GroupType(Enum):
    FAMILY = "family"
    WORK_TEAM = "work_team"
    SOCIAL_CIRCLE = "social_circle"
    COMMUNITY = "community"
    ONLINE_GROUP = "online_group"
    ORGANIZATION = "organization"

class ContagionMechanism(Enum):
    DIRECT_INFLUENCE = "direct"          # One-on-one interactions
    FIELD_EFFECT = "field"               # Ambient group coherence
    ROLE_MODELING = "role_modeling"      # Following high-coherence individuals
    EMOTIONAL_CONTAGION = "emotional"    # Mood and energy spreading
    STRUCTURAL = "structural"            # System/process induced

@dataclass
class GroupCoherenceState:
    """Current coherence state of a group"""
    group_id: str
    group_type: GroupType
    timestamp: datetime
    average_coherence: float
    coherence_variance: float
    member_count: int
    coherence_distribution: Dict[str, float]  # member_id -> coherence
    field_strength: float  # 0-1, how strong the group field effect is
    stability_score: float  # 0-1, how stable the current state is

@dataclass
class ContagionEvent:
    """A coherence transmission event"""
    source_id: str
    target_id: str
    mechanism: ContagionMechanism
    timestamp: datetime
    coherence_change: float
    variables_affected: Dict[str, float]  # which variables changed
    interaction_quality: float  # 0-1, quality of the interaction

class CoherenceContagionModel:
    """Models coherence transmission in groups"""
    
    def __init__(self):
        # Base transmission rates by mechanism
        self.transmission_rates = {
            ContagionMechanism.DIRECT_INFLUENCE: 0.15,
            ContagionMechanism.FIELD_EFFECT: 0.05,
            ContagionMechanism.ROLE_MODELING: 0.10,
            ContagionMechanism.EMOTIONAL_CONTAGION: 0.08,
            ContagionMechanism.STRUCTURAL: 0.12
        }
        
        # Group-specific parameters
        self.group_parameters = {
            GroupType.FAMILY: {
                'field_strength_base': 0.8,
                'interaction_frequency': 0.9,
                'boundary_permeability': 0.3,
                'hierarchy_effect': 0.6
            },
            GroupType.WORK_TEAM: {
                'field_strength_base': 0.6,
                'interaction_frequency': 0.7,
                'boundary_permeability': 0.5,
                'hierarchy_effect': 0.8
            },
            GroupType.SOCIAL_CIRCLE: {
                'field_strength_base': 0.4,
                'interaction_frequency': 0.5,
                'boundary_permeability': 0.7,
                'hierarchy_effect': 0.3
            },
            GroupType.COMMUNITY: {
                'field_strength_base': 0.5,
                'interaction_frequency': 0.4,
                'boundary_permeability': 0.6,
                'hierarchy_effect': 0.5
            },
            GroupType.ONLINE_GROUP: {
                'field_strength_base': 0.3,
                'interaction_frequency': 0.6,
                'boundary_permeability': 0.9,
                'hierarchy_effect': 0.4
            },
            GroupType.ORGANIZATION: {
                'field_strength_base': 0.7,
                'interaction_frequency': 0.6,
                'boundary_permeability': 0.4,
                'hierarchy_effect': 0.9
            }
        }
        
        # Threshold effects
        self.coherence_thresholds = {
            'breakdown': 1.2,      # Below this, group starts breaking down
            'struggling': 1.8,     # Group functioning but with difficulty
            'functional': 2.2,     # Normal functioning
            'thriving': 2.8,       # High performance state
            'transcendent': 3.2    # Exceptional group coherence
        }
    
    def calculate_group_coherence_field(self, 
                                      member_profiles: List[CoherenceProfile],
                                      group_type: GroupType,
                                      interaction_matrix: Optional[np.ndarray] = None) -> GroupCoherenceState:
        """
        Calculate the coherence field strength and state of a group
        """
        if not member_profiles:
            raise ValueError("Need at least one member to calculate group coherence")
        
        # Basic statistics
        coherences = [p.static_coherence for p in member_profiles]
        avg_coherence = np.mean(coherences)
        coherence_variance = np.var(coherences)
        
        # Calculate field strength
        base_field = self.group_parameters[group_type]['field_strength_base']
        
        # Field strength increases with coherence alignment (lower variance)
        alignment_factor = 1.0 / (1.0 + coherence_variance)
        
        # Field strength increases with average coherence
        coherence_factor = min(1.0, avg_coherence / 3.0)
        
        field_strength = base_field * alignment_factor * coherence_factor
        
        # Calculate stability
        stability = self._calculate_group_stability(
            coherences, 
            group_type,
            interaction_matrix
        )
        
        # Create distribution map
        distribution = {
            str(p.user_id): p.static_coherence 
            for p in member_profiles
        }
        
        return GroupCoherenceState(
            group_id=f"{group_type.value}_{datetime.now().timestamp()}",
            group_type=group_type,
            timestamp=datetime.now(),
            average_coherence=avg_coherence,
            coherence_variance=coherence_variance,
            member_count=len(member_profiles),
            coherence_distribution=distribution,
            field_strength=field_strength,
            stability_score=stability
        )
    
    def predict_individual_impact(self,
                                individual_profile: CoherenceProfile,
                                group_state: GroupCoherenceState,
                                exposure_hours_per_week: float) -> Dict[str, float]:
        """
        Predict how group field affects individual coherence
        """
        # Calculate coherence differential
        coherence_diff = group_state.average_coherence - individual_profile.static_coherence
        
        # Field effect is stronger when individual is far from group average
        field_pull_strength = group_state.field_strength * abs(coherence_diff) / 3.0
        
        # Direction of pull (toward group average)
        pull_direction = np.sign(coherence_diff)
        
        # Exposure effect
        exposure_factor = min(1.0, exposure_hours_per_week / 40.0)
        
        # Individual resistance based on their own coherence
        # High coherence individuals are less affected by low coherence groups
        if individual_profile.static_coherence > 2.5 and coherence_diff < 0:
            resistance_factor = 0.5
        else:
            resistance_factor = 1.0
        
        # Calculate per-variable impacts
        weekly_impact = field_pull_strength * pull_direction * exposure_factor * resistance_factor
        
        # Distribute impact across variables based on group type
        variable_impacts = self._distribute_field_impact(
            weekly_impact,
            individual_profile,
            group_state.group_type
        )
        
        return {
            'total_weekly_impact': weekly_impact,
            'variable_impacts': variable_impacts,
            'exposure_factor': exposure_factor,
            'resistance_factor': resistance_factor,
            'field_pull_strength': field_pull_strength
        }
    
    def model_dyadic_transmission(self,
                                source_profile: CoherenceProfile,
                                target_profile: CoherenceProfile,
                                interaction_quality: float,
                                interaction_duration_minutes: int) -> ContagionEvent:
        """
        Model coherence transmission between two individuals
        """
        # Asymmetric transmission based on GCT principles
        # High-ρ individuals transmit more, receive less
        source_transmission_power = (source_profile.variables.rho * 0.6 + 
                                   source_profile.variables.q * 0.4)
        target_reception_openness = 1.0 - (target_profile.variables.rho * 0.7)
        
        # Base transmission strength
        base_transmission = source_transmission_power * target_reception_openness
        
        # Adjust for interaction quality and duration
        quality_factor = interaction_quality
        duration_factor = min(1.0, interaction_duration_minutes / 60.0)
        
        # Calculate coherence differential
        coherence_diff = source_profile.static_coherence - target_profile.static_coherence
        
        # Transmission is stronger when source has higher coherence
        if coherence_diff > 0:
            transmission_strength = base_transmission * quality_factor * duration_factor
            coherence_change = transmission_strength * coherence_diff * 0.1
        else:
            # Negative transmission (dragging down) is weaker but still possible
            transmission_strength = base_transmission * quality_factor * duration_factor * 0.5
            coherence_change = transmission_strength * coherence_diff * 0.05
        
        # Determine which variables are most affected
        variables_affected = self._calculate_variable_transmission(
            source_profile,
            target_profile,
            transmission_strength
        )
        
        return ContagionEvent(
            source_id=source_profile.user_id,
            target_id=target_profile.user_id,
            mechanism=ContagionMechanism.DIRECT_INFLUENCE,
            timestamp=datetime.now(),
            coherence_change=coherence_change,
            variables_affected=variables_affected,
            interaction_quality=interaction_quality
        )
    
    def identify_coherence_catalysts(self,
                                   group_profiles: List[CoherenceProfile],
                                   interaction_network: Optional[nx.Graph] = None) -> List[Tuple[str, float]]:
        """
        Identify individuals who could catalyze group coherence improvement
        """
        catalysts = []
        
        for profile in group_profiles:
            catalyst_score = 0
            
            # High coherence is necessary but not sufficient
            if profile.static_coherence > 2.5:
                catalyst_score += 0.3
            
            # High wisdom enables better transmission
            if profile.variables.rho > 0.7:
                catalyst_score += 0.2
            
            # High social belonging means better connections
            if profile.variables.f > 0.7:
                catalyst_score += 0.2
            
            # Moral activation drives change
            if profile.variables.q > 0.6:
                catalyst_score += 0.15
            
            # Network position matters if we have network data
            if interaction_network and profile.user_id in interaction_network:
                centrality = nx.degree_centrality(interaction_network)[profile.user_id]
                catalyst_score += centrality * 0.15
            
            catalysts.append((profile.user_id, catalyst_score))
        
        # Sort by catalyst potential
        catalysts.sort(key=lambda x: x[1], reverse=True)
        
        return catalysts
    
    def predict_group_trajectory(self,
                               current_state: GroupCoherenceState,
                               planned_interventions: Optional[List[Dict[str, any]]] = None,
                               time_horizon_days: int = 30) -> Dict[str, any]:
        """
        Predict group coherence trajectory with or without interventions
        """
        # Baseline trajectory without intervention
        baseline_trajectory = self._calculate_natural_trajectory(
            current_state,
            time_horizon_days
        )
        
        # Intervention trajectory if provided
        if planned_interventions:
            intervention_trajectory = self._calculate_intervention_trajectory(
                current_state,
                planned_interventions,
                time_horizon_days
            )
        else:
            intervention_trajectory = None
        
        # Identify critical thresholds
        critical_points = self._identify_critical_points(
            current_state,
            baseline_trajectory
        )
        
        # Generate recommendations
        recommendations = self._generate_group_recommendations(
            current_state,
            baseline_trajectory,
            critical_points
        )
        
        return {
            'current_state': {
                'average_coherence': current_state.average_coherence,
                'field_strength': current_state.field_strength,
                'stability': current_state.stability_score
            },
            'baseline_trajectory': baseline_trajectory,
            'intervention_trajectory': intervention_trajectory,
            'critical_points': critical_points,
            'recommendations': recommendations
        }
    
    def _calculate_group_stability(self,
                                 coherences: List[float],
                                 group_type: GroupType,
                                 interaction_matrix: Optional[np.ndarray]) -> float:
        """
        Calculate how stable the current group coherence state is
        """
        # Base stability from coherence variance
        variance_stability = 1.0 / (1.0 + np.var(coherences))
        
        # Stability from average coherence level
        avg_coherence = np.mean(coherences)
        if avg_coherence < self.coherence_thresholds['breakdown']:
            level_stability = 0.2
        elif avg_coherence < self.coherence_thresholds['struggling']:
            level_stability = 0.4
        elif avg_coherence < self.coherence_thresholds['functional']:
            level_stability = 0.6
        elif avg_coherence < self.coherence_thresholds['thriving']:
            level_stability = 0.8
        else:
            level_stability = 0.9
        
        # Network stability if available
        if interaction_matrix is not None:
            # More connections generally mean more stability
            density = np.mean(interaction_matrix)
            network_stability = min(1.0, density * 2)
        else:
            network_stability = 0.5
        
        # Combine factors
        total_stability = (variance_stability * 0.3 + 
                          level_stability * 0.5 + 
                          network_stability * 0.2)
        
        return total_stability
    
    def _distribute_field_impact(self,
                               total_impact: float,
                               individual_profile: CoherenceProfile,
                               group_type: GroupType) -> Dict[str, float]:
        """
        Distribute field effect impact across coherence variables
        """
        # Different group types affect different variables more strongly
        impact_distributions = {
            GroupType.FAMILY: {'psi': 0.2, 'rho': 0.3, 'q': 0.1, 'f': 0.4},
            GroupType.WORK_TEAM: {'psi': 0.3, 'rho': 0.2, 'q': 0.3, 'f': 0.2},
            GroupType.SOCIAL_CIRCLE: {'psi': 0.2, 'rho': 0.2, 'q': 0.2, 'f': 0.4},
            GroupType.COMMUNITY: {'psi': 0.2, 'rho': 0.3, 'q': 0.3, 'f': 0.2},
            GroupType.ONLINE_GROUP: {'psi': 0.3, 'rho': 0.1, 'q': 0.4, 'f': 0.2},
            GroupType.ORGANIZATION: {'psi': 0.4, 'rho': 0.2, 'q': 0.2, 'f': 0.2}
        }
        
        distribution = impact_distributions[group_type]
        
        return {
            'psi': total_impact * distribution['psi'],
            'rho': total_impact * distribution['rho'],
            'q': total_impact * distribution['q'],
            'f': total_impact * distribution['f']
        }
    
    def _calculate_variable_transmission(self,
                                       source: CoherenceProfile,
                                       target: CoherenceProfile,
                                       transmission_strength: float) -> Dict[str, float]:
        """
        Calculate which variables are transmitted in dyadic interaction
        """
        variable_diffs = {
            'psi': source.variables.psi - target.variables.psi,
            'rho': source.variables.rho - target.variables.rho,
            'q': source.variables.q - target.variables.q,
            'f': source.variables.f - target.variables.f
        }
        
        # Transmission is proportional to difference and transmission strength
        transmitted = {}
        for var, diff in variable_diffs.items():
            transmitted[var] = diff * transmission_strength * 0.1
        
        return transmitted
    
    def _calculate_natural_trajectory(self,
                                    current_state: GroupCoherenceState,
                                    days: int) -> List[float]:
        """
        Calculate group coherence trajectory without intervention
        """
        trajectory = [current_state.average_coherence]
        current_coherence = current_state.average_coherence
        
        for day in range(1, days + 1):
            # Natural drift based on current level
            if current_coherence < self.coherence_thresholds['breakdown']:
                # Rapid deterioration below breakdown threshold
                daily_change = -0.01 * (1.5 - current_state.stability_score)
            elif current_coherence < self.coherence_thresholds['struggling']:
                # Slow deterioration
                daily_change = -0.005 * (1.2 - current_state.stability_score)
            elif current_coherence < self.coherence_thresholds['functional']:
                # Relatively stable
                daily_change = -0.002 * (1.0 - current_state.stability_score)
            else:
                # Slight natural improvement at high levels
                daily_change = 0.001 * current_state.stability_score
            
            current_coherence += daily_change
            trajectory.append(max(0, current_coherence))
        
        return trajectory
    
    def _calculate_intervention_trajectory(self,
                                         current_state: GroupCoherenceState,
                                         interventions: List[Dict[str, any]],
                                         days: int) -> List[float]:
        """
        Calculate trajectory with planned interventions
        """
        trajectory = [current_state.average_coherence]
        current_coherence = current_state.average_coherence
        
        # Process interventions by day
        interventions_by_day = {}
        for intervention in interventions:
            day = intervention.get('day', 1)
            if day not in interventions_by_day:
                interventions_by_day[day] = []
            interventions_by_day[day].append(intervention)
        
        for day in range(1, days + 1):
            # Apply natural trajectory
            daily_change = -0.002 * (1.0 - current_state.stability_score)
            
            # Apply interventions if scheduled
            if day in interventions_by_day:
                for intervention in interventions_by_day[day]:
                    impact = intervention.get('expected_impact', 0.05)
                    daily_change += impact
            
            current_coherence += daily_change
            trajectory.append(max(0, current_coherence))
        
        return trajectory
    
    def _identify_critical_points(self,
                                current_state: GroupCoherenceState,
                                trajectory: List[float]) -> List[Dict[str, any]]:
        """
        Identify critical threshold crossings in trajectory
        """
        critical_points = []
        
        for i, coherence in enumerate(trajectory[1:], 1):
            prev_coherence = trajectory[i-1]
            
            # Check threshold crossings
            for threshold_name, threshold_value in self.coherence_thresholds.items():
                if prev_coherence >= threshold_value > coherence:
                    critical_points.append({
                        'day': i,
                        'type': 'crossing_down',
                        'threshold': threshold_name,
                        'value': threshold_value,
                        'severity': 'high' if threshold_name in ['breakdown', 'struggling'] else 'medium'
                    })
                elif prev_coherence < threshold_value <= coherence:
                    critical_points.append({
                        'day': i,
                        'type': 'crossing_up',
                        'threshold': threshold_name,
                        'value': threshold_value,
                        'severity': 'positive'
                    })
        
        return critical_points
    
    def _generate_group_recommendations(self,
                                      current_state: GroupCoherenceState,
                                      trajectory: List[float],
                                      critical_points: List[Dict[str, any]]) -> List[str]:
        """
        Generate recommendations for group coherence improvement
        """
        recommendations = []
        
        # Current state recommendations
        if current_state.average_coherence < self.coherence_thresholds['struggling']:
            recommendations.append("⚠️ Group coherence critically low - immediate intervention needed")
            recommendations.append("Consider bringing in external facilitation or coaching")
        
        if current_state.coherence_variance > 0.5:
            recommendations.append("High coherence variance - focus on alignment activities")
            recommendations.append("Pair high and low coherence members for mutual benefit")
        
        if current_state.field_strength < 0.3:
            recommendations.append("Weak group field - increase meaningful interactions")
            recommendations.append("Create regular rituals that reinforce group identity")
        
        # Trajectory-based recommendations
        if trajectory[-1] < trajectory[0]:
            recommendations.append("Declining trajectory - implement coherence-building practices")
        
        # Critical point recommendations
        breakdown_crossings = [cp for cp in critical_points 
                             if cp['threshold'] == 'breakdown' and cp['type'] == 'crossing_down']
        if breakdown_crossings:
            days_to_breakdown = breakdown_crossings[0]['day']
            recommendations.append(f"⚠️ Group will cross breakdown threshold in {days_to_breakdown} days without intervention")
        
        # Type-specific recommendations
        if current_state.group_type == GroupType.WORK_TEAM:
            recommendations.append("Implement daily standup with coherence check-in")
            recommendations.append("Create psychological safety for authentic expression")
        elif current_state.group_type == GroupType.FAMILY:
            recommendations.append("Establish device-free family time for authentic connection")
            recommendations.append("Practice active listening without judgment")
        
        return recommendations