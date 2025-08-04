# Conversational Assessment Module
# Uses AI to analyze natural conversation and extract coherence scores

import re
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import numpy as np
from gct_types import CoherenceVariables, CoherenceProfile

class ConversationalAssessmentAnalyzer:
    """Analyzes conversational responses to extract coherence scores"""
    
    def __init__(self):
        # Keywords and patterns for each coherence dimension
        self.coherence_indicators = {
            'psi': {  # Internal Consistency
                'positive': [
                    'aligned', 'consistent', 'authentic', 'true to myself', 'integrity',
                    'values', 'principles', 'follow through', 'keep my word', 'reliable',
                    'match', 'congruent', 'unified', 'whole', 'integrated'
                ],
                'negative': [
                    'conflicted', 'torn', 'inconsistent', 'hypocritical', 'contradictory',
                    'confused', 'uncertain', 'wavering', 'divided', 'fragmented'
                ],
                'patterns': [
                    r'my actions (align|match|reflect) my values',
                    r'I (always|usually|often) do what I say',
                    r'true to (myself|my values|who I am)',
                    r'(struggle|hard) to be consistent'
                ]
            },
            'rho': {  # Wisdom Integration
                'positive': [
                    'learned', 'growth', 'wisdom', 'understanding', 'insight',
                    'experience taught', 'pattern', 'recognize', 'apply lessons',
                    'evolved', 'matured', 'developed', 'reflection', 'perspective'
                ],
                'negative': [
                    'repeat mistakes', 'never learn', 'same problems', 'stuck',
                    'no growth', 'stagnant', 'blind spots', 'ignore lessons'
                ],
                'patterns': [
                    r'learned (from|through) (that|this)',
                    r'experience (taught|showed) me',
                    r'I (now|have) understand',
                    r'(grew|growth) from (that|this)'
                ]
            },
            'q': {  # Moral Activation
                'positive': [
                    'act', 'action', 'stand up', 'intervene', 'help', 'contribute',
                    'make a difference', 'step up', 'take responsibility', 'initiative',
                    'volunteer', 'engage', 'participate', 'advocate', 'fight for'
                ],
                'negative': [
                    'passive', 'watch', 'ignore', 'avoid', 'hesitate', 'freeze',
                    'bystander', 'uninvolved', 'apathetic', 'indifferent'
                ],
                'patterns': [
                    r'I (take|took) action',
                    r'step(ped)? up (to|when)',
                    r'couldn\'t just (watch|stand by)',
                    r'felt compelled to (act|help|do something)'
                ]
            },
            'f': {  # Social Belonging
                'positive': [
                    'connected', 'belong', 'community', 'friends', 'family',
                    'support', 'close', 'bonds', 'relationships', 'together',
                    'understood', 'accepted', 'valued', 'loved', 'included'
                ],
                'negative': [
                    'lonely', 'isolated', 'disconnected', 'alone', 'excluded',
                    'misunderstood', 'rejected', 'outsider', 'distant', 'superficial'
                ],
                'patterns': [
                    r'feel (connected|close) to',
                    r'sense of (belonging|community)',
                    r'(strong|deep|meaningful) relationships',
                    r'(lonely|isolated|alone)'
                ]
            }
        }
        
        # Phase-specific prompts
        self.phase_prompts = {
            'psi': "Tell me about a recent decision you made - how did it feel in relation to your values?",
            'rho': "When you face challenges, how do you typically learn from them? Can you share a recent example?",
            'q': "When you see something that needs to be done, how do you decide whether to step up?",
            'f': "Tell me about your connections with others. How would you describe the quality of your relationships?"
        }
    
    def analyze_response(self, text: str, phase: str) -> Dict[str, float]:
        """
        Analyze a conversational response for coherence indicators
        Returns scores for the relevant dimension
        """
        text_lower = text.lower()
        
        # Get indicators for this phase
        indicators = self.coherence_indicators.get(phase, {})
        
        # Count positive and negative indicators
        positive_count = sum(1 for word in indicators.get('positive', []) if word in text_lower)
        negative_count = sum(1 for word in indicators.get('negative', []) if word in text_lower)
        
        # Check patterns
        pattern_matches = sum(1 for pattern in indicators.get('patterns', []) 
                            if re.search(pattern, text_lower))
        
        # Calculate base score
        base_score = 0.5  # Start neutral
        
        # Adjust based on indicators
        base_score += (positive_count * 0.05)
        base_score -= (negative_count * 0.05)
        base_score += (pattern_matches * 0.08)
        
        # Consider response length and complexity
        word_count = len(text.split())
        if word_count > 50:
            base_score += 0.05
        if word_count > 100:
            base_score += 0.05
        
        # Look for specific phrases that indicate high coherence
        high_coherence_phrases = {
            'psi': ['always true to', 'never compromise my values', 'complete alignment'],
            'rho': ['profound learning', 'transformed my perspective', 'deep wisdom'],
            'q': ['always take action', 'never hesitate to help', 'moral imperative'],
            'f': ['deeply connected', 'strong support system', 'meaningful relationships']
        }
        
        for phrase in high_coherence_phrases.get(phase, []):
            if phrase in text_lower:
                base_score += 0.1
        
        # Ensure score is between 0 and 1
        score = max(0.0, min(1.0, base_score))
        
        return {phase: score}
    
    def analyze_full_conversation(self, messages: List[Dict[str, str]]) -> CoherenceVariables:
        """
        Analyze a complete conversation to extract coherence scores
        """
        scores = {'psi': 0.5, 'rho': 0.5, 'q': 0.5, 'f': 0.5}
        
        # Analyze each message based on its phase
        for message in messages:
            if message.get('role') == 'user':
                phase = message.get('phase')
                if phase and phase in scores:
                    analysis = self.analyze_response(message['content'], phase)
                    scores[phase] = analysis.get(phase, 0.5)
        
        return CoherenceVariables(
            psi=scores['psi'],
            rho=scores['rho'],
            q=scores['q'],
            f=scores['f']
        )
    
    def generate_follow_up_question(self, response: str, phase: str, score: float) -> str:
        """
        Generate a contextual follow-up question based on the response
        """
        if score < 0.4:
            # Low score - explore challenges
            follow_ups = {
                'psi': "It sounds like you're experiencing some internal conflict. What makes it challenging to align your actions with your values?",
                'rho': "Learning from difficulties can be tough. What obstacles do you face when trying to apply past lessons?",
                'q': "Taking action isn't always easy. What holds you back when you want to make a difference?",
                'f': "Building connections can be challenging. What would help you feel more connected?"
            }
        elif score < 0.7:
            # Medium score - explore growth
            follow_ups = {
                'psi': "You show some alignment between values and actions. What helps you stay consistent, and where do you still struggle?",
                'rho': "You're learning from experiences. Can you share a specific lesson that changed how you approach similar situations?",
                'q': "You take action sometimes. What factors influence whether you step up or hold back?",
                'f': "You have some meaningful connections. What makes certain relationships deeper than others for you?"
            }
        else:
            # High score - explore depth
            follow_ups = {
                'psi': "Your strong alignment is impressive. How did you develop such consistency between your values and actions?",
                'rho': "You clearly integrate wisdom well. What's the most profound lesson that shapes your decisions today?",
                'q': "Your moral activation is strong. Can you share a time when taking action was difficult but you did it anyway?",
                'f': "Your connections sound meaningful. How do you nurture and maintain these deep relationships?"
            }
        
        return follow_ups.get(phase, "Tell me more about that.")
    
    def extract_insights(self, conversation: List[Dict[str, str]], scores: CoherenceVariables) -> Dict[str, any]:
        """
        Extract key insights from the conversation
        """
        insights = {
            'strengths': [],
            'growth_areas': [],
            'key_themes': [],
            'recommendations': []
        }
        
        # Identify strengths and growth areas
        variable_names = {
            'psi': 'Internal Consistency',
            'rho': 'Wisdom Integration',
            'q': 'Moral Activation',
            'f': 'Social Belonging'
        }
        
        for var, name in variable_names.items():
            value = getattr(scores, var)
            if value > 0.7:
                insights['strengths'].append(f"Strong {name} ({value:.0%})")
            elif value < 0.4:
                insights['growth_areas'].append(f"{name} needs attention ({value:.0%})")
        
        # Extract themes from conversation
        all_text = ' '.join([m['content'] for m in conversation if m.get('role') == 'user'])
        
        # Common themes to look for
        if 'family' in all_text.lower() or 'relationships' in all_text.lower():
            insights['key_themes'].append('Relationships are central to your coherence')
        if 'work' in all_text.lower() or 'career' in all_text.lower():
            insights['key_themes'].append('Professional life impacts your coherence')
        if 'growth' in all_text.lower() or 'learning' in all_text.lower():
            insights['key_themes'].append('Continuous learning is important to you')
        
        # Generate recommendations
        lowest_var = min(['psi', 'rho', 'q', 'f'], key=lambda v: getattr(scores, v))
        
        recommendations_map = {
            'psi': [
                "Practice daily values reflection",
                "Create a personal mission statement",
                "Track alignment between intentions and actions"
            ],
            'rho': [
                "Keep a learning journal",
                "Regularly review past experiences for patterns",
                "Seek mentorship or wisdom from others"
            ],
            'q': [
                "Set weekly action goals aligned with your values",
                "Look for small ways to make a difference daily",
                "Join causes that matter to you"
            ],
            'f': [
                "Schedule regular quality time with loved ones",
                "Join communities aligned with your interests",
                "Practice vulnerability in relationships"
            ]
        }
        
        insights['recommendations'] = recommendations_map.get(lowest_var, [])
        
        return insights