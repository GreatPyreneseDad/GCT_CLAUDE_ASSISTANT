#!/usr/bin/env python3
"""
Automated Test Agent for GCT Assessment System
Tests the complete assessment flow with realistic responses
"""

import asyncio
import aiohttp
import json
import random
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GCTTestAgent:
    """Automated test agent for the GCT assessment system"""
    
    def __init__(self, base_url: str = "http://localhost:5001"):
        self.base_url = base_url
        self.session: Optional[aiohttp.ClientSession] = None
        self.user_id = f"test_agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Test personas with different coherence profiles
        self.personas = {
            "thriving": {
                "name": "Alex the Aligned",
                "profile": "High coherence individual with strong values alignment",
                "responses": self._generate_thriving_responses()
            },
            "developing": {
                "name": "Sam the Seeker",
                "profile": "Growing individual with some inconsistencies",
                "responses": self._generate_developing_responses()
            },
            "struggling": {
                "name": "Jordan the Challenged",
                "profile": "Facing coherence challenges across dimensions",
                "responses": self._generate_struggling_responses()
            }
        }
        
        self.current_persona = "developing"  # Default persona
    
    def _generate_thriving_responses(self) -> Dict[str, Any]:
        """Generate responses for a high-coherence individual"""
        return {
            # PSI - Internal Consistency
            "psi_1": {
                "type": "story",
                "answer": "Last week, I had to choose between taking a high-paying project that conflicted with my environmental values and staying true to my principles. I turned it down and instead took a lower-paying project for a sustainable company. It felt incredibly liberating to honor my values, even though it meant less money."
            },
            "psi_2": {
                "type": "scale",
                "answer": 9
            },
            "psi_3": {
                "type": "true_false",
                "answer": False  # They DON'T contradict their beliefs
            },
            "psi_4": {
                "type": "true_false",
                "answer": True  # They DO keep promises to themselves
            },
            "psi_5": {
                "type": "choice",
                "answer": 0  # Always follow values
            },
            "psi_6": {
                "type": "scale",
                "answer": 8
            },
            "psi_7": {
                "type": "scale",
                "answer": 8
            },
            "psi_8": {
                "type": "story",
                "answer": "I felt most authentic during a team meeting where I respectfully disagreed with a popular but ethically questionable decision. Speaking my truth, even when it was uncomfortable, reminded me of who I truly am."
            },
            
            # RHO - Wisdom Integration
            "rho_1": {
                "type": "story",
                "answer": "My biggest failure was a startup that crashed spectacularly. But it taught me invaluable lessons about market research, team building, and resilience. Now I apply those lessons daily - I validate ideas thoroughly, invest in people first, and maintain perspective during setbacks."
            },
            "rho_2": {
                "type": "true_false",
                "answer": True  # They DO notice patterns
            },
            "rho_3": {
                "type": "scale",
                "answer": 9
            },
            "rho_4": {
                "type": "choice",
                "answer": 0  # Try to understand their perspective
            },
            "rho_5": {
                "type": "true_false",
                "answer": False  # Abilities are NOT fixed
            },
            "rho_6": {
                "type": "story",
                "answer": "I used to believe success meant climbing the corporate ladder. After burning out, I realized success is about impact and balance. This shift came from experiencing the emptiness of achievement without purpose."
            },
            "rho_7": {
                "type": "scale",
                "answer": 8
            },
            
            # Q - Moral Activation
            "q_1": {
                "type": "story",
                "answer": "I witnessed a colleague being unfairly blamed for a mistake. Despite potential backlash, I spoke up with evidence showing it was a system failure, not personal error. It was uncomfortable but necessary."
            },
            "q_2": {
                "type": "true_false",
                "answer": True  # They DO notice moral dimensions
            },
            "q_3": {
                "type": "scale",
                "answer": 8
            },
            "q_4": {
                "type": "choice",
                "answer": 1  # Modify approach based on feedback
            },
            "q_5": {
                "type": "true_false",
                "answer": True  # They DO think about impact
            },
            "q_6": {
                "type": "story",
                "answer": "I reported safety violations at my workplace, knowing it could affect my position. The personal cost was real - strained relationships with some colleagues - but preventing potential harm was more important."
            },
            "q_7": {
                "type": "scale",
                "answer": 8
            },
            
            # F - Social Belonging
            "f_1": {
                "type": "story",
                "answer": "My closest relationships are built on mutual growth and authentic connection. With my partner and two best friends, we can be completely ourselves - supporting each other through challenges while celebrating growth."
            },
            "f_2": {
                "type": "true_false",
                "answer": True  # They DO have people who understand them
            },
            "f_3": {
                "type": "scale",
                "answer": 8
            },
            "f_4": {
                "type": "choice",
                "answer": 1  # Maintains good balance
            },
            "f_5": {
                "type": "true_false",
                "answer": False  # They DON'T hide true thoughts
            },
            "f_6": {
                "type": "story",
                "answer": "At a community workshop, I felt deep belonging when everyone shared vulnerably about their struggles. The raw honesty and mutual support created a space where I felt truly seen and accepted."
            },
            "f_7": {
                "type": "choice",
                "answer": 3  # More than 5 people
            },
            "f_8": {
                "type": "scale",
                "answer": 2  # Rarely lonely
            }
        }
    
    def _generate_developing_responses(self) -> Dict[str, Any]:
        """Generate responses for someone in development"""
        return {
            # PSI - Internal Consistency
            "psi_1": {
                "type": "story",
                "answer": "I value health but recently chose to work late nights on a project instead of maintaining my exercise routine. I justified it as temporary, but it's been three weeks now. I'm struggling to get back on track."
            },
            "psi_2": {
                "type": "scale",
                "answer": 5
            },
            "psi_3": {
                "type": "true_false",
                "answer": True  # Sometimes contradicts beliefs
            },
            "psi_4": {
                "type": "true_false",
                "answer": False  # Struggles with promises
            },
            "psi_5": {
                "type": "choice",
                "answer": 3  # Depends on situation
            },
            "psi_6": {
                "type": "scale",
                "answer": 6
            },
            "psi_7": {
                "type": "scale",
                "answer": 5
            },
            "psi_8": {
                "type": "story",
                "answer": "I feel most authentic when I'm alone in nature, away from others' expectations. It's the only time I don't feel pulled in different directions."
            },
            
            # RHO - Wisdom Integration
            "rho_1": {
                "type": "story",
                "answer": "I failed at maintaining a long-term relationship due to poor communication. I'm trying to be better at expressing my needs, but old patterns keep surfacing. Progress is slow."
            },
            "rho_2": {
                "type": "true_false",
                "answer": True
            },
            "rho_3": {
                "type": "scale",
                "answer": 6
            },
            "rho_4": {
                "type": "choice",
                "answer": 1  # Defend while listening
            },
            "rho_5": {
                "type": "true_false",
                "answer": False
            },
            "rho_6": {
                "type": "story",
                "answer": "I used to think being strong meant never asking for help. After a health crisis, I learned that vulnerability is actually strength. Still working on applying this consistently."
            },
            "rho_7": {
                "type": "scale",
                "answer": 6
            },
            
            # Q - Moral Activation
            "q_1": {
                "type": "story",
                "answer": "I saw someone drop their wallet but I was running late for an important meeting. I hesitated, then quickly picked it up and caught up to them. I almost didn't though."
            },
            "q_2": {
                "type": "true_false",
                "answer": True
            },
            "q_3": {
                "type": "scale",
                "answer": 5
            },
            "q_4": {
                "type": "choice",
                "answer": 3  # Abandon and try different
            },
            "q_5": {
                "type": "true_false",
                "answer": True
            },
            "q_6": {
                "type": "story",
                "answer": "I need to have a difficult conversation with my boss about unethical practices, but I keep postponing it. The fear of consequences is paralyzing me."
            },
            "q_7": {
                "type": "scale",
                "answer": 5
            },
            
            # F - Social Belonging
            "f_1": {
                "type": "story",
                "answer": "I have a few close friends but sometimes feel like I'm wearing a mask. I want deeper connections but struggle with being fully vulnerable."
            },
            "f_2": {
                "type": "true_false",
                "answer": False
            },
            "f_3": {
                "type": "scale",
                "answer": 5
            },
            "f_4": {
                "type": "choice",
                "answer": 2  # Receives more than gives
            },
            "f_5": {
                "type": "true_false",
                "answer": True  # Does hide thoughts
            },
            "f_6": {
                "type": "story",
                "answer": "I felt belonging at a friend's wedding when I was included in the preparations. For once, I wasn't on the periphery but truly part of something."
            },
            "f_7": {
                "type": "choice",
                "answer": 1  # 1-2 people
            },
            "f_8": {
                "type": "scale",
                "answer": 6
            }
        }
    
    def _generate_struggling_responses(self) -> Dict[str, Any]:
        """Generate responses for someone struggling with coherence"""
        return {
            # PSI - Internal Consistency
            "psi_1": {
                "type": "story",
                "answer": "I can't think of a specific example. I just go with the flow mostly. My values? I guess I value success and happiness but I'm not sure what that means anymore."
            },
            "psi_2": {
                "type": "scale",
                "answer": 3
            },
            "psi_3": {
                "type": "true_false",
                "answer": True
            },
            "psi_4": {
                "type": "true_false",
                "answer": False
            },
            "psi_5": {
                "type": "choice",
                "answer": 2  # Go along with others
            },
            "psi_6": {
                "type": "scale",
                "answer": 3
            },
            "psi_7": {
                "type": "scale",
                "answer": 2
            },
            "psi_8": {
                "type": "story",
                "answer": "I honestly can't remember feeling truly authentic. I'm always adapting to what others expect."
            },
            
            # RHO - Wisdom Integration
            "rho_1": {
                "type": "story",
                "answer": "I keep making the same mistakes in relationships. I know I should change but I don't know how. Nothing seems to stick."
            },
            "rho_2": {
                "type": "true_false",
                "answer": False
            },
            "rho_3": {
                "type": "scale",
                "answer": 2
            },
            "rho_4": {
                "type": "choice",
                "answer": 3  # Try to convince them
            },
            "rho_5": {
                "type": "true_false",
                "answer": True  # Believes abilities are fixed
            },
            "rho_6": {
                "type": "story",
                "answer": "My beliefs haven't really changed. Maybe I'm just stuck being who I am."
            },
            "rho_7": {
                "type": "scale",
                "answer": 3
            },
            
            # Q - Moral Activation
            "q_1": {
                "type": "story",
                "answer": "I see unfair things happen all the time but what can I do? I'm just one person. It's not my problem."
            },
            "q_2": {
                "type": "true_false",
                "answer": False
            },
            "q_3": {
                "type": "scale",
                "answer": 2
            },
            "q_4": {
                "type": "choice",
                "answer": 2  # Hand it off
            },
            "q_5": {
                "type": "true_false",
                "answer": False
            },
            "q_6": {
                "type": "story",
                "answer": "I avoid situations where I'd have to stand up for something. It's easier that way."
            },
            "q_7": {
                "type": "scale",
                "answer": 2
            },
            
            # F - Social Belonging
            "f_1": {
                "type": "story",
                "answer": "I don't really have close relationships. People are exhausting and disappointing. I prefer to keep to myself."
            },
            "f_2": {
                "type": "true_false",
                "answer": False
            },
            "f_3": {
                "type": "scale",
                "answer": 2
            },
            "f_4": {
                "type": "choice",
                "answer": 3  # Minimal interaction
            },
            "f_5": {
                "type": "true_false",
                "answer": True
            },
            "f_6": {
                "type": "story",
                "answer": "I can't remember ever feeling like I truly belonged anywhere."
            },
            "f_7": {
                "type": "choice",
                "answer": 0  # None
            },
            "f_8": {
                "type": "scale",
                "answer": 8
            }
        }
    
    async def start(self):
        """Initialize the test session"""
        self.session = aiohttp.ClientSession()
        logger.info(f"Test agent initialized with user_id: {self.user_id}")
    
    async def close(self):
        """Close the test session"""
        if self.session:
            await self.session.close()
    
    async def test_health_check(self) -> bool:
        """Test if the backend is running"""
        try:
            async with self.session.get(f"{self.base_url}/health") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    logger.info(f"✅ Health check passed: {data}")
                    return True
                else:
                    logger.error(f"❌ Health check failed with status: {resp.status}")
                    return False
        except Exception as e:
            logger.error(f"❌ Health check error: {e}")
            return False
    
    async def test_assessment_flow(self, persona: str = "developing") -> Dict[str, Any]:
        """Run through the complete assessment flow"""
        self.current_persona = persona
        persona_data = self.personas[persona]
        logger.info(f"🎭 Testing as: {persona_data['name']} - {persona_data['profile']}")
        
        # Prepare all responses
        all_responses = persona_data['responses']
        
        # Format for API
        formatted_responses = {}
        for question_id, response_data in all_responses.items():
            formatted_responses[question_id] = {
                "question": f"Test question for {question_id}",
                "answer": response_data["answer"],
                "type": response_data["type"]
            }
        
        # Submit assessment
        logger.info("📝 Submitting assessment responses...")
        start_time = time.time()
        
        try:
            async with self.session.post(
                f"{self.base_url}/api/enhanced/assessment/complete/llm",
                json={
                    "responses": formatted_responses,
                    "user_id": f"{self.user_id}_{persona}"
                }
            ) as resp:
                elapsed = time.time() - start_time
                
                if resp.status == 200:
                    data = await resp.json()
                    logger.info(f"✅ Assessment completed in {elapsed:.2f}s")
                    
                    if data.get('success'):
                        profile = data.get('profile', {})
                        insights = data.get('insights', {})
                        
                        # Log results
                        logger.info(f"📊 Coherence Score: {profile.get('static_coherence', 0):.2f}/4.0")
                        logger.info(f"📈 Coherence State: {insights.get('narrative_feedback', {}).get('coherence_state', 'Unknown')}")
                        
                        # Log dimension scores
                        variables = profile.get('variables', {})
                        logger.info("📐 Dimension Scores:")
                        logger.info(f"  - Ψ (Internal Consistency): {variables.get('psi', 0)*100:.0f}%")
                        logger.info(f"  - ρ (Wisdom Integration): {variables.get('rho', 0)*100:.0f}%")
                        logger.info(f"  - q (Moral Activation): {variables.get('q', 0)*100:.0f}%")
                        logger.info(f"  - f (Social Belonging): {variables.get('f', 0)*100:.0f}%")
                        
                        # Log trajectory prediction
                        prob = insights.get('narrative_feedback', {}).get('probability_assessment', {})
                        if prob:
                            logger.info("🔮 Trajectory Prediction:")
                            logger.info(f"  - Growth: {prob.get('growth', 0)*100:.0f}%")
                            logger.info(f"  - Stable: {prob.get('stable', 0)*100:.0f}%")
                            logger.info(f"  - Decline: {prob.get('decline', 0)*100:.0f}%")
                        
                        return data
                    else:
                        logger.error(f"❌ Assessment failed: {data.get('error', 'Unknown error')}")
                        return data
                else:
                    error_text = await resp.text()
                    logger.error(f"❌ Assessment failed with status {resp.status}: {error_text}")
                    return {"success": False, "error": error_text}
                    
        except Exception as e:
            logger.error(f"❌ Assessment error: {e}")
            return {"success": False, "error": str(e)}
    
    async def test_all_personas(self) -> Dict[str, Any]:
        """Test all personas and compare results"""
        results = {}
        
        for persona in self.personas.keys():
            logger.info(f"\n{'='*60}")
            result = await self.test_assessment_flow(persona)
            results[persona] = result
            await asyncio.sleep(2)  # Pause between tests
        
        # Compare results
        logger.info(f"\n{'='*60}")
        logger.info("📊 COMPARATIVE RESULTS:")
        logger.info(f"{'='*60}")
        
        for persona, result in results.items():
            if result.get('success'):
                profile = result.get('profile', {})
                name = self.personas[persona]['name']
                score = profile.get('static_coherence', 0)
                state = result.get('insights', {}).get('narrative_feedback', {}).get('coherence_state', 'Unknown')
                logger.info(f"{name}: {score:.2f}/4.0 - {state}")
        
        return results
    
    async def test_error_handling(self) -> Dict[str, Any]:
        """Test error handling with invalid data"""
        logger.info("\n🧪 Testing error handling...")
        
        tests = {
            "empty_responses": {
                "responses": {},
                "user_id": "test_empty"
            },
            "invalid_types": {
                "responses": {
                    "psi_1": {
                        "question": "Test",
                        "answer": None,
                        "type": "invalid_type"
                    }
                },
                "user_id": "test_invalid"
            }
        }
        
        results = {}
        for test_name, test_data in tests.items():
            try:
                async with self.session.post(
                    f"{self.base_url}/api/enhanced/assessment/complete/llm",
                    json=test_data
                ) as resp:
                    data = await resp.json()
                    results[test_name] = {
                        "status": resp.status,
                        "success": data.get('success', False),
                        "error": data.get('error')
                    }
                    logger.info(f"Test '{test_name}': Status {resp.status}, Success: {data.get('success')}")
            except Exception as e:
                results[test_name] = {"error": str(e)}
                logger.error(f"Test '{test_name}' error: {e}")
        
        return results

async def main():
    """Run all tests"""
    agent = GCTTestAgent()
    
    try:
        await agent.start()
        
        # 1. Health check
        logger.info("🏥 Running health check...")
        if not await agent.test_health_check():
            logger.error("Backend is not running! Please start it first.")
            return
        
        # 2. Test single persona
        logger.info("\n🧪 Testing single assessment flow...")
        await agent.test_assessment_flow("developing")
        
        # 3. Test all personas
        logger.info("\n🎭 Testing all personas...")
        await agent.test_all_personas()
        
        # 4. Test error handling
        logger.info("\n⚠️ Testing error handling...")
        await agent.test_error_handling()
        
        logger.info("\n✅ All tests completed!")
        
    finally:
        await agent.close()

if __name__ == "__main__":
    # Run the test agent
    asyncio.run(main())