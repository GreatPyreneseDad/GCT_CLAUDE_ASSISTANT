#!/usr/bin/env python3
"""
Demo script showing various GCT queries through the Apple Intelligence interface
"""

import requests
import json
import time

BASE_URL = "http://localhost:5001"

def simulate_query(query, user_id="demo_user"):
    """Simulate an Apple Intelligence query"""
    print(f"\n💬 User: '{query}'")
    print("🔄 Processing...")
    
    # In real implementation, this would go through the Apple Intelligence bridge
    # For demo, we'll show what the response would look like
    
    if "coherence" in query.lower() or "wellness" in query.lower():
        # Get profile
        response = requests.get(f"{BASE_URL}/api/user/{user_id}/profile")
        if response.status_code == 200:
            data = response.json()
            profile = data['profile']
            coherence = profile['static_coherence']
            variables = profile['variables']
            
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
            
            print(f"\n🤖 Assistant: {emoji} Your current coherence is {level} ({coherence:.2f}/4.0)")
            print(f"   • Internal Consistency (Ψ): {variables['psi']:.2f}")
            print(f"   • Wisdom Integration (ρ): {variables['rho']:.2f}")
            print(f"   • Moral Activation (q): {variables['q']:.2f}")
            print(f"   • Social Belonging (f): {variables['f']:.2f}")
            
            # Find lowest variable
            lowest = min(variables.items(), key=lambda x: x[1])
            var_names = {
                'psi': 'internal consistency',
                'rho': 'wisdom integration', 
                'q': 'moral activation',
                'f': 'social belonging'
            }
            print(f"\n   💡 Focus on improving your {var_names[lowest[0]]} for the biggest impact.")
    
    elif "improve" in query.lower() or "help" in query.lower():
        print("\n🤖 Assistant: Here's your personalized recovery plan:")
        print("   1. Morning Reflection (10 min)")
        print("      - Write down 3 things you're grateful for")
        print("      - Set one meaningful intention for the day")
        print("   2. Midday Check-in (5 min)")
        print("      - Rate your energy and focus (1-10)")
        print("      - Take 5 deep breaths")
        print("   3. Evening Review (10 min)")
        print("      - Journal about today's lessons learned")
        print("      - Plan tomorrow's priorities")
        print("\n   🎯 Expected improvement: 15-20% coherence boost in 2 weeks")
    
    elif "pattern" in query.lower() or "time" in query.lower():
        print("\n🤖 Assistant: Your Coherence Patterns:")
        print("   🌅 You're a morning person - coherence peaks 8-10 AM")
        print("   📊 Best days: Tuesday and Thursday")
        print("   📉 Low point: Sunday evenings")
        print("\n   💡 Schedule important decisions during your peak times")
    
    else:
        print("\n🤖 Assistant: I can help you with:")
        print("   • Checking your coherence levels")
        print("   • Creating improvement plans")
        print("   • Analyzing communication patterns")
        print("   • Understanding your daily rhythms")
        print("\n   Just ask about any of these topics!")

def main():
    print("🎯 GCT-Apple Intelligence Demo")
    print("=" * 50)
    
    # Create a demo user profile
    print("Setting up demo user...")
    data = {
        "user_id": "demo_user",
        "responses": {
            "consistency": 0.65,
            "wisdom": 0.72,
            "energy": 0.58,
            "belonging": 0.78
        },
        "age": 35
    }
    
    response = requests.post(f"{BASE_URL}/api/assessment/tier1", json=data)
    if response.status_code == 200:
        print("✅ Demo user created")
    
    # Demo queries
    queries = [
        "Check my coherence",
        "How can I improve my wellness?",
        "What are my daily patterns?",
        "I'm feeling unbalanced today",
        "Help me boost my energy"
    ]
    
    print("\n🎬 Starting demo conversation...")
    print("-" * 50)
    
    for query in queries:
        simulate_query(query)
        time.sleep(1)  # Pause between queries
    
    print("\n" + "-" * 50)
    print("✅ Demo complete!")
    print("\n🚀 The Apple Intelligence Chat app would display these")
    print("   responses in a beautiful SwiftUI interface with")
    print("   streaming text and haptic feedback!")

if __name__ == "__main__":
    main()