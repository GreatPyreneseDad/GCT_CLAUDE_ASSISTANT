# Enhanced API Endpoints for GCT Extensions
# Integrates all new modules into the Flask backend

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import json

# Import shared types
from gct_types import CoherenceProfile, CoherenceVariables, CommunicationAnalysis

# Import enhancement modules
from temporal_coherence import TemporalCoherenceAnalyzer, CircadianType
from coherence_recovery import CoherenceRecoveryProtocol, RecoveryUrgency
from ai_coherence_interaction import AICoherenceAnalyzer, AIInteractionType
from cultural_calibration import CulturalCoherenceCalibrator, CulturalContext
from coherence_contagion import CoherenceContagionModel, GroupType
from coherence_development_prediction import CoherenceDevelopmentPredictor
from conversational_assessment import ConversationalAssessmentAnalyzer
from comprehensive_assessment import ComprehensiveAssessmentFramework, QuestionType
from llm_assessment_analyzer import LLMAssessmentAnalyzer, ResponseAnalysis, DimensionAnalysis

# Import core components (avoiding circular import)
from gct_backend import GCTDatabase, GCTAssessment
import sqlite3
import asyncio

# Create blueprint for enhanced endpoints
enhanced_api = Blueprint('enhanced_api', __name__)

# Initialize enhancement modules
temporal_analyzer = TemporalCoherenceAnalyzer()
recovery_protocol = CoherenceRecoveryProtocol()
ai_analyzer = AICoherenceAnalyzer()
cultural_calibrator = CulturalCoherenceCalibrator()
contagion_model = CoherenceContagionModel()
development_predictor = CoherenceDevelopmentPredictor()
conversational_analyzer = ConversationalAssessmentAnalyzer()
comprehensive_framework = ComprehensiveAssessmentFramework()
llm_analyzer = LLMAssessmentAnalyzer()

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

# ============================================================================
# CONVERSATIONAL ASSESSMENT ENDPOINTS
# ============================================================================

