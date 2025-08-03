# GCT-Apple Intelligence Bridge
# Enables Apple Intelligence Chat to access GCT coherence analysis

import json
import requests
from typing import Dict, List, Optional
from datetime import datetime
import re

class GCTAppleIntelligenceBridge:
    """Bridge between Apple Intelligence Chat and GCT Assistant"""
    
    def __init__(self, gct_backend_url: str = "http://localhost:5001"):
        self.gct_backend_url = gct_backend_url
        self.context_patterns = {
            'coherence_check': r'(check|analyze|assess|measure).*(coherence|wellness|balance)',
            'communication_analysis': r'(analyze|review|check).*(communication|message|text)',
            'recovery_plan': r'(help|improve|boost|recover).*(coherence|wellness|balance)',
            'group_analysis': r'(group|team|family).*(coherence|dynamics|wellness)',
            'temporal_pattern': r'(pattern|trend|cycle).*(time|daily|weekly|monthly)'
        }
    
    def process_apple_intelligence_query(self, query: str, user_id: str) -> Dict[str, any]:
        """
        Process queries from Apple Intelligence Chat and route to appropriate GCT endpoints
        """
        query_lower = query.lower()
        
        # Detect intent
        intent = self._detect_intent(query_lower)
        
        # Route to appropriate handler
        if intent == 'coherence_check':
            return self._handle_coherence_check(user_id)
        elif intent == 'communication_analysis':
            return self._handle_communication_analysis(query, user_id)
        elif intent == 'recovery_plan':
            return self._handle_recovery_plan(user_id)
        elif intent == 'group_analysis':
            return self._handle_group_analysis(query, user_id)
        elif intent == 'temporal_pattern':
            return self._handle_temporal_pattern(user_id)
        else:
            return self._handle_general_query(query, user_id)
    
    def _detect_intent(self, query: str) -> Optional[str]:
        """Detect the intent of the query"""
        for intent, pattern in self.context_patterns.items():
            if re.search(pattern, query):
                return intent
        return None
    
    def _handle_coherence_check(self, user_id: str) -> Dict[str, any]:
        """Handle coherence check requests"""
        try:
            # Get latest coherence profile
            response = requests.get(
                f"{self.gct_backend_url}/api/profile/{user_id}"
            )
            
            if response.status_code == 200:
                data = response.json()
                profile = data.get('profile', {})
                
                return {
                    'success': True,
                    'type': 'coherence_check',
                    'response': self._format_coherence_response(profile),
                    'data': profile
                }
            else:
                return {
                    'success': False,
                    'response': "I don't have a coherence profile for you yet. Would you like to take a quick assessment?"
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'response': "I'm having trouble accessing your coherence data right now."
            }
    
    def _handle_communication_analysis(self, text: str, user_id: str) -> Dict[str, any]:
        """Handle communication analysis requests"""
        try:
            response = requests.post(
                f"{self.gct_backend_url}/api/communication/analyze",
                json={'text': text, 'user_id': user_id}
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'type': 'communication_analysis',
                    'response': self._format_communication_response(data),
                    'data': data
                }
            else:
                return {
                    'success': False,
                    'response': "I couldn't analyze the communication at this time."
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'response': "Communication analysis is temporarily unavailable."
            }
    
    def _handle_recovery_plan(self, user_id: str) -> Dict[str, any]:
        """Generate coherence recovery plan"""
        try:
            response = requests.post(
                f"{self.gct_backend_url}/api/enhanced/recovery/plan",
                json={'user_id': user_id}
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'type': 'recovery_plan',
                    'response': self._format_recovery_response(data),
                    'data': data
                }
            else:
                return {
                    'success': False,
                    'response': "I need your coherence profile first to create a personalized recovery plan."
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'response': "Recovery planning is temporarily unavailable."
            }
    
    def _handle_group_analysis(self, query: str, user_id: str) -> Dict[str, any]:
        """Handle group coherence analysis"""
        # Extract group members from query (simplified)
        return {
            'success': True,
            'type': 'group_analysis',
            'response': "To analyze group coherence, I'll need the profiles of all group members. You can share their user IDs or have them complete assessments.",
            'data': {'requires_group_data': True}
        }
    
    def _handle_temporal_pattern(self, user_id: str) -> Dict[str, any]:
        """Analyze temporal coherence patterns"""
        try:
            response = requests.post(
                f"{self.gct_backend_url}/api/enhanced/temporal/patterns",
                json={'user_id': user_id}
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'type': 'temporal_pattern',
                    'response': self._format_temporal_response(data),
                    'data': data
                }
            else:
                return {
                    'success': False,
                    'response': "I need more historical data to identify your coherence patterns."
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'response': "Pattern analysis is temporarily unavailable."
            }
    
    def _handle_general_query(self, query: str, user_id: str) -> Dict[str, any]:
        """Handle general queries about GCT"""
        return {
            'success': True,
            'type': 'general',
            'response': self._get_gct_explanation(),
            'data': {'query': query}
        }
    
    def _format_coherence_response(self, profile: Dict) -> str:
        """Format coherence profile into natural language"""
        if not profile:
            return "No coherence profile found."
        
        coherence = profile.get('static_coherence', 0)
        variables = profile.get('variables', {})
        
        # Determine coherence level
        if coherence < 1.5:
            level = "low"
            emoji = "🔴"
        elif coherence < 2.5:
            level = "moderate"
            emoji = "🟡"
        elif coherence < 3.5:
            level = "good"
            emoji = "🟢"
        else:
            level = "excellent"
            emoji = "⭐"
        
        response = f"{emoji} Your current coherence is {level} ({coherence:.2f}/4.0)\n\n"
        response += "Here's your breakdown:\n"
        response += f"• Internal Consistency (Ψ): {variables.get('psi', 0):.2f}\n"
        response += f"• Wisdom Integration (ρ): {variables.get('rho', 0):.2f}\n"
        response += f"• Moral Activation (q): {variables.get('q', 0):.2f}\n"
        response += f"• Social Belonging (f): {variables.get('f', 0):.2f}\n"
        
        # Add personalized insight
        lowest_var = min(variables.items(), key=lambda x: x[1])[0]
        var_names = {
            'psi': 'internal consistency',
            'rho': 'wisdom integration',
            'q': 'moral activation',
            'f': 'social belonging'
        }
        
        response += f"\n💡 Focus area: Improving your {var_names[lowest_var]} could boost your overall coherence."
        
        return response
    
    def _format_communication_response(self, analysis: Dict) -> str:
        """Format communication analysis into natural language"""
        coherence_estimate = analysis.get('coherence_estimate', {})
        markers = analysis.get('communication_markers', {})
        
        response = "📊 Communication Analysis:\n\n"
        
        # Overall coherence
        overall = coherence_estimate.get('overall', 0)
        if overall > 0.7:
            response += "✅ Your communication shows high coherence\n"
        elif overall > 0.5:
            response += "🟡 Your communication shows moderate coherence\n"
        else:
            response += "🔴 Your communication shows low coherence\n"
        
        # Key insights
        response += "\nKey patterns:\n"
        if markers.get('clarity_score', 0) > 0.7:
            response += "• Clear and well-structured expression\n"
        if markers.get('authenticity_markers', 0) > 0.6:
            response += "• Authentic and genuine communication\n"
        if markers.get('emotional_coherence', 0) > 0.7:
            response += "• Emotionally balanced expression\n"
        
        return response
    
    def _format_recovery_response(self, plan: Dict) -> str:
        """Format recovery plan into natural language"""
        immediate = plan.get('immediate_interventions', [])
        
        response = "🌟 Your Personalized Recovery Plan:\n\n"
        
        if immediate:
            response += "Start with these actions today:\n"
            for i, intervention in enumerate(immediate[:3], 1):
                response += f"{i}. {intervention['description']} ({intervention['time_required']} min)\n"
        
        response += "\n💪 Expected improvement: 15-20% coherence boost in 2 weeks"
        
        return response
    
    def _format_temporal_response(self, patterns: Dict) -> str:
        """Format temporal patterns into natural language"""
        circadian = patterns.get('circadian_type', 'unknown')
        weekly = patterns.get('weekly_patterns', [])
        
        response = f"🕐 Your Coherence Patterns:\n\n"
        response += f"You're a {circadian} type - "
        
        if circadian == 'morning_peak':
            response += "your coherence peaks in the morning hours\n"
        elif circadian == 'evening_peak':
            response += "you perform best in the evening\n"
        else:
            response += "you maintain steady coherence throughout the day\n"
        
        if weekly:
            response += f"\nBest days: {', '.join(weekly[:2])}"
        
        return response
    
    def _get_gct_explanation(self) -> str:
        """Provide a brief explanation of GCT"""
        return """
🧠 Grounded Coherence Theory (GCT) measures your overall wellbeing through four key dimensions:

1. **Internal Consistency (Ψ)** - How aligned your thoughts, feelings, and actions are
2. **Wisdom Integration (ρ)** - Your ability to learn from experience and apply insights
3. **Moral Activation (q)** - Your drive to act on your values and make a positive impact
4. **Social Belonging (f)** - The quality of your connections and sense of community

Together, these create your Coherence score (0-4), indicating your overall life balance and fulfillment.

Would you like to check your current coherence or get personalized recommendations?
"""

