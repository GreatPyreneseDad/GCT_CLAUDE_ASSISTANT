# Enhanced API Endpoints for GCT Extensions
# Integrates all new modules into the Flask backend

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import json

# Import enhancement modules
from temporal_coherence import TemporalCoherenceAnalyzer, CircadianType
from coherence_recovery import CoherenceRecoveryProtocol, RecoveryUrgency
from ai_coherence_interaction import AICoherenceAnalyzer, AIInteractionType
from cultural_calibration import CulturalCoherenceCalibrator, CulturalContext
from coherence_contagion import CoherenceContagionModel, GroupType
from coherence_development_prediction import CoherenceDevelopmentPredictor

# Import core components
from gct_backend import GCTDatabase, GCTAssessment
from gct_backend import logger

# Create blueprint for enhanced endpoints
enhanced_api = Blueprint('enhanced_api', __name__)

# Initialize enhancement modules
temporal_analyzer = TemporalCoherenceAnalyzer()
recovery_protocol = CoherenceRecoveryProtocol()
ai_analyzer = AICoherenceAnalyzer()
cultural_calibrator = CulturalCoherenceCalibrator()
contagion_model = CoherenceContagionModel()
development_predictor = CoherenceDevelopmentPredictor()

# ============================================================================
# TEMPORAL COHERENCE ENDPOINTS
# ============================================================================

