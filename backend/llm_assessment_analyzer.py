# LLM-Based Assessment Analyzer
# Uses AI to dynamically analyze interview responses and create gradient scoring

import os
import json
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import openai
from anthropic import Anthropic
import numpy as np
from gct_types import CoherenceVariables, CoherenceProfile
from narrative_feedback_generator import NarrativeFeedbackGenerator, NarrativeFeedback

@dataclass
class ResponseAnalysis:
    """Analysis of a single response"""
    dimension: str
    raw_score: float  # 0-1 gradient
    confidence: float  # How confident the AI is in this score
    key_indicators: List[str]  # What the AI identified
    sub_dimensions: Dict[str, float]  # Breakdown by sub-dimensions
    emotional_tone: str  # Detected emotional state
    authenticity_score: float  # How genuine the response seems

@dataclass
class DimensionAnalysis:
    """Complete analysis for one coherence dimension"""
    dimension: str
    overall_score: float
    sub_scores: Dict[str, float]
    response_analyses: List[ResponseAnalysis]
    patterns: List[str]
    growth_indicators: List[str]
    concern_areas: List[str]

class LLMAssessmentAnalyzer:
    """Uses LLM to analyze assessment responses with nuanced gradient scoring"""
    
    def __init__(self):
        # Initialize AI clients
        self.openai_client = None
        self.anthropic_client = None
        
        # Try to initialize available AI services
        if os.getenv('OPENAI_API_KEY'):
            openai.api_key = os.getenv('OPENAI_API_KEY')
            self.openai_client = openai
        
        if os.getenv('ANTHROPIC_API_KEY'):
            self.anthropic_client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        
        # Initialize narrative feedback generator
        self.narrative_generator = NarrativeFeedbackGenerator()
        
        # Dimension definitions for AI context
        self.dimension_context = {
            'psi': {
                'name': 'Internal Consistency',
                'description': 'How well actions align with stated values and beliefs',
                'sub_dimensions': {
                    'value_action_alignment': 'Actions matching stated values',
                    'emotional_congruence': 'Emotions aligning with beliefs',
                    'behavioral_consistency': 'Consistent behavior across contexts',
                    'identity_integration': 'Unified sense of self'
                }
            },
            'rho': {
                'name': 'Wisdom Integration',
                'description': 'Ability to learn from experiences and apply wisdom',
                'sub_dimensions': {
                    'pattern_recognition': 'Seeing patterns in experiences',
                    'learning_application': 'Applying lessons learned',
                    'perspective_taking': 'Understanding multiple viewpoints',
                    'growth_mindset': 'Openness to learning and change'
                }
            },
            'q': {
                'name': 'Moral Activation',
                'description': 'Tendency to act on moral principles',
                'sub_dimensions': {
                    'moral_sensitivity': 'Recognizing moral situations',
                    'action_initiation': 'Taking the first step',
                    'perseverance': 'Following through despite obstacles',
                    'impact_awareness': 'Understanding consequences'
                }
            },
            'f': {
                'name': 'Social Belonging',
                'description': 'Quality of connections and relationships',
                'sub_dimensions': {
                    'relationship_depth': 'Quality of close relationships',
                    'community_connection': 'Sense of belonging to groups',
                    'social_contribution': 'Giving to others/community',
                    'authentic_relating': 'Being genuine in relationships'
                }
            }
        }
    
    async def analyze_response(self, 
                             response_text: str, 
                             question_text: str,
                             dimension: str,
                             response_type: str) -> ResponseAnalysis:
        """Analyze a single response using LLM"""
        
        # Build the analysis prompt
        prompt = self._build_analysis_prompt(
            response_text, question_text, dimension, response_type
        )
        
        # Get AI analysis
        analysis = await self._get_ai_analysis(prompt)
        
        # Parse the analysis into structured format
        return self._parse_response_analysis(analysis, dimension)
    
    def _build_analysis_prompt(self, response: str, question: str, 
                              dimension: str, response_type: str) -> str:
        """Build a detailed prompt for AI analysis"""
        
        dim_info = self.dimension_context[dimension]
        
        prompt = f"""You are an expert psychologist analyzing responses in a coherence assessment.

DIMENSION: {dim_info['name']} ({dimension})
DESCRIPTION: {dim_info['description']}

SUB-DIMENSIONS to consider:
{json.dumps(dim_info['sub_dimensions'], indent=2)}

QUESTION: {question}
RESPONSE TYPE: {response_type}
USER'S RESPONSE: {response}

Please analyze this response and provide:

1. OVERALL SCORE (0.0-1.0): A nuanced gradient score for this dimension
2. SUB-DIMENSION SCORES: Score each sub-dimension (0.0-1.0)
3. CONFIDENCE (0.0-1.0): How confident you are in this assessment
4. KEY INDICATORS: Specific phrases or patterns that influenced your scoring
5. EMOTIONAL TONE: The emotional state detected (e.g., confident, uncertain, defensive, open)
6. AUTHENTICITY (0.0-1.0): How genuine/authentic the response seems
7. ANALYSIS: Brief explanation of your scoring rationale

For {response_type} responses:
- For 'story': Look for depth, self-reflection, growth patterns
- For 'scale': Consider if the rating aligns with their explanations
- For 'true_false': Look for consistency with other responses
- For 'choice': Analyze the reasoning behind their selection

Output as JSON with these exact keys:
{{
    "overall_score": 0.0-1.0,
    "sub_scores": {{"sub_dim_name": score, ...}},
    "confidence": 0.0-1.0,
    "key_indicators": ["indicator1", "indicator2", ...],
    "emotional_tone": "tone",
    "authenticity": 0.0-1.0,
    "analysis": "explanation"
}}"""
        
        return prompt
    
    async def _get_ai_analysis(self, prompt: str) -> Dict[str, Any]:
        """Get analysis from available AI service"""
        
        # Try Anthropic first (Claude)
        if self.anthropic_client:
            try:
                response = self.anthropic_client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=1000,
                    temperature=0.3,
                    messages=[{"role": "user", "content": prompt}]
                )
                # Extract JSON from response
                json_str = response.content[0].text
                return json.loads(json_str)
            except Exception as e:
                print(f"Anthropic API error: {e}")
        
        # Fall back to OpenAI
        if self.openai_client:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are an expert psychological assessor. Always respond with valid JSON."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=1000
                )
                return json.loads(response.choices[0].message.content)
            except Exception as e:
                print(f"OpenAI API error: {e}")
        
        # Fallback to local analysis if no AI available
        return self._fallback_analysis()
    
    def _fallback_analysis(self) -> Dict[str, Any]:
        """Basic analysis when AI is not available"""
        return {
            "overall_score": 0.5,
            "sub_scores": {k: 0.5 for k in ["alignment", "congruence", "consistency", "integration"]},
            "confidence": 0.3,
            "key_indicators": ["Unable to perform AI analysis"],
            "emotional_tone": "neutral",
            "authenticity": 0.5,
            "analysis": "AI analysis unavailable, using baseline scoring"
        }
    
    def _parse_response_analysis(self, analysis: Dict[str, Any], 
                                dimension: str) -> ResponseAnalysis:
        """Parse AI analysis into ResponseAnalysis object"""
        
        return ResponseAnalysis(
            dimension=dimension,
            raw_score=float(analysis.get('overall_score', 0.5)),
            confidence=float(analysis.get('confidence', 0.5)),
            key_indicators=analysis.get('key_indicators', []),
            sub_dimensions=analysis.get('sub_scores', {}),
            emotional_tone=analysis.get('emotional_tone', 'neutral'),
            authenticity_score=float(analysis.get('authenticity', 0.5))
        )
    
    async def analyze_dimension_responses(self, 
                                        responses: List[Dict[str, Any]], 
                                        dimension: str) -> DimensionAnalysis:
        """Analyze all responses for a dimension"""
        
        response_analyses = []
        
        # Analyze each response
        for resp in responses:
            analysis = await self.analyze_response(
                resp['answer'],
                resp['question'],
                dimension,
                resp.get('type', 'story')
            )
            response_analyses.append(analysis)
        
        # Calculate overall dimension score using weighted average
        weights = [a.confidence * a.authenticity_score for a in response_analyses]
        scores = [a.raw_score for a in response_analyses]
        
        if sum(weights) > 0:
            overall_score = np.average(scores, weights=weights)
        else:
            overall_score = np.mean(scores)
        
        # Aggregate sub-dimension scores
        sub_scores = {}
        for sub_dim in self.dimension_context[dimension]['sub_dimensions']:
            sub_dim_scores = [
                a.sub_dimensions.get(sub_dim, 0.5) 
                for a in response_analyses 
                if sub_dim in a.sub_dimensions
            ]
            if sub_dim_scores:
                sub_scores[sub_dim] = np.mean(sub_dim_scores)
            else:
                sub_scores[sub_dim] = 0.5
        
        # Identify patterns and areas
        patterns = self._identify_patterns(response_analyses)
        growth_indicators = self._identify_growth_indicators(response_analyses)
        concern_areas = self._identify_concerns(response_analyses)
        
        return DimensionAnalysis(
            dimension=dimension,
            overall_score=float(overall_score),
            sub_scores=sub_scores,
            response_analyses=response_analyses,
            patterns=patterns,
            growth_indicators=growth_indicators,
            concern_areas=concern_areas
        )
    
    def _identify_patterns(self, analyses: List[ResponseAnalysis]) -> List[str]:
        """Identify patterns across responses"""
        patterns = []
        
        # Check for consistency
        scores = [a.raw_score for a in analyses]
        if np.std(scores) < 0.1:
            patterns.append("Highly consistent responses across questions")
        elif np.std(scores) > 0.3:
            patterns.append("Significant variation in response quality")
        
        # Check emotional tones
        tones = [a.emotional_tone for a in analyses]
        dominant_tone = max(set(tones), key=tones.count)
        patterns.append(f"Predominantly {dominant_tone} emotional tone")
        
        # Check authenticity
        auth_scores = [a.authenticity_score for a in analyses]
        if np.mean(auth_scores) > 0.8:
            patterns.append("High authenticity and openness throughout")
        elif np.mean(auth_scores) < 0.5:
            patterns.append("Guarded or rehearsed responses detected")
        
        return patterns
    
    def _identify_growth_indicators(self, analyses: List[ResponseAnalysis]) -> List[str]:
        """Identify positive growth indicators"""
        indicators = []
        
        for analysis in analyses:
            for indicator in analysis.key_indicators:
                if any(word in indicator.lower() for word in 
                      ['growth', 'learned', 'improved', 'developed', 'realized']):
                    indicators.append(indicator)
        
        return list(set(indicators))[:5]  # Top 5 unique indicators
    
    def _identify_concerns(self, analyses: List[ResponseAnalysis]) -> List[str]:
        """Identify areas of concern"""
        concerns = []
        
        # Low scores
        low_score_areas = [
            f"Low {a.dimension} score in response" 
            for a in analyses 
            if a.raw_score < 0.4
        ]
        concerns.extend(low_score_areas[:3])
        
        # Low confidence responses
        if any(a.confidence < 0.5 for a in analyses):
            concerns.append("Some responses showed uncertainty or confusion")
        
        # Low authenticity
        if any(a.authenticity_score < 0.5 for a in analyses):
            concerns.append("Some responses may not fully reflect genuine experience")
        
        return concerns
    
    async def generate_comprehensive_profile(self, 
                                           all_responses: Dict[str, List[Dict[str, Any]]]) -> Tuple[CoherenceProfile, Dict[str, Any]]:
        """Generate complete coherence profile from all responses"""
        
        dimension_analyses = {}
        
        # Analyze each dimension
        for dimension in ['psi', 'rho', 'q', 'f']:
            if dimension in all_responses:
                analysis = await self.analyze_dimension_responses(
                    all_responses[dimension], 
                    dimension
                )
                dimension_analyses[dimension] = analysis
        
        # Create coherence variables with gradient scores
        variables = CoherenceVariables(
            psi=dimension_analyses.get('psi', DimensionAnalysis('psi', 0.5, {}, [], [], [], [])).overall_score,
            rho=dimension_analyses.get('rho', DimensionAnalysis('rho', 0.5, {}, [], [], [], [])).overall_score,
            q=dimension_analyses.get('q', DimensionAnalysis('q', 0.5, {}, [], [], [], [])).overall_score,
            f=dimension_analyses.get('f', DimensionAnalysis('f', 0.5, {}, [], [], [], [])).overall_score
        )
        
        # Calculate static coherence
        static_coherence = (
            variables.psi + 
            (variables.rho * variables.psi) + 
            variables.q + 
            (variables.f * variables.psi)
        )
        
        # Create profile
        profile = CoherenceProfile(
            user_id='llm_assessment_user',
            variables=variables,
            static_coherence=static_coherence,
            coherence_velocity=0.0,
            assessment_tier='comprehensive_llm',
            timestamp=datetime.now()
        )
        
        # Generate insights
        insights = self._generate_insights(dimension_analyses, variables)
        
        # Generate comprehensive narrative feedback
        narrative_feedback = self.narrative_generator.generate_comprehensive_feedback(
            profile=profile,
            analysis_details=insights,
            response_content=all_responses,
            historical_profiles=None  # Would fetch from DB in production
        )
        
        # Add narrative to insights
        insights['narrative_feedback'] = {
            'overall_summary': narrative_feedback.overall_summary,
            'coherence_state': narrative_feedback.coherence_state,
            'trajectory_analysis': narrative_feedback.trajectory_analysis,
            'dimension_narratives': narrative_feedback.dimension_narratives,
            'key_themes': narrative_feedback.key_themes,
            'growth_opportunities': narrative_feedback.growth_opportunities,
            'actionable_steps': narrative_feedback.actionable_steps,
            'probability_assessment': narrative_feedback.probability_assessment
        }
        
        return profile, insights
    
    def _generate_insights(self, analyses: Dict[str, DimensionAnalysis], 
                          variables: CoherenceVariables) -> Dict[str, Any]:
        """Generate comprehensive insights from analyses"""
        
        insights = {
            'overall_coherence_level': self._get_coherence_level(variables),
            'strengths': [],
            'growth_areas': [],
            'key_patterns': [],
            'recommendations': [],
            'dimension_details': {}
        }
        
        # Compile insights from each dimension
        for dim, analysis in analyses.items():
            dim_name = self.dimension_context[dim]['name']
            
            # Add to strengths or growth areas
            if analysis.overall_score > 0.7:
                insights['strengths'].append(
                    f"Strong {dim_name} ({analysis.overall_score:.1%})"
                )
            elif analysis.overall_score < 0.4:
                insights['growth_areas'].append(
                    f"{dim_name} needs attention ({analysis.overall_score:.1%})"
                )
            
            # Add patterns
            insights['key_patterns'].extend(analysis.patterns)
            
            # Store detailed analysis
            insights['dimension_details'][dim] = {
                'score': analysis.overall_score,
                'sub_scores': analysis.sub_scores,
                'growth_indicators': analysis.growth_indicators,
                'concerns': analysis.concern_areas
            }
        
        # Generate personalized recommendations
        insights['recommendations'] = self._generate_recommendations(analyses)
        
        return insights
    
    def _get_coherence_level(self, variables: CoherenceVariables) -> str:
        """Determine overall coherence level"""
        avg_score = (variables.psi + variables.rho + variables.q + variables.f) / 4
        
        if avg_score > 0.8:
            return "Highly Coherent"
        elif avg_score > 0.6:
            return "Moderately Coherent"
        elif avg_score > 0.4:
            return "Developing Coherence"
        else:
            return "Low Coherence - Growth Opportunity"
    
    def _generate_recommendations(self, analyses: Dict[str, DimensionAnalysis]) -> List[str]:
        """Generate personalized recommendations"""
        recommendations = []
        
        # Find lowest dimension
        lowest_dim = min(analyses.items(), key=lambda x: x[1].overall_score)
        dim_name = self.dimension_context[lowest_dim[0]]['name']
        
        # Base recommendation on lowest dimension
        if lowest_dim[0] == 'psi':
            recommendations.append(
                "Daily values reflection: Spend 5 minutes each evening reviewing how your actions aligned with your values"
            )
        elif lowest_dim[0] == 'rho':
            recommendations.append(
                "Learning journal: Document one lesson learned each day and how you'll apply it"
            )
        elif lowest_dim[0] == 'q':
            recommendations.append(
                "Action commitment: Identify one small way to make a positive difference each week"
            )
        elif lowest_dim[0] == 'f':
            recommendations.append(
                "Connection practice: Schedule regular quality time with important relationships"
            )
        
        # Add general recommendations based on patterns
        for analysis in analyses.values():
            if "variation" in " ".join(analysis.patterns).lower():
                recommendations.append(
                    "Work on consistency: Your responses show variability - focus on steady practices"
                )
                break
        
        return recommendations[:3]  # Top 3 recommendations