# Narrative Feedback Generator
# Creates personalized, comprehensive text feedback based on assessment responses

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import numpy as np
from datetime import datetime, timedelta
from gct_types import CoherenceVariables, CoherenceProfile

@dataclass
class NarrativeFeedback:
    """Complete narrative feedback for a coherence assessment"""
    overall_summary: str
    coherence_state: str  # "Thriving", "Stable", "Developing", "Struggling"
    trajectory_analysis: str
    dimension_narratives: Dict[str, str]
    key_themes: List[str]
    growth_opportunities: List[str]
    actionable_steps: List[str]
    probability_assessment: Dict[str, float]  # growth/decline probabilities

class NarrativeFeedbackGenerator:
    """Generates comprehensive narrative feedback from assessment analysis"""
    
    def __init__(self):
        self.coherence_thresholds = {
            'thriving': 3.0,
            'stable': 2.0,
            'developing': 1.0,
            'struggling': 0
        }
        
        self.dimension_narratives = {
            'psi': self._generate_psi_narrative,
            'rho': self._generate_rho_narrative,
            'q': self._generate_q_narrative,
            'f': self._generate_f_narrative
        }
    
    def generate_comprehensive_feedback(self,
                                      profile: CoherenceProfile,
                                      analysis_details: Dict[str, any],
                                      response_content: Dict[str, List[Dict]],
                                      historical_profiles: Optional[List[CoherenceProfile]] = None) -> NarrativeFeedback:
        """Generate complete narrative feedback"""
        
        # Determine coherence state
        coherence_state = self._determine_coherence_state(profile.static_coherence)
        
        # Generate overall summary
        overall_summary = self._generate_overall_summary(
            profile, coherence_state, analysis_details
        )
        
        # Generate trajectory analysis
        trajectory_analysis = self._generate_trajectory_analysis(
            profile, historical_profiles, analysis_details
        )
        
        # Generate dimension-specific narratives
        dimension_narratives = {}
        for dimension in ['psi', 'rho', 'q', 'f']:
            if dimension in analysis_details.get('dimension_details', {}):
                narrative_func = self.dimension_narratives[dimension]
                dimension_narratives[dimension] = narrative_func(
                    getattr(profile.variables, dimension),
                    analysis_details['dimension_details'][dimension],
                    response_content.get(dimension, [])
                )
        
        # Extract key themes from responses
        key_themes = self._extract_key_themes(response_content, analysis_details)
        
        # Identify growth opportunities
        growth_opportunities = self._identify_growth_opportunities(
            profile, analysis_details, response_content
        )
        
        # Generate actionable steps
        actionable_steps = self._generate_actionable_steps(
            profile, growth_opportunities, analysis_details
        )
        
        # Calculate probability assessment
        probability_assessment = self._calculate_trajectory_probabilities(
            profile, historical_profiles, analysis_details
        )
        
        return NarrativeFeedback(
            overall_summary=overall_summary,
            coherence_state=coherence_state,
            trajectory_analysis=trajectory_analysis,
            dimension_narratives=dimension_narratives,
            key_themes=key_themes,
            growth_opportunities=growth_opportunities,
            actionable_steps=actionable_steps,
            probability_assessment=probability_assessment
        )
    
    def _determine_coherence_state(self, static_coherence: float) -> str:
        """Determine the coherence state category"""
        if static_coherence >= self.coherence_thresholds['thriving']:
            return "Thriving"
        elif static_coherence >= self.coherence_thresholds['stable']:
            return "Stable"
        elif static_coherence >= self.coherence_thresholds['developing']:
            return "Developing"
        else:
            return "Struggling"
    
    def _generate_overall_summary(self, profile: CoherenceProfile, 
                                state: str, analysis: Dict) -> str:
        """Generate overall summary narrative"""
        
        templates = {
            "Thriving": (
                "Your coherence profile reveals a remarkably integrated and aligned life structure. "
                "With a coherence score of {score:.2f}, you demonstrate exceptional harmony between "
                "your values, actions, wisdom, and relationships. {key_strength} "
                "This level of coherence suggests you're not just managing life's complexities—you're "
                "thriving within them."
            ),
            "Stable": (
                "Your coherence profile shows solid integration across life dimensions. "
                "With a score of {score:.2f}, you maintain good alignment between your inner values "
                "and outer expression. {key_strength} While there's room for growth, you have "
                "a strong foundation that supports meaningful progress."
            ),
            "Developing": (
                "Your coherence profile indicates you're in an active phase of growth and integration. "
                "With a score of {score:.2f}, you show promise in {strong_area}, while working to "
                "strengthen {growth_area}. This is a crucial developmental stage where focused "
                "attention can yield significant improvements."
            ),
            "Struggling": (
                "Your coherence profile suggests you're facing challenges in aligning different aspects "
                "of your life. With a score of {score:.2f}, there's significant opportunity for growth, "
                "particularly in {growth_area}. Remember, recognizing these patterns is the first step "
                "toward positive change."
            )
        }
        
        # Identify strengths and growth areas
        dims = {'psi': profile.variables.psi, 'rho': profile.variables.rho, 
                'q': profile.variables.q, 'f': profile.variables.f}
        
        strongest = max(dims.items(), key=lambda x: x[1])
        weakest = min(dims.items(), key=lambda x: x[1])
        
        strength_descriptions = {
            'psi': "Your actions consistently reflect your values",
            'rho': "You effectively learn from and integrate life experiences",
            'q': "You readily act on your moral convictions",
            'f': "You maintain deep, authentic connections"
        }
        
        area_names = {
            'psi': "internal consistency",
            'rho': "wisdom integration",
            'q': "moral activation",
            'f': "social belonging"
        }
        
        template = templates[state]
        
        if state in ["Thriving", "Stable"]:
            summary = template.format(
                score=profile.static_coherence,
                key_strength=strength_descriptions[strongest[0]]
            )
        else:
            summary = template.format(
                score=profile.static_coherence,
                strong_area=area_names[strongest[0]],
                growth_area=area_names[weakest[0]]
            )
        
        return summary
    
    def _generate_trajectory_analysis(self, current: CoherenceProfile,
                                    historical: Optional[List[CoherenceProfile]],
                                    analysis: Dict) -> str:
        """Analyze coherence trajectory"""
        
        if not historical or len(historical) < 2:
            # First assessment or insufficient history
            return self._generate_initial_trajectory(current, analysis)
        
        # Calculate velocity and acceleration
        recent_scores = [p.static_coherence for p in historical[-5:]] + [current.static_coherence]
        velocity = np.gradient(recent_scores)[-1]
        
        if len(recent_scores) > 2:
            acceleration = np.gradient(velocity)
        else:
            acceleration = 0
        
        # Determine trajectory
        if velocity > 0.01:
            if acceleration > 0:
                trajectory = "accelerating growth"
                description = (
                    "Your coherence is not just improving—it's accelerating. This suggests "
                    "you've found effective practices that are compounding in their benefits. "
                    f"At your current rate ({velocity:.3f} per assessment), you're likely to see "
                    "significant positive changes in the coming months."
                )
            else:
                trajectory = "steady growth"
                description = (
                    "You're on a positive trajectory with consistent improvements in coherence. "
                    f"Your growth rate of {velocity:.3f} per assessment shows dedication to "
                    "personal development. Maintaining this momentum will lead to meaningful progress."
                )
        elif velocity < -0.01:
            if acceleration < 0:
                trajectory = "concerning decline"
                description = (
                    "Your coherence trajectory shows a decline that appears to be accelerating. "
                    "This pattern suggests increasing disconnection between different life dimensions. "
                    "Immediate intervention with focused practices is recommended to reverse this trend."
                )
            else:
                trajectory = "stabilizing after decline"
                description = (
                    "While your coherence has been declining, the rate of decline is slowing. "
                    "This suggests you may be finding your footing. With focused effort, you can "
                    "turn this trajectory around."
                )
        else:
            trajectory = "stable"
            description = (
                "Your coherence remains relatively stable. While stability can be positive, "
                "consider whether you're in a comfort zone that might benefit from intentional "
                "growth challenges."
            )
        
        # Add pattern analysis
        patterns = self._identify_trajectory_patterns(historical + [current])
        if patterns:
            description += f" {patterns}"
        
        return description
    
    def _generate_initial_trajectory(self, profile: CoherenceProfile, analysis: Dict) -> str:
        """Generate trajectory analysis for first assessment"""
        
        base_analysis = (
            "As this is your initial assessment, we're establishing your baseline coherence profile. "
        )
        
        # Analyze current state indicators
        indicators = []
        
        # Check for high variability between dimensions
        dims = [profile.variables.psi, profile.variables.rho, profile.variables.q, profile.variables.f]
        variability = np.std(dims)
        
        if variability > 0.2:
            indicators.append(
                "The significant variation between your dimensions suggests untapped potential—"
                "bringing your lower dimensions up to match your strengths could dramatically "
                "improve your overall coherence"
            )
        
        # Check for specific patterns
        if profile.variables.rho > 0.7 and profile.variables.q < 0.5:
            indicators.append(
                "You show strong wisdom integration but lower action orientation, suggesting "
                "that translating insights into action could be a key growth lever"
            )
        
        if profile.variables.f < 0.4:
            indicators.append(
                "Your social belonging score indicates potential isolation, which can impact "
                "all other dimensions over time"
            )
        
        prediction = base_analysis
        if indicators:
            prediction += " Based on your responses: " + ". ".join(indicators) + "."
        
        return prediction
    
    def _identify_trajectory_patterns(self, profiles: List[CoherenceProfile]) -> str:
        """Identify patterns in coherence trajectory"""
        
        if len(profiles) < 3:
            return ""
        
        patterns = []
        
        # Check for dimension-specific trends
        for dim in ['psi', 'rho', 'q', 'f']:
            values = [getattr(p.variables, dim) for p in profiles]
            trend = np.polyfit(range(len(values)), values, 1)[0]
            
            if abs(trend) > 0.02:
                dim_names = {
                    'psi': "internal consistency",
                    'rho': "wisdom integration", 
                    'q': "moral activation",
                    'f': "social belonging"
                }
                
                if trend > 0:
                    patterns.append(f"Notable improvement in {dim_names[dim]}")
                else:
                    patterns.append(f"Declining {dim_names[dim]} needs attention")
        
        if patterns:
            return "Specific patterns: " + ", ".join(patterns) + "."
        
        return ""
    
    def _generate_psi_narrative(self, score: float, details: Dict, responses: List[Dict]) -> str:
        """Generate narrative for Internal Consistency dimension"""
        
        narrative = f"**Internal Consistency (Ψ): {score:.1%}**\n\n"
        
        # Analyze responses for themes
        value_action_gaps = []
        consistency_examples = []
        
        for resp in responses:
            if 'values' in resp.get('answer', '').lower():
                if 'but' in resp['answer'].lower() or 'however' in resp['answer'].lower():
                    value_action_gaps.append(resp['answer'])
                else:
                    consistency_examples.append(resp['answer'])
        
        if score > 0.7:
            narrative += (
                "Your responses reveal strong alignment between your stated values and lived actions. "
            )
            if consistency_examples:
                narrative += (
                    "This is particularly evident in how you describe your decision-making process. "
                )
        elif score > 0.4:
            narrative += (
                "You show moderate consistency between values and actions, with some areas of disconnect. "
            )
            if value_action_gaps:
                narrative += (
                    "Your awareness of these gaps is actually a strength—recognition is the first step to alignment. "
                )
        else:
            narrative += (
                "There appears to be significant tension between your ideals and your daily choices. "
                "This internal conflict may be creating stress and limiting your effectiveness. "
            )
        
        # Add specific insights from sub-dimensions
        if 'sub_dimensions' in details:
            subs = details['sub_dimensions']
            if subs.get('emotional_congruence', 0) < subs.get('value_action_alignment', 0):
                narrative += (
                    "\n\nNotably, while your actions often align with values, your emotional responses "
                    "sometimes conflict with your beliefs. This emotional incongruence may be worth exploring."
                )
        
        return narrative
    
    def _generate_rho_narrative(self, score: float, details: Dict, responses: List[Dict]) -> str:
        """Generate narrative for Wisdom Integration dimension"""
        
        narrative = f"**Wisdom Integration (ρ): {score:.1%}**\n\n"
        
        # Look for learning patterns in responses
        growth_stories = [r for r in responses if 'learn' in r.get('answer', '').lower()]
        
        if score > 0.7:
            narrative += (
                "You demonstrate exceptional ability to extract wisdom from experiences and apply it forward. "
            )
            if growth_stories:
                narrative += (
                    "Your examples show a pattern of transforming challenges into lasting insights. "
                    "This metacognitive awareness—learning how you learn—is a powerful asset."
                )
        elif score > 0.4:
            narrative += (
                "You show developing capacity for learning from experience, though the integration process "
                "could be more systematic. "
            )
            if details.get('sub_dimensions', {}).get('pattern_recognition', 0) < 0.5:
                narrative += (
                    "Strengthening your ability to recognize patterns across different experiences "
                    "could accelerate your wisdom development."
                )
        else:
            narrative += (
                "Your responses suggest difficulty in extracting lasting lessons from experiences. "
                "You may be repeating patterns without recognizing them. "
            )
        
        return narrative
    
    def _generate_q_narrative(self, score: float, details: Dict, responses: List[Dict]) -> str:
        """Generate narrative for Moral Activation dimension"""
        
        narrative = f"**Moral Activation (q): {score:.1%}**\n\n"
        
        action_stories = [r for r in responses if any(word in r.get('answer', '').lower() 
                         for word in ['acted', 'helped', 'stood up', 'intervened'])]
        
        if score > 0.7:
            narrative += (
                "You show strong moral activation—readily translating principles into action. "
            )
            if action_stories:
                narrative += (
                    "Your examples demonstrate courage and initiative in addressing injustices "
                    "or needs you encounter. This active engagement enriches both your life and your community."
                )
        elif score > 0.4:
            narrative += (
                "You have moderate moral activation, sometimes acting on your principles but not consistently. "
            )
            barriers = details.get('concerns', [])
            if barriers:
                narrative += (
                    f"Common barriers appear to include: {', '.join(barriers[:2])}. "
                    "Addressing these could unlock greater moral agency."
                )
        else:
            narrative += (
                "Your moral activation appears limited, with significant gaps between recognizing "
                "what should be done and taking action. This passivity may be contributing to "
                "feelings of powerlessness or regret."
            )
        
        return narrative
    
    def _generate_f_narrative(self, score: float, details: Dict, responses: List[Dict]) -> str:
        """Generate narrative for Social Belonging dimension"""
        
        narrative = f"**Social Belonging (f): {score:.1%}**\n\n"
        
        connection_quality = [r for r in responses if 'deep' in r.get('answer', '').lower() 
                            or 'meaningful' in r.get('answer', '').lower()]
        isolation_indicators = [r for r in responses if 'alone' in r.get('answer', '').lower() 
                              or 'lonely' in r.get('answer', '').lower()]
        
        if score > 0.7:
            narrative += (
                "Your social coherence is strong, with deep connections that provide both support and meaning. "
            )
            if connection_quality:
                narrative += (
                    "The quality of your relationships appears to be a major source of strength, "
                    "creating positive feedback loops with other life dimensions."
                )
        elif score > 0.4:
            narrative += (
                "You maintain moderate social connections, though there's room for deepening these bonds. "
            )
            if details.get('sub_dimensions', {}).get('authentic_relating', 0) < 0.5:
                narrative += (
                    "Increasing authenticity in your relationships could transform surface-level "
                    "connections into sources of real belonging."
                )
        else:
            narrative += (
                "Your sense of belonging appears challenged, potentially impacting all areas of coherence. "
            )
            if isolation_indicators:
                narrative += (
                    "The isolation you describe can become self-reinforcing. Small steps toward "
                    "connection, even if uncomfortable, can begin reversing this pattern."
                )
        
        return narrative
    
    def _extract_key_themes(self, responses: Dict[str, List[Dict]], analysis: Dict) -> List[str]:
        """Extract key themes from user responses"""
        
        themes = []
        
        # Compile all response text
        all_text = ""
        for dimension_responses in responses.values():
            for resp in dimension_responses:
                all_text += " " + resp.get('answer', '')
        
        all_text_lower = all_text.lower()
        
        # Theme detection
        theme_indicators = {
            "Work-life integration challenges": ['work', 'job', 'career', 'balance', 'stress'],
            "Family dynamics influencing coherence": ['family', 'parents', 'children', 'spouse'],
            "Identity exploration phase": ['who i am', 'identity', 'finding myself', 'purpose'],
            "Past trauma affecting present": ['trauma', 'hurt', 'pain', 'past', 'healing'],
            "Spiritual/existential seeking": ['meaning', 'spiritual', 'god', 'universe', 'purpose'],
            "Relationship patterns": ['relationships', 'partner', 'friends', 'connection'],
            "Achievement orientation": ['success', 'goals', 'achievement', 'accomplish'],
            "Fear-based decision making": ['afraid', 'fear', 'scared', 'worry', 'anxiety']
        }
        
        for theme, indicators in theme_indicators.items():
            if sum(1 for ind in indicators if ind in all_text_lower) >= 2:
                themes.append(theme)
        
        # Add themes from AI analysis if available
        if 'key_patterns' in analysis:
            themes.extend(analysis['key_patterns'][:2])
        
        return themes[:5]  # Top 5 themes
    
    def _identify_growth_opportunities(self, profile: CoherenceProfile,
                                     analysis: Dict, responses: Dict) -> List[str]:
        """Identify specific growth opportunities"""
        
        opportunities = []
        
        # Dimension-based opportunities
        dims = {'psi': profile.variables.psi, 'rho': profile.variables.rho,
                'q': profile.variables.q, 'f': profile.variables.f}
        
        lowest_two = sorted(dims.items(), key=lambda x: x[1])[:2]
        
        opportunity_map = {
            'psi': "Strengthening value-action alignment through daily reflection practices",
            'rho': "Developing systematic learning practices to extract wisdom from experiences",
            'q': "Building moral courage through incremental action steps",
            'f': "Deepening connections through vulnerable, authentic sharing"
        }
        
        for dim, score in lowest_two:
            if score < 0.6:
                opportunities.append(opportunity_map[dim])
        
        # Cross-dimensional opportunities
        if profile.variables.rho > 0.7 and profile.variables.q < 0.5:
            opportunities.append(
                "Bridging the gap between wisdom and action—you know what to do, "
                "now practice doing it"
            )
        
        if profile.variables.psi < 0.5 and profile.variables.f < 0.5:
            opportunities.append(
                "Addressing internal-external coherence through authentic self-expression "
                "in relationships"
            )
        
        # Response-based opportunities
        if analysis.get('dimension_details', {}).get('psi', {}).get('concerns'):
            opportunities.append(
                "Creating accountability structures to support consistent follow-through"
            )
        
        return opportunities
    
    def _generate_actionable_steps(self, profile: CoherenceProfile,
                                 opportunities: List[str], analysis: Dict) -> List[str]:
        """Generate specific, actionable next steps"""
        
        steps = []
        
        # Priority 1: Address lowest dimension
        dims = {'psi': profile.variables.psi, 'rho': profile.variables.rho,
                'q': profile.variables.q, 'f': profile.variables.f}
        lowest = min(dims.items(), key=lambda x: x[1])
        
        immediate_actions = {
            'psi': [
                "Tonight: Write down your top 3 values and rate how well today's actions reflected them (1-10)",
                "This week: Set one specific intention each morning that aligns with your values",
                "This month: Track the gap between intentions and actions in a simple journal"
            ],
            'rho': [
                "Tonight: Reflect on one challenge from today and write what it taught you",
                "This week: Start a 'lessons learned' note on your phone—add one insight daily",
                "This month: Review patterns in your lessons and identify recurring themes"
            ],
            'q': [
                "Tonight: Identify one small action you've been avoiding that aligns with your values",
                "This week: Take that action, no matter how small",
                "This month: Commit to one weekly action that serves others or a cause you care about"
            ],
            'f': [
                "Tonight: Reach out to one person you care about with a genuine message",
                "This week: Have one vulnerable conversation with someone you trust",
                "This month: Join a group or community aligned with your interests"
            ]
        }
        
        steps.extend(immediate_actions[lowest[0]])
        
        # Add integration practice
        steps.append(
            "Daily integration: Before bed, rate your coherence (1-10) and note what influenced it"
        )
        
        return steps[:5]  # Top 5 steps
    
    def _calculate_trajectory_probabilities(self, current: CoherenceProfile,
                                          historical: Optional[List[CoherenceProfile]],
                                          analysis: Dict) -> Dict[str, float]:
        """Calculate probabilities of growth vs decline"""
        
        if not historical:
            # Base probabilities on current state and patterns
            return self._calculate_initial_probabilities(current, analysis)
        
        # Historical trend analysis
        recent_scores = [p.static_coherence for p in historical[-5:]] + [current.static_coherence]
        
        # Calculate trend
        x = np.arange(len(recent_scores))
        slope, intercept = np.polyfit(x, recent_scores, 1)
        
        # Calculate momentum
        if len(recent_scores) > 2:
            recent_momentum = recent_scores[-1] - recent_scores[-2]
            overall_momentum = slope
        else:
            recent_momentum = 0
            overall_momentum = slope
        
        # Base probabilities on trend
        if overall_momentum > 0.01:
            base_growth = 0.7
            base_decline = 0.1
        elif overall_momentum < -0.01:
            base_growth = 0.2
            base_decline = 0.6
        else:
            base_growth = 0.4
            base_decline = 0.3
        
        # Adjust based on current level
        if current.static_coherence > 3.0:
            # High coherence is harder to improve but easier to maintain
            base_growth *= 0.7
            base_decline *= 0.8
        elif current.static_coherence < 1.0:
            # Low coherence has more room for growth
            base_growth *= 1.3
            base_decline *= 1.2
        
        # Adjust based on dimension balance
        dims = [current.variables.psi, current.variables.rho, 
                current.variables.q, current.variables.f]
        balance = 1 - np.std(dims)
        
        # Better balance improves growth probability
        base_growth *= (1 + balance * 0.2)
        
        # Normalize probabilities
        total = base_growth + base_decline + 0.2  # 0.2 for stable
        
        return {
            'growth': min(0.9, base_growth / total),
            'stable': 0.2 / total,
            'decline': min(0.9, base_decline / total)
        }
    
    def _calculate_initial_probabilities(self, profile: CoherenceProfile, 
                                       analysis: Dict) -> Dict[str, float]:
        """Calculate trajectory probabilities for first assessment"""
        
        # Base on current coherence level
        if profile.static_coherence > 2.5:
            base_growth = 0.5
            base_decline = 0.2
        elif profile.static_coherence > 1.5:
            base_growth = 0.6
            base_decline = 0.2
        else:
            base_growth = 0.7
            base_decline = 0.2
        
        # Adjust based on dimension patterns
        dims = {'psi': profile.variables.psi, 'rho': profile.variables.rho,
                'q': profile.variables.q, 'f': profile.variables.f}
        
        # High wisdom with low action suggests potential for growth
        if dims['rho'] > 0.6 and dims['q'] < 0.4:
            base_growth *= 1.2
        
        # Low social belonging is a risk factor
        if dims['f'] < 0.3:
            base_decline *= 1.3
        
        # Strong foundation (high psi) supports growth
        if dims['psi'] > 0.7:
            base_growth *= 1.1
            base_decline *= 0.8
        
        # Normalize
        total = base_growth + base_decline + 0.1
        
        return {
            'growth': min(0.85, base_growth / total),
            'stable': 0.1 / total,
            'decline': min(0.7, base_decline / total)
        }