@enhanced_api.route('/api/temporal/analyze', methods=['POST'])
def analyze_temporal_patterns():
    """Analyze temporal coherence patterns"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'user_id required'}), 400
        
        # Get user's assessment history
        db = GCTDatabase()
        assessment = GCTAssessment(db)
        
        # Get all assessments for temporal analysis
        # This would need to be implemented in the main backend
        # For now, using placeholder
        
        # Analyze circadian pattern
        circadian_type = CircadianType.VARIABLE  # Placeholder
        
        # Generate temporal insights
        temporal_pattern = temporal_analyzer.generate_temporal_insights(
            circadian_type,
            {},  # Weekly pattern placeholder
            []   # Transition impacts placeholder
        )
        
        return jsonify({
            'success': True,
            'temporal_analysis': {
                'circadian_type': circadian_type.value,
                'peak_times': [t.isoformat() for t in temporal_pattern.peak_times],
                'trough_times': [t.isoformat() for t in temporal_pattern.trough_times],
                'consistency_score': temporal_pattern.consistency_score,
                'recommendations': temporal_pattern.recommendations
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@enhanced_api.route('/api/temporal/optimal-timing', methods=['POST'])
def get_optimal_timing():
    """Get optimal timing for specific activities"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        activity_type = data.get('activity_type')
        
        if not user_id or not activity_type:
            return jsonify({'error': 'user_id and activity_type required'}), 400
        
        # Get user's temporal pattern (simplified)
        # In production, this would fetch from database
        user_pattern = temporal_analyzer.generate_temporal_insights(
            CircadianType.MORNING_PEAK,
            {},
            []
        )
        
        # Predict optimal timing
        optimal_timing = temporal_analyzer.predict_optimal_timing(
            user_pattern,
            activity_type,
            data.get('constraints', {})
        )
        
        return jsonify({
            'success': True,
            'optimal_timing': optimal_timing
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# COHERENCE RECOVERY ENDPOINTS
# ============================================================================

@enhanced_api.route('/api/recovery/generate-plan', methods=['POST'])
def generate_recovery_plan():
    """Generate personalized coherence recovery plan"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        available_time_daily = data.get('available_time_daily', 60)
        
        if not user_id:
            return jsonify({'error': 'user_id required'}), 400
        
        # Get user's latest profile
        db = GCTDatabase()
        assessment = GCTAssessment(db)
        profile = assessment.get_latest_assessment(user_id)
        
        if not profile:
            return jsonify({'error': 'No assessment found for user'}), 404
        
        # Generate recovery plan
        plan = recovery_protocol.generate_recovery_plan(
            profile,
            available_time_daily,
            data.get('constraints', {})
        )
        
        return jsonify({
            'success': True,
            'recovery_plan': {
                'urgency': plan.urgency.value,
                'current_state_analysis': plan.current_state_analysis,
                'immediate_interventions': [
                    {
                        'type': i.intervention_type,
                        'description': i.description,
                        'time_required': i.time_required_minutes,
                        'difficulty': i.difficulty_level
                    } for i in plan.immediate_interventions
                ],
                'daily_interventions': [
                    {
                        'type': i.intervention_type,
                        'description': i.description,
                        'time_required': i.time_required_minutes
                    } for i in plan.daily_interventions
                ],
                'expected_recovery_days': plan.expected_recovery_days,
                'warning_signs': plan.warning_signs
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# AI INTERACTION ANALYSIS ENDPOINTS
# ============================================================================

@enhanced_api.route('/api/ai-interaction/analyze', methods=['POST'])
def analyze_ai_interaction():
    """Analyze impact of AI interaction on coherence"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        conversation_text = data.get('conversation_text', '')
        duration_minutes = data.get('duration_minutes', 30)
        
        if not user_id or not conversation_text:
            return jsonify({'error': 'user_id and conversation_text required'}), 400
        
        # Classify interaction type
        interaction_type = ai_analyzer.classify_interaction(conversation_text)
        
        # Get user profile for impact analysis
        db = GCTDatabase()
        assessment = GCTAssessment(db)
        profile = assessment.get_latest_assessment(user_id)
        
        if profile:
            # Analyze impact
            from gct_backend import CommunicationAnalysis
            ai_response_analysis = CommunicationAnalysis(
                text="",
                consistency_score=0.7,
                wisdom_indicators=0.6,
                moral_activation=0.5,
                social_awareness=0.6,
                authenticity_score=0.65,
                red_flags=[],
                enhancement_suggestions=[],
                confidence_level=0.8
            )
            
            impact = ai_analyzer.analyze_interaction_impact(
                interaction_type,
                duration_minutes,
                ai_response_analysis,
                profile
            )
            
            return jsonify({
                'success': True,
                'ai_interaction_analysis': {
                    'interaction_type': interaction_type.value,
                    'predicted_impacts': impact,
                    'recommendations': [
                        "Monitor dependency indicators",
                        "Balance AI use with human interaction"
                    ]
                }
            })
        
        return jsonify({'error': 'User profile not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@enhanced_api.route('/api/ai-interaction/predict-trajectory', methods=['POST'])
def predict_ai_usage_impact():
    """Predict how planned AI usage will affect coherence"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        planned_usage = data.get('planned_usage', {})
        days_forward = data.get('days_forward', 30)
        
        if not user_id:
            return jsonify({'error': 'user_id required'}), 400
        
        # Get user profile
        db = GCTDatabase()
        assessment = GCTAssessment(db)
        profile = assessment.get_latest_assessment(user_id)
        
        if not profile:
            return jsonify({'error': 'No assessment found for user'}), 404
        
        # Convert planned usage to proper format
        usage_by_type = {}
        for usage_type, count in planned_usage.items():
            try:
                usage_by_type[AIInteractionType(usage_type)] = count
            except:
                pass
        
        # Predict trajectory
        prediction = ai_analyzer.predict_ai_coherence_trajectory(
            profile,
            usage_by_type,
            days_forward
        )
        
        return jsonify({
            'success': True,
            'ai_impact_prediction': prediction
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# CULTURAL CALIBRATION ENDPOINTS
# ============================================================================

@enhanced_api.route('/api/cultural/calibrate', methods=['POST'])
def calibrate_for_culture():
    """Calibrate coherence measurement for cultural context"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        cultural_context = data.get('cultural_context')
        
        if not user_id or not cultural_context:
            return jsonify({'error': 'user_id and cultural_context required'}), 400
        
        # Get user profile
        db = GCTDatabase()
        assessment = GCTAssessment(db)
        profile = assessment.get_latest_assessment(user_id)
        
        if not profile:
            return jsonify({'error': 'No assessment found for user'}), 404
        
        # Convert cultural context
        try:
            context = CulturalContext(cultural_context)
        except:
            return jsonify({'error': 'Invalid cultural context'}), 400
        
        # Calibrate profile
        calibrated_profile = cultural_calibrator.calibrate_coherence_measurement(
            profile,
            context,
            data.get('response_style', {})
        )
        
        # Generate cultural insights
        insights = cultural_calibrator.generate_cultural_insights(
            calibrated_profile,
            context
        )
        
        return jsonify({
            'success': True,
            'calibrated_profile': {
                'variables': {
                    'psi': calibrated_profile.variables.psi,
                    'rho': calibrated_profile.variables.rho,
                    'q': calibrated_profile.variables.q,
                    'f': calibrated_profile.variables.f
                },
                'static_coherence': calibrated_profile.static_coherence,
                'cultural_context': context.value,
                'insights': insights
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# COHERENCE CONTAGION ENDPOINTS
# ============================================================================

@enhanced_api.route('/api/contagion/analyze-group', methods=['POST'])
def analyze_group_coherence():
    """Analyze coherence contagion in a group"""
    try:
        data = request.get_json()
        member_ids = data.get('member_ids', [])
        group_type = data.get('group_type')
        
        if not member_ids or not group_type:
            return jsonify({'error': 'member_ids and group_type required'}), 400
        
        # Get member profiles
        db = GCTDatabase()
        assessment = GCTAssessment(db)
        
        member_profiles = []
        for member_id in member_ids:
            profile = assessment.get_latest_assessment(member_id)
            if profile:
                member_profiles.append(profile)
        
        if len(member_profiles) < 2:
            return jsonify({'error': 'Need at least 2 members with assessments'}), 400
        
        # Convert group type
        try:
            g_type = GroupType(group_type)
        except:
            return jsonify({'error': 'Invalid group type'}), 400
        
        # Calculate group coherence field
        group_state = contagion_model.calculate_group_coherence_field(
            member_profiles,
            g_type
        )
        
        # Identify catalysts
        catalysts = contagion_model.identify_coherence_catalysts(member_profiles)
        
        # Predict trajectory
        trajectory = contagion_model.predict_group_trajectory(
            group_state,
            data.get('interventions', []),
            data.get('time_horizon_days', 30)
        )
        
        return jsonify({
            'success': True,
            'group_analysis': {
                'average_coherence': group_state.average_coherence,
                'coherence_variance': group_state.coherence_variance,
                'field_strength': group_state.field_strength,
                'stability_score': group_state.stability_score,
                'top_catalysts': catalysts[:3],
                'trajectory': trajectory
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# DEVELOPMENT PREDICTION ENDPOINTS
# ============================================================================

@enhanced_api.route('/api/development/predict', methods=['POST'])
def predict_development():
    """Predict coherence development trajectory"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        time_horizon_weeks = data.get('time_horizon_weeks', 12)
        
        if not user_id:
            return jsonify({'error': 'user_id required'}), 400
        
        # Get user's assessment history
        db = GCTDatabase()
        assessment = GCTAssessment(db)
        current_profile = assessment.get_latest_assessment(user_id)
        
        if not current_profile:
            return jsonify({'error': 'No assessment found for user'}), 404
        
        # For demo, create minimal history
        history = [current_profile]
        
        # Predict trajectory
        trajectory = development_predictor.predict_development_trajectory(
            current_profile,
            history,
            data.get('life_context', {}),
            data.get('support_system', {}),
            time_horizon_weeks
        )
        
        # Generate personalized plan
        plan = development_predictor.generate_personalized_plan(
            trajectory,
            data.get('available_time_daily', 60),
            data.get('personality_type', 'balanced'),
            data.get('constraints', {})
        )
        
        return jsonify({
            'success': True,
            'development_prediction': {
                'baseline_coherence': trajectory.baseline_profile.static_coherence,
                'predicted_coherence_12_weeks': trajectory.predicted_profiles[-1].static_coherence if trajectory.predicted_profiles else None,
                'confidence_intervals': trajectory.confidence_intervals,
                'breakthrough_windows': [
                    {
                        'date': t.isoformat(),
                        'probability': p
                    } for t, p in trajectory.breakthrough_windows
                ],
                'expected_milestones': {
                    k: v.isoformat() for k, v in trajectory.expected_milestones.items()
                },
                'success_probability': plan.success_probability,
                'immediate_actions': [
                    {
                        'description': a.description,
                        'time_required': a.time_required_minutes
                    } for a in plan.immediate_actions
                ]
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# INTEGRATED INSIGHTS ENDPOINT
# ============================================================================

@enhanced_api.route('/api/integrated-insights/<user_id>', methods=['GET'])
def get_integrated_insights(user_id):
    """Get comprehensive insights combining all enhancement modules"""
    try:
        db = GCTDatabase()
        assessment = GCTAssessment(db)
        profile = assessment.get_latest_assessment(user_id)
        
        if not profile:
            return jsonify({'error': 'No assessment found for user'}), 404
        
        insights = {
            'current_coherence': profile.static_coherence,
            'coherence_level': 'high' if profile.static_coherence > 2.5 else 'moderate' if profile.static_coherence > 1.5 else 'developing',
            'enhancement_recommendations': []
        }
        
        # Add temporal insights
        if profile.static_coherence < 2.0:
            insights['enhancement_recommendations'].append({
                'module': 'temporal',
                'recommendation': 'Identify your peak coherence times for important decisions'
            })
        
        # Add recovery insights
        urgency = recovery_protocol.assess_recovery_urgency(profile)
        if urgency in [RecoveryUrgency.CRITICAL, RecoveryUrgency.HIGH]:
            insights['enhancement_recommendations'].append({
                'module': 'recovery',
                'recommendation': 'Implement immediate coherence recovery protocols'
            })
        
        # Add AI interaction insights
        insights['enhancement_recommendations'].append({
            'module': 'ai_interaction',
            'recommendation': 'Monitor AI usage patterns to maintain authentic coherence'
        })
        
        # Add cultural insights
        insights['enhancement_recommendations'].append({
            'module': 'cultural',
            'recommendation': 'Consider cultural context when interpreting coherence scores'
        })
        
        # Add development insights
        insights['enhancement_recommendations'].append({
            'module': 'development',
            'recommendation': 'Track progress weekly for optimal development trajectory'
        })
        
        return jsonify({
            'success': True,
            'integrated_insights': insights
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500