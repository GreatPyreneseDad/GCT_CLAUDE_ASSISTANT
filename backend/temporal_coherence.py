# Temporal Coherence Patterns Module
# Analyzes coherence variations across time cycles and life transitions

import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

@dataclass
class TemporalPattern:
    """Represents a coherence pattern over time"""
    pattern_type: str  # 'circadian', 'weekly', 'monthly', 'transitional'
    peak_times: List[datetime]
    trough_times: List[datetime]
    average_amplitude: float
    consistency_score: float
    recommendations: List[str]

class CircadianType(Enum):
    MORNING_PEAK = "morning_peak"
    EVENING_PEAK = "evening_peak"
    MIDDAY_PEAK = "midday_peak"
    VARIABLE = "variable"

class TemporalCoherenceAnalyzer:
    """Analyzes coherence patterns across time cycles"""
    
    def __init__(self):
        self.circadian_windows = {
            'early_morning': (5, 8),    # 5am-8am
            'morning': (8, 12),         # 8am-12pm
            'afternoon': (12, 17),      # 12pm-5pm
            'evening': (17, 21),        # 5pm-9pm
            'night': (21, 24),          # 9pm-12am
        }
        
        self.life_transitions = {
            'career_change': {'typical_duration_days': 180, 'coherence_impact': -0.15},
            'relationship_start': {'typical_duration_days': 90, 'coherence_impact': 0.10},
            'relationship_end': {'typical_duration_days': 120, 'coherence_impact': -0.25},
            'relocation': {'typical_duration_days': 60, 'coherence_impact': -0.10},
            'loss_grief': {'typical_duration_days': 365, 'coherence_impact': -0.30},
            'new_child': {'typical_duration_days': 180, 'coherence_impact': -0.20},
            'health_crisis': {'typical_duration_days': 90, 'coherence_impact': -0.25},
            'achievement': {'typical_duration_days': 30, 'coherence_impact': 0.15},
        }
    
    def analyze_circadian_pattern(self, timestamped_assessments: List[Tuple[datetime, float]]) -> CircadianType:
        """
        Identify individual's circadian coherence pattern
        Returns their peak coherence time of day
        """
        if len(timestamped_assessments) < 10:
            return CircadianType.VARIABLE
        
        # Group assessments by time window
        window_coherences = {window: [] for window in self.circadian_windows}
        
        for timestamp, coherence in timestamped_assessments:
            hour = timestamp.hour
            for window, (start, end) in self.circadian_windows.items():
                if start <= hour < end:
                    window_coherences[window].append(coherence)
                    break
        
        # Calculate average coherence for each window
        window_averages = {}
        for window, coherences in window_coherences.items():
            if coherences:
                window_averages[window] = np.mean(coherences)
        
        if not window_averages:
            return CircadianType.VARIABLE
        
        # Find peak window
        peak_window = max(window_averages, key=window_averages.get)
        peak_value = window_averages[peak_window]
        
        # Check if there's a clear peak (>10% higher than others)
        other_values = [v for k, v in window_averages.items() if k != peak_window]
        if other_values and peak_value > np.mean(other_values) * 1.1:
            if peak_window in ['early_morning', 'morning']:
                return CircadianType.MORNING_PEAK
            elif peak_window == 'afternoon':
                return CircadianType.MIDDAY_PEAK
            elif peak_window == 'evening':
                return CircadianType.EVENING_PEAK
        
        return CircadianType.VARIABLE
    
    def analyze_weekly_pattern(self, daily_coherences: List[Tuple[datetime, float]]) -> Dict[str, float]:
        """
        Analyze weekly coherence cycles (stress accumulation/recovery)
        Returns pattern of coherence across days of week
        """
        if len(daily_coherences) < 14:  # Need at least 2 weeks
            return {}
        
        # Group by day of week (0=Monday, 6=Sunday)
        day_coherences = {i: [] for i in range(7)}
        
        for timestamp, coherence in daily_coherences:
            day_of_week = timestamp.weekday()
            day_coherences[day_of_week].append(coherence)
        
        # Calculate patterns
        weekly_pattern = {}
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        for day_num, coherences in day_coherences.items():
            if coherences:
                weekly_pattern[day_names[day_num]] = {
                    'average': np.mean(coherences),
                    'variability': np.std(coherences),
                    'sample_size': len(coherences)
                }
        
        return weekly_pattern
    
    def analyze_life_transition_impact(self, 
                                     coherence_history: List[Tuple[datetime, float]], 
                                     transition_events: List[Dict[str, any]]) -> List[Dict[str, any]]:
        """
        Analyze how life transitions affect coherence trajectory
        transition_events: [{'type': 'career_change', 'date': datetime, 'severity': 0.5-1.0}]
        """
        results = []
        
        for event in transition_events:
            event_type = event['type']
            event_date = event['date']
            severity = event.get('severity', 1.0)
            
            if event_type not in self.life_transitions:
                continue
            
            transition_info = self.life_transitions[event_type]
            expected_impact = transition_info['coherence_impact'] * severity
            expected_duration = transition_info['typical_duration_days']
            
            # Get coherence before, during, and after transition
            before_coherences = []
            during_coherences = []
            after_coherences = []
            
            for timestamp, coherence in coherence_history:
                days_from_event = (timestamp - event_date).days
                
                if -90 <= days_from_event < 0:
                    before_coherences.append(coherence)
                elif 0 <= days_from_event <= expected_duration:
                    during_coherences.append(coherence)
                elif expected_duration < days_from_event <= expected_duration + 90:
                    after_coherences.append(coherence)
            
            # Analyze recovery trajectory
            if before_coherences and during_coherences:
                baseline = np.mean(before_coherences)
                actual_impact = np.mean(during_coherences) - baseline
                
                recovery_data = {
                    'event_type': event_type,
                    'event_date': event_date,
                    'baseline_coherence': baseline,
                    'expected_impact': expected_impact,
                    'actual_impact': actual_impact,
                    'impact_accuracy': 1.0 - abs(actual_impact - expected_impact),
                }
                
                if after_coherences:
                    recovery_level = np.mean(after_coherences)
                    recovery_percent = (recovery_level - np.mean(during_coherences)) / abs(actual_impact) if actual_impact != 0 else 0
                    recovery_data['recovery_percent'] = recovery_percent
                    recovery_data['recovered_to'] = recovery_level
                    recovery_data['full_recovery'] = recovery_level >= baseline * 0.95
                
                results.append(recovery_data)
        
        return results
    
    def generate_temporal_insights(self, 
                                 circadian_type: CircadianType,
                                 weekly_pattern: Dict[str, float],
                                 transition_impacts: List[Dict[str, any]]) -> TemporalPattern:
        """
        Generate actionable insights from temporal analysis
        """
        recommendations = []
        peak_times = []
        trough_times = []
        
        # Circadian recommendations
        if circadian_type == CircadianType.MORNING_PEAK:
            recommendations.append("Schedule important decisions and difficult conversations in morning hours (8am-12pm)")
            recommendations.append("Avoid critical tasks after 6pm when your coherence naturally declines")
            peak_times.extend([datetime.now().replace(hour=9), datetime.now().replace(hour=10)])
            trough_times.extend([datetime.now().replace(hour=19), datetime.now().replace(hour=20)])
        elif circadian_type == CircadianType.EVENING_PEAK:
            recommendations.append("Your coherence peaks in evening (5pm-9pm) - ideal for important conversations")
            recommendations.append("Morning may not be optimal for critical decisions - consider delaying to afternoon")
            peak_times.extend([datetime.now().replace(hour=18), datetime.now().replace(hour=19)])
            trough_times.extend([datetime.now().replace(hour=7), datetime.now().replace(hour=8)])
        
        # Weekly pattern recommendations
        if weekly_pattern:
            best_day = max(weekly_pattern.items(), key=lambda x: x[1]['average'])[0]
            worst_day = min(weekly_pattern.items(), key=lambda x: x[1]['average'])[0]
            
            recommendations.append(f"Your coherence peaks on {best_day}s - schedule important meetings then")
            recommendations.append(f"Coherence typically lowest on {worst_day}s - plan lighter activities")
        
        # Transition recovery insights
        if transition_impacts:
            recent_transitions = [t for t in transition_impacts if (datetime.now() - t['event_date']).days < 180]
            if recent_transitions:
                for transition in recent_transitions:
                    if transition.get('recovery_percent', 0) < 0.8:
                        recommendations.append(f"Still recovering from {transition['event_type']} - be patient with yourself")
                    else:
                        recommendations.append(f"Excellent recovery from {transition['event_type']} - coherence restored")
        
        # Calculate overall temporal consistency
        consistency_scores = []
        if weekly_pattern:
            weekly_values = [v['average'] for v in weekly_pattern.values()]
            if weekly_values:
                consistency_scores.append(1.0 - (np.std(weekly_values) / (np.mean(weekly_values) + 0.001)))
        
        return TemporalPattern(
            pattern_type='composite',
            peak_times=peak_times,
            trough_times=trough_times,
            average_amplitude=0.15,  # Typical daily variation
            consistency_score=np.mean(consistency_scores) if consistency_scores else 0.5,
            recommendations=recommendations
        )
    
    def predict_optimal_timing(self, 
                             user_pattern: TemporalPattern,
                             activity_type: str,
                             constraints: Optional[Dict[str, any]] = None) -> Dict[str, any]:
        """
        Predict optimal timing for specific activities based on individual patterns
        """
        activity_requirements = {
            'difficult_conversation': {'coherence_needed': 0.8, 'duration_hours': 1},
            'major_decision': {'coherence_needed': 0.85, 'duration_hours': 2},
            'creative_work': {'coherence_needed': 0.7, 'duration_hours': 3},
            'routine_tasks': {'coherence_needed': 0.5, 'duration_hours': 2},
            'learning_new_skill': {'coherence_needed': 0.75, 'duration_hours': 2},
            'conflict_resolution': {'coherence_needed': 0.9, 'duration_hours': 1},
        }
        
        if activity_type not in activity_requirements:
            return {'error': 'Unknown activity type'}
        
        requirements = activity_requirements[activity_type]
        
        # Find optimal windows based on peak times
        optimal_windows = []
        for peak_time in user_pattern.peak_times:
            window_start = peak_time - timedelta(hours=1)
            window_end = peak_time + timedelta(hours=requirements['duration_hours'])
            
            optimal_windows.append({
                'start': window_start,
                'end': window_end,
                'confidence': 0.85,
                'reason': f"Aligns with your peak coherence time at {peak_time.strftime('%I:%M %p')}"
            })
        
        # Avoid trough times
        avoid_windows = []
        for trough_time in user_pattern.trough_times:
            avoid_start = trough_time - timedelta(hours=1)
            avoid_end = trough_time + timedelta(hours=2)
            
            avoid_windows.append({
                'start': avoid_start,
                'end': avoid_end,
                'reason': f"Your coherence typically drops around {trough_time.strftime('%I:%M %p')}"
            })
        
        return {
            'activity': activity_type,
            'optimal_windows': optimal_windows,
            'avoid_windows': avoid_windows,
            'general_advice': user_pattern.recommendations[0] if user_pattern.recommendations else None,
            'coherence_requirement': requirements['coherence_needed']
        }