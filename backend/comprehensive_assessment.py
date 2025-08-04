# Comprehensive Assessment Framework
# Deep, multi-layered assessment with varied question types

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import json

class QuestionType(Enum):
    OPEN_STORY = "story"          # Tell me about a time when...
    TRUE_FALSE = "true_false"     # True/False questions
    SCALE = "scale"               # 1-10 rating
    MULTIPLE_CHOICE = "choice"    # Multiple choice
    FOLLOW_UP = "follow_up"       # Dynamic follow-up based on previous answer

@dataclass
class AssessmentQuestion:
    """Represents a single assessment question"""
    id: str
    dimension: str  # psi, rho, q, f
    text: str
    type: QuestionType
    weight: float = 1.0  # How much this question contributes to the dimension score
    options: Optional[List[str]] = None  # For multiple choice
    scale_labels: Optional[Tuple[str, str]] = None  # For scale questions
    follow_ups: Optional[Dict[str, str]] = None  # Conditional follow-ups
    scoring_hints: Optional[Dict[str, float]] = None  # How to score different responses

class ComprehensiveAssessmentFramework:
    """Comprehensive assessment with deep probing questions"""
    
    def __init__(self):
        self.assessment_structure = self._build_assessment_structure()
        self.dimension_weights = {
            'psi': {'base': 0.25, 'sub_dimensions': self._get_psi_subdimensions()},
            'rho': {'base': 0.25, 'sub_dimensions': self._get_rho_subdimensions()},
            'q': {'base': 0.25, 'sub_dimensions': self._get_q_subdimensions()},
            'f': {'base': 0.25, 'sub_dimensions': self._get_f_subdimensions()}
        }
    
    def _get_psi_subdimensions(self) -> Dict[str, float]:
        """Sub-dimensions of Internal Consistency (Ψ)"""
        return {
            'value_action_alignment': 0.25,    # How well actions match stated values
            'emotional_congruence': 0.25,      # Emotional responses match beliefs
            'behavioral_consistency': 0.25,     # Consistent behavior across contexts
            'identity_integration': 0.25        # Unified sense of self
        }
    
    def _get_rho_subdimensions(self) -> Dict[str, float]:
        """Sub-dimensions of Wisdom Integration (ρ)"""
        return {
            'pattern_recognition': 0.25,        # Seeing patterns in experiences
            'learning_application': 0.25,       # Applying lessons learned
            'perspective_taking': 0.25,         # Understanding multiple viewpoints
            'growth_mindset': 0.25             # Openness to learning and change
        }
    
    def _get_q_subdimensions(self) -> Dict[str, float]:
        """Sub-dimensions of Moral Activation (q)"""
        return {
            'moral_sensitivity': 0.25,          # Recognizing moral situations
            'action_initiation': 0.25,          # Taking the first step
            'perseverance': 0.25,               # Following through despite obstacles
            'impact_awareness': 0.25            # Understanding consequences of action/inaction
        }
    
    def _get_f_subdimensions(self) -> Dict[str, float]:
        """Sub-dimensions of Social Belonging (f)"""
        return {
            'relationship_depth': 0.25,         # Quality of close relationships
            'community_connection': 0.25,       # Sense of belonging to groups
            'social_contribution': 0.25,        # Giving to others/community
            'authentic_relating': 0.25          # Being genuine in relationships
        }
    
    def _build_assessment_structure(self) -> Dict[str, List[AssessmentQuestion]]:
        """Build the complete assessment question tree"""
        return {
            'psi': self._build_psi_questions(),
            'rho': self._build_rho_questions(),
            'q': self._build_q_questions(),
            'f': self._build_f_questions()
        }
    
    def _build_psi_questions(self) -> List[AssessmentQuestion]:
        """Build Internal Consistency (Ψ) questions"""
        return [
            # Opening story question
            AssessmentQuestion(
                id="psi_1",
                dimension="psi",
                text="Tell me about a recent decision where you had to choose between what was easy and what aligned with your values. What happened?",
                type=QuestionType.OPEN_STORY,
                weight=2.0
            ),
            
            # Follow-up based on story
            AssessmentQuestion(
                id="psi_2",
                dimension="psi",
                text="In that situation, how satisfied were you with your choice?",
                type=QuestionType.SCALE,
                scale_labels=("Very dissatisfied", "Very satisfied"),
                weight=1.0
            ),
            
            # True/False probes
            AssessmentQuestion(
                id="psi_3",
                dimension="psi",
                text="I often find myself doing things that contradict what I say I believe in.",
                type=QuestionType.TRUE_FALSE,
                weight=1.5,
                scoring_hints={"true": 0.2, "false": 0.8}
            ),
            
            AssessmentQuestion(
                id="psi_4",
                dimension="psi",
                text="When I make promises to myself, I almost always keep them.",
                type=QuestionType.TRUE_FALSE,
                weight=1.5,
                scoring_hints={"true": 0.8, "false": 0.2}
            ),
            
            # Multiple choice scenario
            AssessmentQuestion(
                id="psi_5",
                dimension="psi",
                text="When your personal values conflict with what others expect of you, you typically:",
                type=QuestionType.MULTIPLE_CHOICE,
                options=[
                    "Always follow your values, regardless of consequences",
                    "Try to find a compromise that honors both",
                    "Go along with others to avoid conflict",
                    "It depends entirely on the situation"
                ],
                weight=2.0,
                scoring_hints={
                    "0": 0.9,  # Strong consistency
                    "1": 0.7,  # Thoughtful balance
                    "2": 0.3,  # Low consistency
                    "3": 0.5   # Context-dependent
                }
            ),
            
            # Scale questions for sub-dimensions
            AssessmentQuestion(
                id="psi_6",
                dimension="psi",
                text="How often do your emotions align with your logical understanding of situations?",
                type=QuestionType.SCALE,
                scale_labels=("Never", "Always"),
                weight=1.0
            ),
            
            AssessmentQuestion(
                id="psi_7",
                dimension="psi",
                text="Rate how consistently you behave across different areas of your life (work, home, social):",
                type=QuestionType.SCALE,
                scale_labels=("Very inconsistent", "Very consistent"),
                weight=1.5
            ),
            
            # Deeper probe
            AssessmentQuestion(
                id="psi_8",
                dimension="psi",
                text="Describe a time when you felt most authentic and true to yourself. What were the circumstances?",
                type=QuestionType.OPEN_STORY,
                weight=1.5
            )
        ]
    
    def _build_rho_questions(self) -> List[AssessmentQuestion]:
        """Build Wisdom Integration (ρ) questions"""
        return [
            # Opening story
            AssessmentQuestion(
                id="rho_1",
                dimension="rho",
                text="Share a significant challenge or failure from your past. What did you learn, and how do you apply that lesson today?",
                type=QuestionType.OPEN_STORY,
                weight=2.0
            ),
            
            # Pattern recognition
            AssessmentQuestion(
                id="rho_2",
                dimension="rho",
                text="I often notice patterns in my life experiences that help me make better decisions.",
                type=QuestionType.TRUE_FALSE,
                weight=1.5,
                scoring_hints={"true": 0.8, "false": 0.3}
            ),
            
            # Learning application scale
            AssessmentQuestion(
                id="rho_3",
                dimension="rho",
                text="When facing new challenges, how often do you consciously apply lessons from past experiences?",
                type=QuestionType.SCALE,
                scale_labels=("Never", "Always"),
                weight=1.5
            ),
            
            # Perspective taking
            AssessmentQuestion(
                id="rho_4",
                dimension="rho",
                text="When someone disagrees with you, you typically:",
                type=QuestionType.MULTIPLE_CHOICE,
                options=[
                    "Try to understand their perspective before responding",
                    "Defend your position while listening to theirs",
                    "Agree to disagree without exploring further",
                    "Try to convince them you're right"
                ],
                weight=1.5,
                scoring_hints={"0": 0.9, "1": 0.7, "2": 0.4, "3": 0.2}
            ),
            
            # Growth mindset assessment
            AssessmentQuestion(
                id="rho_5",
                dimension="rho",
                text="My abilities and wisdom are fixed traits that don't change much over time.",
                type=QuestionType.TRUE_FALSE,
                weight=1.0,
                scoring_hints={"true": 0.2, "false": 0.8}
            ),
            
            # Wisdom integration story
            AssessmentQuestion(
                id="rho_6",
                dimension="rho",
                text="Tell me about a belief or assumption you've changed significantly over the years. What caused this shift?",
                type=QuestionType.OPEN_STORY,
                weight=1.5
            ),
            
            # Practical wisdom
            AssessmentQuestion(
                id="rho_7",
                dimension="rho",
                text="How well do you recognize when a current situation is similar to something you've experienced before?",
                type=QuestionType.SCALE,
                scale_labels=("Very poorly", "Very well"),
                weight=1.0
            )
        ]
    
    def _build_q_questions(self) -> List[AssessmentQuestion]:
        """Build Moral Activation (q) questions"""
        return [
            # Opening scenario
            AssessmentQuestion(
                id="q_1",
                dimension="q",
                text="Describe a recent situation where you witnessed something wrong or unjust. What did you do, and why?",
                type=QuestionType.OPEN_STORY,
                weight=2.0
            ),
            
            # Moral sensitivity
            AssessmentQuestion(
                id="q_2",
                dimension="q",
                text="I often notice moral dimensions in everyday situations that others might overlook.",
                type=QuestionType.TRUE_FALSE,
                weight=1.0,
                scoring_hints={"true": 0.8, "false": 0.3}
            ),
            
            # Action initiation
            AssessmentQuestion(
                id="q_3",
                dimension="q",
                text="When you see an opportunity to help or make a difference, how quickly do you act?",
                type=QuestionType.SCALE,
                scale_labels=("Very slowly/Never", "Immediately"),
                weight=1.5
            ),
            
            # Perseverance scenario
            AssessmentQuestion(
                id="q_4",
                dimension="q",
                text="You start a community project that faces unexpected resistance. You would most likely:",
                type=QuestionType.MULTIPLE_CHOICE,
                options=[
                    "Push through despite the obstacles",
                    "Modify your approach based on feedback",
                    "Hand it off to someone else",
                    "Abandon it and try something different"
                ],
                weight=1.5,
                scoring_hints={"0": 0.9, "1": 0.8, "2": 0.4, "3": 0.3}
            ),
            
            # Impact awareness
            AssessmentQuestion(
                id="q_5",
                dimension="q",
                text="I regularly think about how my actions (or inaction) affect others.",
                type=QuestionType.TRUE_FALSE,
                weight=1.0,
                scoring_hints={"true": 0.8, "false": 0.2}
            ),
            
            # Cost of action
            AssessmentQuestion(
                id="q_6",
                dimension="q",
                text="Tell me about a time when doing the right thing came at a personal cost. How did you handle it?",
                type=QuestionType.OPEN_STORY,
                weight=2.0
            ),
            
            # Moral courage scale
            AssessmentQuestion(
                id="q_7",
                dimension="q",
                text="How willing are you to stand up for your principles when it's unpopular or risky?",
                type=QuestionType.SCALE,
                scale_labels=("Not at all willing", "Completely willing"),
                weight=1.5
            )
        ]
    
    def _build_f_questions(self) -> List[AssessmentQuestion]:
        """Build Social Belonging (f) questions"""
        return [
            # Opening reflection
            AssessmentQuestion(
                id="f_1",
                dimension="f",
                text="Describe your closest relationships. What makes them meaningful to you?",
                type=QuestionType.OPEN_STORY,
                weight=2.0
            ),
            
            # Relationship depth
            AssessmentQuestion(
                id="f_2",
                dimension="f",
                text="I have people in my life who truly understand and accept me for who I am.",
                type=QuestionType.TRUE_FALSE,
                weight=1.5,
                scoring_hints={"true": 0.8, "false": 0.2}
            ),
            
            # Community connection scale
            AssessmentQuestion(
                id="f_3",
                dimension="f",
                text="How connected do you feel to your broader community or social groups?",
                type=QuestionType.SCALE,
                scale_labels=("Completely disconnected", "Deeply connected"),
                weight=1.5
            ),
            
            # Social contribution
            AssessmentQuestion(
                id="f_4",
                dimension="f",
                text="In your relationships and communities, you tend to be:",
                type=QuestionType.MULTIPLE_CHOICE,
                options=[
                    "Someone who gives more than they receive",
                    "Someone who maintains a good balance",
                    "Someone who receives more than they give",
                    "Someone who keeps interactions minimal"
                ],
                weight=1.0,
                scoring_hints={"0": 0.7, "1": 0.9, "2": 0.4, "3": 0.2}
            ),
            
            # Authentic relating
            AssessmentQuestion(
                id="f_5",
                dimension="f",
                text="I often hide my true thoughts and feelings to maintain relationships.",
                type=QuestionType.TRUE_FALSE,
                weight=1.0,
                scoring_hints={"true": 0.3, "false": 0.8}
            ),
            
            # Belonging story
            AssessmentQuestion(
                id="f_6",
                dimension="f",
                text="Tell me about a time when you felt a deep sense of belonging. What created that feeling?",
                type=QuestionType.OPEN_STORY,
                weight=1.5
            ),
            
            # Support system
            AssessmentQuestion(
                id="f_7",
                dimension="f",
                text="If you faced a major life crisis tomorrow, how many people could you turn to for genuine support?",
                type=QuestionType.MULTIPLE_CHOICE,
                options=[
                    "None",
                    "1-2 people",
                    "3-5 people",
                    "More than 5 people"
                ],
                weight=1.5,
                scoring_hints={"0": 0.1, "1": 0.4, "2": 0.7, "3": 0.9}
            ),
            
            # Loneliness check
            AssessmentQuestion(
                id="f_8",
                dimension="f",
                text="How often do you feel lonely or isolated, even when around others?",
                type=QuestionType.SCALE,
                scale_labels=("Never", "Always"),
                weight=1.0
            )
        ]
    
    def get_question_sequence(self, dimension: str, responses: Dict[str, Any] = None) -> List[AssessmentQuestion]:
        """Get the appropriate question sequence for a dimension"""
        base_questions = self.assessment_structure.get(dimension, [])
        
        # Add dynamic follow-ups based on responses
        if responses:
            # Add contextual follow-ups based on patterns in responses
            follow_ups = self._generate_dynamic_followups(dimension, responses)
            base_questions.extend(follow_ups)
        
        return base_questions
    
    def _generate_dynamic_followups(self, dimension: str, responses: Dict[str, Any]) -> List[AssessmentQuestion]:
        """Generate follow-up questions based on responses"""
        follow_ups = []
        
        # Analyze response patterns
        if dimension == 'psi':
            # If inconsistency detected, probe deeper
            if self._detect_inconsistency(responses):
                follow_ups.append(AssessmentQuestion(
                    id=f"psi_followup_1",
                    dimension="psi",
                    text="You mentioned some conflicts between your values and actions. What makes it challenging to maintain consistency?",
                    type=QuestionType.OPEN_STORY,
                    weight=1.5
                ))
        
        elif dimension == 'rho':
            # If limited learning indicated, explore barriers
            if self._detect_learning_barriers(responses):
                follow_ups.append(AssessmentQuestion(
                    id=f"rho_followup_1",
                    dimension="rho",
                    text="What obstacles do you face when trying to learn from your experiences?",
                    type=QuestionType.OPEN_STORY,
                    weight=1.0
                ))
        
        return follow_ups
    
    def _detect_inconsistency(self, responses: Dict[str, Any]) -> bool:
        """Detect patterns suggesting internal inconsistency"""
        # Simplified detection logic
        low_scores = sum(1 for r in responses.values() 
                        if isinstance(r, (int, float)) and r < 0.4)
        return low_scores >= 2
    
    def _detect_learning_barriers(self, responses: Dict[str, Any]) -> bool:
        """Detect patterns suggesting learning barriers"""
        # Simplified detection logic
        return any('stuck' in str(r).lower() or 'same' in str(r).lower() 
                  for r in responses.values() if isinstance(r, str))
    
    def calculate_dimension_score(self, dimension: str, responses: Dict[str, Any]) -> float:
        """Calculate weighted score for a dimension based on all responses"""
        questions = self.assessment_structure.get(dimension, [])
        
        total_weight = 0
        weighted_score = 0
        
        for question in questions:
            response = responses.get(question.id)
            if response is not None:
                score = self._score_response(question, response)
                weighted_score += score * question.weight
                total_weight += question.weight
        
        if total_weight > 0:
            return weighted_score / total_weight
        return 0.5  # Default middle score
    
    def _score_response(self, question: AssessmentQuestion, response: Any) -> float:
        """Score a single response based on question type and content"""
        if question.type == QuestionType.TRUE_FALSE:
            if question.scoring_hints:
                return question.scoring_hints.get(str(response).lower(), 0.5)
            return 0.8 if response else 0.2
        
        elif question.type == QuestionType.SCALE:
            # Assume response is 0-10, normalize to 0-1
            return float(response) / 10.0
        
        elif question.type == QuestionType.MULTIPLE_CHOICE:
            if question.scoring_hints:
                return question.scoring_hints.get(str(response), 0.5)
            return 0.5
        
        elif question.type == QuestionType.OPEN_STORY:
            # Analyze story content for coherence indicators
            return self._analyze_story_response(question.dimension, str(response))
        
        return 0.5
    
    def _analyze_story_response(self, dimension: str, story: str) -> float:
        """Analyze open-ended story responses"""
        # This would use more sophisticated NLP in production
        
        # Positive indicators by dimension
        positive_indicators = {
            'psi': ['aligned', 'consistent', 'authentic', 'true to', 'integrity'],
            'rho': ['learned', 'realized', 'understood', 'grew', 'changed'],
            'q': ['acted', 'helped', 'stood up', 'made a difference', 'took action'],
            'f': ['connected', 'supported', 'belonging', 'together', 'understood']
        }
        
        # Check for positive indicators
        indicators = positive_indicators.get(dimension, [])
        score = 0.5  # Base score
        
        story_lower = story.lower()
        for indicator in indicators:
            if indicator in story_lower:
                score += 0.1
        
        # Adjust for story length and complexity
        word_count = len(story.split())
        if word_count > 50:
            score += 0.1
        if word_count > 100:
            score += 0.05
        
        return min(1.0, score)