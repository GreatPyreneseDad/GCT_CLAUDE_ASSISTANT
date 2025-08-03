# Shared GCT Types and Data Structures
# This module contains shared types to avoid circular imports

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum

# ============================================================================
# CORE DATA STRUCTURES
# ============================================================================

class AssessmentTier(Enum):
    BASIC = "basic"
    PROFESSIONAL = "professional"
    ADVANCED = "advanced"
    CONTINUOUS = "continuous"

@dataclass
class CoherenceVariables:
    """Core GCT variables with mathematical precision"""
    psi: float  # Internal Consistency (0.0-1.0)
    rho: float  # Accumulated Wisdom (0.0-1.0, age-adjusted)
    q: float    # Moral Activation Energy (0.0-1.0, biologically optimized)
    f: float    # Social Belonging Architecture (0.0-1.0)
    
    def __post_init__(self):
        # Ensure all values are within valid range
        for field in ['psi', 'rho', 'q', 'f']:
            value = getattr(self, field)
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{field} must be between 0.0 and 1.0, got {value}")

@dataclass
class CoherenceProfile:
    """Complete coherence assessment profile"""
    user_id: str
    variables: CoherenceVariables
    static_coherence: float
    coherence_velocity: Optional[float] = None
    assessment_tier: AssessmentTier = AssessmentTier.BASIC
    timestamp: datetime = None
    age: Optional[int] = None
    context: str = "general"
    individual_optimization: Dict[str, float] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.individual_optimization is None:
            self.individual_optimization = {}

@dataclass
class CommunicationAnalysis:
    """Analysis of text/speech for coherence patterns"""
    text: str
    consistency_score: float
    wisdom_indicators: float
    moral_activation: float
    social_awareness: float
    authenticity_score: float
    red_flags: List[str]
    enhancement_suggestions: List[str]
    confidence_level: float