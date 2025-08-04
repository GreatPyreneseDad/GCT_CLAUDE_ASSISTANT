#!/usr/bin/env python3
"""
Simple test endpoint to verify assessment completion works
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

@app.route('/api/test/assessment/complete', methods=['POST'])
def test_assessment_complete():
    """Simple test endpoint that returns mock assessment results"""
    data = request.json
    responses = data.get('responses', {})
    user_id = data.get('user_id', 'test_user')
    
    # Count responses per dimension
    dim_counts = {'psi': 0, 'rho': 0, 'q': 0, 'f': 0}
    dim_scores = {'psi': 0, 'rho': 0, 'q': 0, 'f': 0}
    
    for question_id, response_data in responses.items():
        dimension = question_id.split('_')[0]
        if dimension in dim_counts:
            dim_counts[dimension] += 1
            
            # Simple scoring based on response type
            answer = response_data.get('answer')
            if response_data.get('type') == 'scale':
                dim_scores[dimension] += float(answer) / 10.0
            elif response_data.get('type') == 'true_false':
                dim_scores[dimension] += 0.8 if answer else 0.3
            elif response_data.get('type') == 'choice':
                dim_scores[dimension] += [0.9, 0.7, 0.4, 0.2][int(answer)]
            else:  # story
                # Simple length-based scoring for stories
                dim_scores[dimension] += min(1.0, len(str(answer)) / 200)
    
    # Calculate average scores
    for dim in dim_scores:
        if dim_counts[dim] > 0:
            dim_scores[dim] /= dim_counts[dim]
        else:
            dim_scores[dim] = 0.5
    
    # Calculate static coherence
    static_coherence = (
        dim_scores['psi'] + 
        (dim_scores['rho'] * dim_scores['psi']) + 
        dim_scores['q'] + 
        (dim_scores['f'] * dim_scores['psi'])
    )
    
    # Determine coherence state
    if static_coherence > 3.0:
        state = "Thriving"
    elif static_coherence > 2.0:
        state = "Stable"
    elif static_coherence > 1.0:
        state = "Developing"
    else:
        state = "Struggling"
    
    # Generate mock insights
    insights = {
        'strengths': [],
        'growth_areas': [],
        'recommendations': [],
        'narrative_feedback': {
            'coherence_state': state,
            'overall_summary': f"Your assessment shows a {state.lower()} coherence profile with a score of {static_coherence:.2f}/4.0.",
            'trajectory_analysis': "Based on your responses, you show potential for growth in several areas.",
            'dimension_narratives': {
                'psi': f"Internal Consistency: {dim_scores['psi']:.1%} - Your values and actions show {'strong' if dim_scores['psi'] > 0.7 else 'moderate' if dim_scores['psi'] > 0.4 else 'developing'} alignment.",
                'rho': f"Wisdom Integration: {dim_scores['rho']:.1%} - You {'effectively' if dim_scores['rho'] > 0.7 else 'moderately' if dim_scores['rho'] > 0.4 else 'are learning to'} integrate lessons from experience.",
                'q': f"Moral Activation: {dim_scores['q']:.1%} - Your tendency to act on principles is {'strong' if dim_scores['q'] > 0.7 else 'developing' if dim_scores['q'] > 0.4 else 'emerging'}.",
                'f': f"Social Belonging: {dim_scores['f']:.1%} - Your connections are {'deep and meaningful' if dim_scores['f'] > 0.7 else 'present but could deepen' if dim_scores['f'] > 0.4 else 'an area for growth'}."
            },
            'key_themes': ['Personal growth', 'Value alignment', 'Relationship building'],
            'growth_opportunities': [
                f"Focus on strengthening {min(dim_scores.items(), key=lambda x: x[1])[0]}",
                "Develop daily practices for coherence",
                "Build deeper connections"
            ],
            'actionable_steps': [
                "Tonight: Reflect on your values for 10 minutes",
                "This week: Practice one act of moral courage",
                "This month: Deepen one important relationship"
            ],
            'probability_assessment': {
                'growth': 0.65 if static_coherence < 2.5 else 0.45,
                'stable': 0.25,
                'decline': 0.10 if static_coherence > 1.5 else 0.30
            }
        }
    }
    
    # Add strengths and growth areas
    for dim, score in dim_scores.items():
        dim_names = {'psi': 'Internal Consistency', 'rho': 'Wisdom Integration', 
                     'q': 'Moral Activation', 'f': 'Social Belonging'}
        if score > 0.7:
            insights['strengths'].append(f"Strong {dim_names[dim]} ({score:.0%})")
        elif score < 0.4:
            insights['growth_areas'].append(f"{dim_names[dim]} needs attention ({score:.0%})")
    
    if not insights['strengths']:
        insights['strengths'].append("Commitment to self-understanding")
    if not insights['growth_areas']:
        insights['growth_areas'].append("Continue deepening all dimensions")
    
    insights['recommendations'] = [
        "Practice daily reflection on values and actions",
        "Seek opportunities for meaningful connection",
        "Apply lessons from past experiences consciously"
    ]
    
    return jsonify({
        'success': True,
        'profile': {
            'user_id': user_id,
            'static_coherence': static_coherence,
            'variables': dim_scores,
            'coherence_level': state,
            'assessment_type': 'test_mock',
            'timestamp': '2025-08-03T21:45:00'
        },
        'insights': insights,
        'session_id': 'test_session_001'
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'test_endpoint'})

if __name__ == '__main__':
    app.run(port=5002, debug=True)