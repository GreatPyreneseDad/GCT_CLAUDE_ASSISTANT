"""
API endpoints for real-time text coherence analysis
Used by the browser extension for advanced LLM output evaluation
"""

from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import numpy as np
from typing import Dict, List, Any, Optional
import re
from datetime import datetime
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Import our existing analyzers
from llm_assessment_analyzer import LLMAssessmentAnalyzer
from narrative_feedback_generator import NarrativeFeedbackGenerator

text_coherence_bp = Blueprint('text_coherence', __name__)

class TextCoherenceAnalyzer:
    """Advanced text coherence analyzer using GCT principles"""
    
    def __init__(self):
        self.llm_analyzer = LLMAssessmentAnalyzer()
        self.executor = ThreadPoolExecutor(max_workers=4)
        
    def analyze_coherence(self, text: str, context: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze text coherence using multiple dimensions
        """
        # Basic metrics
        metrics = self._calculate_basic_metrics(text)
        
        # Advanced linguistic analysis
        linguistic = self._analyze_linguistic_features(text)
        
        # Contextual coherence if context provided
        if context:
            contextual = self._analyze_contextual_coherence(text, context)
            metrics['contextual_coherence'] = contextual
        
        # Calculate GCT dimensions
        gct_scores = self._calculate_gct_dimensions(text, linguistic)
        
        # Generate insights
        insights = self._generate_insights(gct_scores, linguistic)
        
        # Calculate overall coherence
        overall = self._calculate_overall_coherence(gct_scores)
        
        return {
            'metrics': {
                **gct_scores,
                'overall': overall,
                'confidence': metrics['confidence']
            },
            'linguistic': linguistic,
            'insights': insights,
            'meta': {
                'text_length': len(text),
                'word_count': metrics['word_count'],
                'avg_sentence_length': metrics['avg_sentence_length']
            }
        }
    
    def _calculate_basic_metrics(self, text: str) -> Dict[str, Any]:
        """Calculate basic text metrics"""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        words = text.split()
        word_count = len(words)
        
        return {
            'word_count': word_count,
            'sentence_count': len(sentences),
            'avg_sentence_length': word_count / max(len(sentences), 1),
            'confidence': min(1.0, word_count / 200)  # Confidence based on text length
        }
    
    def _analyze_linguistic_features(self, text: str) -> Dict[str, Any]:
        """Analyze linguistic features of the text"""
        # Logical connectors
        logical_connectors = [
            'therefore', 'thus', 'hence', 'consequently', 'as a result',
            'because', 'since', 'due to', 'owing to',
            'however', 'but', 'although', 'despite', 'nevertheless',
            'furthermore', 'moreover', 'additionally', 'also',
            'first', 'second', 'third', 'finally', 'in conclusion'
        ]
        
        # Hedging language (uncertainty)
        hedging_phrases = [
            'might', 'may', 'could', 'possibly', 'perhaps', 'probably',
            'it seems', 'appears to', 'tends to', 'generally', 'usually',
            'in some cases', 'sometimes', 'often'
        ]
        
        # Action-oriented language
        action_words = [
            'do', 'make', 'create', 'build', 'implement', 'execute',
            'try', 'attempt', 'consider', 'should', 'must', 'need to',
            'recommend', 'suggest', 'advise', 'propose'
        ]
        
        # Social/relational language
        social_words = [
            'people', 'person', 'community', 'together', 'collaborate',
            'share', 'help', 'support', 'understand', 'empathy',
            'relationship', 'connection', 'team', 'group'
        ]
        
        text_lower = text.lower()
        
        return {
            'logical_density': sum(1 for word in logical_connectors if word in text_lower) / max(len(text.split()), 1) * 100,
            'hedging_density': sum(1 for phrase in hedging_phrases if phrase in text_lower) / max(len(text.split()), 1) * 100,
            'action_density': sum(1 for word in action_words if word in text_lower) / max(len(text.split()), 1) * 100,
            'social_density': sum(1 for word in social_words if word in text_lower) / max(len(text.split()), 1) * 100,
            'has_examples': 'for example' in text_lower or 'for instance' in text_lower or 'e.g.' in text_lower,
            'has_structure': bool(re.search(r'(first|second|third|finally|\d+\.|\d+\))', text_lower)),
            'question_count': text.count('?'),
            'exclamation_count': text.count('!')
        }
    
    def _calculate_gct_dimensions(self, text: str, linguistic: Dict[str, Any]) -> Dict[str, float]:
        """Calculate GCT dimension scores from text and linguistic features"""
        
        # Ψ (Psi) - Internal Consistency
        # High logical density, low hedging, structural markers
        psi = 0.5  # Base score
        psi += min(0.3, linguistic['logical_density'] * 0.1)
        psi -= min(0.2, linguistic['hedging_density'] * 0.05)
        psi += 0.1 if linguistic['has_structure'] else 0
        psi = max(0, min(1, psi))
        
        # ρ (Rho) - Wisdom Integration
        # References to learning, examples, nuanced thinking
        rho = 0.4  # Base score
        learning_words = ['learn', 'understand', 'realize', 'discover', 'insight', 'experience']
        text_lower = text.lower()
        learning_count = sum(1 for word in learning_words if word in text_lower)
        rho += min(0.3, learning_count * 0.05)
        rho += 0.1 if linguistic['has_examples'] else 0
        rho += min(0.2, linguistic['hedging_density'] * 0.02)  # Some hedging shows nuance
        rho = max(0, min(1, rho))
        
        # q - Actionability/Practical Value
        # Action words, concrete suggestions, structured approach
        q = 0.4  # Base score
        q += min(0.4, linguistic['action_density'] * 0.1)
        q += 0.1 if linguistic['has_structure'] else 0
        q += 0.1 if linguistic['has_examples'] else 0
        q = max(0, min(1, q))
        
        # f - Social/Relational Awareness
        # Social language, consideration of others
        f = 0.4  # Base score
        f += min(0.4, linguistic['social_density'] * 0.1)
        f += 0.1 if 'we' in text_lower or 'us' in text_lower or 'our' in text_lower else 0
        f = max(0, min(1, f))
        
        return {
            'psi': psi,
            'rho': rho,
            'q': q,
            'f': f
        }
    
    def _analyze_contextual_coherence(self, text: str, context: str) -> float:
        """Analyze how well the text relates to its context"""
        # Extract key terms from context
        context_words = set(w.lower() for w in context.split() if len(w) > 3)
        text_words = set(w.lower() for w in text.split() if len(w) > 3)
        
        # Calculate overlap
        overlap = len(context_words.intersection(text_words))
        max_possible = min(len(context_words), len(text_words))
        
        if max_possible == 0:
            return 0.5
        
        return overlap / max_possible
    
    def _calculate_overall_coherence(self, gct_scores: Dict[str, float]) -> float:
        """Calculate overall coherence using GCT formula"""
        psi = gct_scores['psi']
        rho = gct_scores['rho']
        q = gct_scores['q']
        f = gct_scores['f']
        
        # GCT formula: C = ψ + (ρ × ψ) + q + (f × ψ)
        coherence = psi + (rho * psi) + q + (f * psi)
        
        # Normalize to 0-1 range
        return coherence / 4
    
    def _generate_insights(self, gct_scores: Dict[str, float], linguistic: Dict[str, Any]) -> Dict[str, List[str]]:
        """Generate insights based on analysis"""
        strengths = []
        concerns = []
        suggestions = []
        
        # Analyze GCT dimensions
        if gct_scores['psi'] > 0.7:
            strengths.append("Highly consistent and well-structured response")
        elif gct_scores['psi'] < 0.4:
            concerns.append("Response lacks internal consistency")
            suggestions.append("Use more logical connectors and clearer structure")
        
        if gct_scores['rho'] > 0.7:
            strengths.append("Shows deep understanding and wisdom")
        elif gct_scores['rho'] < 0.4:
            concerns.append("Limited depth or learning integration")
            suggestions.append("Include examples or reference past experiences")
        
        if gct_scores['q'] > 0.7:
            strengths.append("Highly actionable and practical")
        elif gct_scores['q'] < 0.4:
            concerns.append("Too abstract or theoretical")
            suggestions.append("Add concrete steps or specific recommendations")
        
        if gct_scores['f'] > 0.7:
            strengths.append("Strong social awareness and empathy")
        elif gct_scores['f'] < 0.4:
            concerns.append("Limited consideration of human factors")
            suggestions.append("Consider the human impact and relationships")
        
        # Analyze linguistic features
        if linguistic['logical_density'] > 5:
            strengths.append("Excellent use of logical connectors")
        
        if linguistic['hedging_density'] > 10:
            concerns.append("Excessive uncertainty or hedging")
        
        if linguistic['has_examples']:
            strengths.append("Good use of examples")
        
        return {
            'strengths': strengths,
            'concerns': concerns,
            'suggestions': suggestions
        }

# Create analyzer instance
analyzer = TextCoherenceAnalyzer()

@text_coherence_bp.route('/api/analyze/text', methods=['POST'])
@cross_origin()
def analyze_text():
    """Analyze text coherence"""
    try:
        data = request.json
        text = data.get('text', '')
        context = data.get('context')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Perform analysis
        result = analyzer.analyze_coherence(text, context)
        
        return jsonify({
            'success': True,
            'analysis': result,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@text_coherence_bp.route('/api/analyze/conversation', methods=['POST'])
@cross_origin()
def analyze_conversation():
    """Analyze an entire conversation for coherence trends"""
    try:
        data = request.json
        messages = data.get('messages', [])
        
        if not messages:
            return jsonify({'error': 'No messages provided'}), 400
        
        # Analyze each message
        analyses = []
        for i, message in enumerate(messages):
            context = messages[i-1]['text'] if i > 0 else None
            analysis = analyzer.analyze_coherence(message['text'], context)
            analyses.append({
                'index': i,
                'role': message.get('role', 'unknown'),
                'analysis': analysis
            })
        
        # Calculate conversation-level metrics
        llm_analyses = [a for a in analyses if a['role'] == 'assistant']
        if llm_analyses:
            avg_coherence = np.mean([a['analysis']['metrics']['overall'] for a in llm_analyses])
            coherence_trend = 'stable'
            
            if len(llm_analyses) > 2:
                first_half = np.mean([a['analysis']['metrics']['overall'] for a in llm_analyses[:len(llm_analyses)//2]])
                second_half = np.mean([a['analysis']['metrics']['overall'] for a in llm_analyses[len(llm_analyses)//2:]])
                
                if second_half > first_half + 0.1:
                    coherence_trend = 'improving'
                elif second_half < first_half - 0.1:
                    coherence_trend = 'declining'
        else:
            avg_coherence = 0
            coherence_trend = 'unknown'
        
        return jsonify({
            'success': True,
            'analyses': analyses,
            'conversation_metrics': {
                'average_coherence': avg_coherence,
                'trend': coherence_trend,
                'message_count': len(messages),
                'llm_message_count': len(llm_analyses)
            },
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@text_coherence_bp.route('/api/analyze/compare', methods=['POST'])
@cross_origin()
def compare_responses():
    """Compare coherence between multiple LLM responses"""
    try:
        data = request.json
        responses = data.get('responses', [])
        
        if len(responses) < 2:
            return jsonify({'error': 'At least 2 responses required for comparison'}), 400
        
        # Analyze each response
        analyses = []
        for response in responses:
            analysis = analyzer.analyze_coherence(
                response['text'], 
                response.get('context')
            )
            analyses.append({
                'llm': response.get('llm', 'Unknown'),
                'analysis': analysis
            })
        
        # Sort by overall coherence
        analyses.sort(key=lambda x: x['analysis']['metrics']['overall'], reverse=True)
        
        # Generate comparison insights
        comparison = {
            'rankings': [
                {
                    'rank': i + 1,
                    'llm': a['llm'],
                    'coherence': a['analysis']['metrics']['overall'],
                    'strengths': a['analysis']['insights']['strengths'][:2]
                }
                for i, a in enumerate(analyses)
            ],
            'dimension_comparison': {
                'psi': {a['llm']: a['analysis']['metrics']['psi'] for a in analyses},
                'rho': {a['llm']: a['analysis']['metrics']['rho'] for a in analyses},
                'q': {a['llm']: a['analysis']['metrics']['q'] for a in analyses},
                'f': {a['llm']: a['analysis']['metrics']['f'] for a in analyses}
            }
        }
        
        return jsonify({
            'success': True,
            'analyses': analyses,
            'comparison': comparison,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500