@enhanced_api.route('/conversational/analyze', methods=['POST'])
def analyze_conversational_response():
    """Analyze a conversational assessment response"""
    try:
        data = request.json
        text = data.get('text', '')
        phase = data.get('phase', 'psi')
        user_id = data.get('user_id', 'anonymous')
        
        # Analyze the response
        score = conversational_analyzer.analyze_response(text, phase)
        
        # Generate contextual follow-up
        follow_up = conversational_analyzer.generate_follow_up_question(
            text, phase, score.get(phase, 0.5)
        )
        
        return jsonify({
            'success': True,
            'score': score,
            'follow_up': follow_up,
            'phase': phase
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@enhanced_api.route('/conversational/complete', methods=['POST'])
def complete_conversational_assessment():
    """Complete a full conversational assessment"""
    try:
        data = request.json
        messages = data.get('messages', [])
        user_id = data.get('user_id', 'anonymous')
        
        # Analyze full conversation
        coherence_vars = conversational_analyzer.analyze_full_conversation(messages)
        
        # Calculate overall coherence
        static_coherence = (
            coherence_vars.psi + 
            (coherence_vars.rho * coherence_vars.psi) + 
            coherence_vars.q + 
            (coherence_vars.f * coherence_vars.psi)
        )
        
        # Extract insights
        insights = conversational_analyzer.extract_insights(messages, coherence_vars)
        
        # Create profile
        profile = CoherenceProfile(
            user_id=user_id,
            variables=coherence_vars,
            static_coherence=static_coherence,
            coherence_velocity=0.0,
            assessment_tier='conversational',
            timestamp=datetime.now()
        )
        
        # Store in database (would need to implement this)
        # database.store_profile(profile)
        
        return jsonify({
            'success': True,
            'profile': {
                'user_id': user_id,
                'static_coherence': static_coherence,
                'variables': {
                    'psi': coherence_vars.psi,
                    'rho': coherence_vars.rho,
                    'q': coherence_vars.q,
                    'f': coherence_vars.f
                },
                'assessment_type': 'conversational',
                'timestamp': datetime.now().isoformat()
            },
            'insights': insights
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# LLM-BASED ASSESSMENT ENDPOINTS  
# ============================================================================

@enhanced_api.route('/assessment/complete/llm', methods=['POST'])
async def complete_llm_assessment():
    """Complete assessment with LLM-based dynamic analysis"""
    try:
        data = request.json
        responses = data.get('responses', {})
        user_id = data.get('user_id', 'llm_user')
        
        # Create database session
        db_path = 'gct_data.db'
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create assessment session
        cursor.execute("""
            INSERT INTO assessment_sessions 
            (user_id, session_type, total_questions, questions_answered, ai_model_used)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, 'comprehensive_llm', 30, len(responses), 'available'))
        
        session_id = cursor.lastrowid
        
        # Store each response
        organized_responses = {'psi': [], 'rho': [], 'q': [], 'f': []}
        
        for question_id, response_data in responses.items():
            # Determine dimension from question_id
            dimension = question_id.split('_')[0]
            
            # Store response in database
            cursor.execute("""
                INSERT INTO assessment_responses
                (session_id, question_id, dimension, question_text, question_type, 
                 response_text, response_value)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (session_id, question_id, dimension, 
                  response_data.get('question', ''),
                  response_data.get('type', 'unknown'),
                  str(response_data.get('answer', '')),
                  float(response_data.get('answer', 0)) if isinstance(response_data.get('answer'), (int, float)) else None))
            
            response_id = cursor.lastrowid
            
            # Organize for LLM analysis
            organized_responses[dimension].append({
                'question_id': question_id,
                'question': response_data.get('question', ''),
                'answer': response_data.get('answer', ''),
                'type': response_data.get('type', 'story'),
                'response_id': response_id
            })
        
        conn.commit()
        
        # Run LLM analysis
        try:
            # Analyze responses with LLM
            profile, insights = await llm_analyzer.generate_comprehensive_profile(organized_responses)
            
            # Store analyses in database
            for dimension, responses_list in organized_responses.items():
                if responses_list:
                    dim_analysis = await llm_analyzer.analyze_dimension_responses(
                        responses_list, dimension
                    )
                    
                    # Store dimension summary
                    cursor.execute("""
                        INSERT INTO dimension_summaries
                        (session_id, dimension, overall_score, pattern_summary, 
                         growth_summary, concern_summary)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (session_id, dimension, dim_analysis.overall_score,
                          ', '.join(dim_analysis.patterns[:3]),
                          ', '.join(dim_analysis.growth_indicators[:3]),
                          ', '.join(dim_analysis.concern_areas[:3])))
                    
                    # Store individual response analyses
                    for resp, analysis in zip(responses_list, dim_analysis.response_analyses):
                        cursor.execute("""
                            INSERT INTO response_analyses
                            (response_id, dimension, overall_score, confidence, 
                             authenticity_score, emotional_tone, analysis_text)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (resp['response_id'], dimension, analysis.raw_score,
                              analysis.confidence, analysis.authenticity_score,
                              analysis.emotional_tone, 
                              f"Key indicators: {', '.join(analysis.key_indicators[:3])}"))
                        
                        analysis_id = cursor.lastrowid
                        
                        # Store sub-dimension scores
                        for sub_dim, score in analysis.sub_dimensions.items():
                            cursor.execute("""
                                INSERT INTO subdimension_scores
                                (analysis_id, subdimension_name, score)
                                VALUES (?, ?, ?)
                            """, (analysis_id, sub_dim, score))
            
            # Store final profile
            cursor.execute("""
                INSERT INTO coherence_profiles_detailed
                (user_id, session_id, psi_score, rho_score, q_score, f_score,
                 static_coherence, coherence_level, assessment_quality)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (user_id, session_id, profile.variables.psi, profile.variables.rho,
                  profile.variables.q, profile.variables.f, profile.static_coherence,
                  insights['overall_coherence_level'], 0.9))
            
            profile_id = cursor.lastrowid
            
            # Store insights
            for strength in insights['strengths']:
                cursor.execute("""
                    INSERT INTO assessment_insights
                    (profile_id, insight_type, insight_text, priority)
                    VALUES (?, ?, ?, ?)
                """, (profile_id, 'strength', strength, 1))
            
            for growth in insights['growth_areas']:
                cursor.execute("""
                    INSERT INTO assessment_insights
                    (profile_id, insight_type, insight_text, priority)
                    VALUES (?, ?, ?, ?)
                """, (profile_id, 'growth_area', growth, 2))
            
            for i, rec in enumerate(insights['recommendations']):
                cursor.execute("""
                    INSERT INTO assessment_insights
                    (profile_id, insight_type, insight_text, priority)
                    VALUES (?, ?, ?, ?)
                """, (profile_id, 'recommendation', rec, 3 + i))
            
            # Mark session as completed
            cursor.execute("""
                UPDATE assessment_sessions
                SET status = 'completed', completed_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (session_id,))
            
            conn.commit()
            conn.close()
            
            return jsonify({
                'success': True,
                'profile': {
                    'user_id': user_id,
                    'static_coherence': profile.static_coherence,
                    'variables': {
                        'psi': profile.variables.psi,
                        'rho': profile.variables.rho,
                        'q': profile.variables.q,
                        'f': profile.variables.f
                    },
                    'coherence_level': insights['overall_coherence_level'],
                    'assessment_type': 'llm_comprehensive',
                    'timestamp': datetime.now().isoformat()
                },
                'insights': insights,
                'session_id': session_id
            })
            
        except Exception as ai_error:
            # Fallback to basic analysis
            conn.close()
            return jsonify({
                'success': False,
                'error': f'AI analysis failed: {str(ai_error)}',
                'fallback': True
            }), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# COMPREHENSIVE ASSESSMENT ENDPOINTS
# ============================================================================

@enhanced_api.route('/assessment/complete', methods=['POST'])
def complete_comprehensive_assessment():
    """Complete a comprehensive multi-layered assessment"""
    try:
        data = request.json
        responses = data.get('responses', {})
        user_id = data.get('user_id', 'comprehensive_user')
        
        # Calculate scores for each dimension
        dimension_scores = {}
        dimension_insights = {}
        
        for dimension in ['psi', 'rho', 'q', 'f']:
            score = comprehensive_framework.calculate_dimension_score(
                dimension, 
                responses
            )
            dimension_scores[dimension] = score
            
            # Get subdimension analysis
            sub_dimensions = getattr(
                comprehensive_framework, 
                f'_get_{dimension}_subdimensions'
            )()
            dimension_insights[dimension] = {
                'score': score,
                'sub_dimensions': sub_dimensions
            }
        
        # Create coherence variables
        coherence_vars = CoherenceVariables(
            psi=dimension_scores['psi'],
            rho=dimension_scores['rho'],
            q=dimension_scores['q'],
            f=dimension_scores['f']
        )
        
        # Calculate overall coherence
        static_coherence = (
            coherence_vars.psi + 
            (coherence_vars.rho * coherence_vars.psi) + 
            coherence_vars.q + 
            (coherence_vars.f * coherence_vars.psi)
        )
        
        # Create profile
        profile = CoherenceProfile(
            user_id=user_id,
            variables=coherence_vars,
            static_coherence=static_coherence,
            coherence_velocity=0.0,
            assessment_tier='comprehensive',
            timestamp=datetime.now()
        )
        
        # Store in database
        db = GCTDatabase()
        assessment = GCTAssessment(db)
        assessment.save_assessment(profile)
        
        # Generate comprehensive insights
        insights = {
            'strengths': [],
            'growth_areas': [],
            'recommendations': []
        }
        
        # Analyze each dimension
        for dimension, score in dimension_scores.items():
            dim_name = {
                'psi': 'Internal Consistency',
                'rho': 'Wisdom Integration',
                'q': 'Moral Activation',
                'f': 'Social Belonging'
            }[dimension]
            
            if score > 0.7:
                insights['strengths'].append(f"Strong {dim_name} ({score:.0%})")
            elif score < 0.4:
                insights['growth_areas'].append(f"{dim_name} needs attention ({score:.0%})")
        
        # Add top recommendations
        lowest_dim = min(dimension_scores.items(), key=lambda x: x[1])
        recommendation_map = {
            'psi': "Focus on aligning your daily actions with your core values",
            'rho': "Develop a practice of reflection to extract wisdom from experiences",
            'q': "Look for small opportunities to take meaningful action each day",
            'f': "Invest time in deepening your most important relationships"
        }
        insights['recommendations'].append(recommendation_map[lowest_dim[0]])
        
        return jsonify({
            'success': True,
            'profile': {
                'user_id': user_id,
                'static_coherence': static_coherence,
                'variables': {
                    'psi': coherence_vars.psi,
                    'rho': coherence_vars.rho,
                    'q': coherence_vars.q,
                    'f': coherence_vars.f
                },
                'assessment_type': 'comprehensive',
                'timestamp': datetime.now().isoformat()
            },
            'insights': insights,
            'dimension_analysis': dimension_insights
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500