# API endpoint wrapper for Swift integration
class GCTAPIWrapper:
    """Wrapper to expose GCT functionality as REST API for Swift app"""
    
    def __init__(self, bridge: GCTAppleIntelligenceBridge):
        self.bridge = bridge
    
    def create_flask_endpoints(self, app):
        """Add GCT bridge endpoints to Flask app"""
        
        @app.route('/api/apple-intelligence/query', methods=['POST'])
        def apple_intelligence_query():
            try:
                data = request.json
                query = data.get('query', '')
                user_id = data.get('user_id', 'apple_user')
                
                result = self.bridge.process_apple_intelligence_query(query, user_id)
                
                return jsonify({
                    'success': result.get('success', False),
                    'response': result.get('response', ''),
                    'type': result.get('type', 'unknown'),
                    'data': result.get('data', {})
                })
                
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e),
                    'response': 'An error occurred processing your request.'
                }), 500
        
        @app.route('/api/apple-intelligence/system-prompt', methods=['GET'])
        def get_system_prompt():
            """Provide system prompt for Apple Intelligence to understand GCT"""
            prompt = """You are an AI assistant integrated with the Grounded Coherence Theory (GCT) system. 

When users ask about their coherence, wellness, balance, or personal development:
1. Use the GCT API to get their coherence data
2. Explain the four variables (Ψ, ρ, q, f) in simple terms
3. Provide actionable insights based on their profile
4. Suggest specific improvements for their lowest variables

When you detect coherence-related queries, respond with:
[GCT_QUERY: <intent>] where intent can be: coherence_check, recovery_plan, temporal_pattern, etc.

Always be supportive, encouraging, and focused on practical improvements."""
            
            return jsonify({
                'system_prompt': prompt,
                'intents': list(self.bridge.context_patterns.keys())
            })