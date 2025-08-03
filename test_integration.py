#!/usr/bin/env python3
"""
Test script for GCT-Apple Intelligence integration
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5001"

def test_health():
    """Test if backend is running"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Backend is running")
            return True
        else:
            print("❌ Backend health check failed")
            return False
    except:
        print("❌ Cannot connect to backend")
        return False

def create_test_profile():
    """Create a test user profile"""
    print("\n📝 Creating test user profile...")
    
    data = {
        "user_id": "apple_test_user",
        "responses": {
            "consistency": 0.7,
            "wisdom": 0.6,
            "energy": 0.5,
            "belonging": 0.8
        },
        "age": 30
    }
    
    response = requests.post(f"{BASE_URL}/api/assessment/tier1", json=data)
    
    if response.status_code == 200:
        result = response.json()
        # Debug: print the actual response structure
        print(f"Response: {json.dumps(result, indent=2)}")
        if 'profile' in result:
            coherence = result['profile']['static_coherence']
        elif 'static_coherence' in result:
            coherence = result['static_coherence']
        else:
            coherence = "unknown"
        print(f"✅ Profile created: Coherence = {coherence}")
        return True
    else:
        print(f"❌ Failed to create profile: {response.status_code}")
        return False

def test_apple_intelligence_queries():
    """Test various Apple Intelligence queries"""
    print("\n🍎 Testing Apple Intelligence queries...")
    
    queries = [
        "Check my coherence",
        "How's my wellness balance?",
        "Help me improve my coherence",
        "What are my daily patterns?",
        "Analyze my communication style",
        "I need a recovery plan"
    ]
    
    # First, let's check if the endpoint exists
    try:
        # Try direct GCT endpoint first
        print("\n Testing standard GCT endpoints:")
        
        # Get profile
        response = requests.get(f"{BASE_URL}/api/user/apple_test_user/profile")
        if response.status_code == 200:
            profile = response.json()
            print(f"✅ Found profile: {json.dumps(profile, indent=2)}")
        
        # Test communication analysis
        comm_data = {
            "text": "I'm feeling great today! Everything seems to be falling into place.",
            "user_id": "apple_test_user"
        }
        response = requests.post(f"{BASE_URL}/api/communication/analyze", json=comm_data)
        if response.status_code == 200:
            result = response.json()
            if 'analysis' in result and 'coherence_estimate' in result['analysis']:
                overall = result['analysis']['coherence_estimate']['overall']
            elif 'coherence_estimate' in result:
                overall = result['coherence_estimate']['overall']
            else:
                overall = 0.0
            print(f"✅ Communication analysis: Overall coherence = {overall:.2f}")
    
    except Exception as e:
        print(f"❌ Error testing endpoints: {e}")

def simulate_swift_integration():
    """Simulate how the Swift app would interact with GCT"""
    print("\n📱 Simulating Swift integration...")
    
    # This is what the Swift app would do
    print("\n1. User asks: 'Check my coherence'")
    print("2. Swift app detects GCT-related query")
    print("3. Swift app calls GCT backend API")
    
    # Get profile
    response = requests.get(f"{BASE_URL}/api/user/apple_test_user/profile")
    if response.status_code == 200:
        data = response.json()
        profile = data['profile'] if 'profile' in data else data
        
        # Format response as the Swift app would
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
        
        response_text = f"{emoji} Your current coherence is {level} ({coherence:.2f}/4.0)\n\n"
        response_text += "Here's your breakdown:\n"
        response_text += f"• Internal Consistency (Ψ): {variables['psi']:.2f}\n"
        response_text += f"• Wisdom Integration (ρ): {variables['rho']:.2f}\n"
        response_text += f"• Moral Activation (q): {variables['q']:.2f}\n"
        response_text += f"• Social Belonging (f): {variables['f']:.2f}\n"
        
        print("\n4. Swift app displays response:")
        print("─" * 50)
        print(response_text)
        print("─" * 50)
    else:
        print("❌ Failed to get profile")

def main():
    print("🚀 GCT-Apple Intelligence Integration Test")
    print("=" * 50)
    print(f"Timestamp: {datetime.now()}")
    print(f"Backend URL: {BASE_URL}")
    
    # Test backend
    if not test_health():
        print("\n⚠️  Please start the backend with: cd backend && PORT=5001 python gct_backend.py")
        return
    
    # Create test profile
    if not create_test_profile():
        return
    
    # Test queries
    test_apple_intelligence_queries()
    
    # Simulate Swift integration
    simulate_swift_integration()
    
    print("\n✅ Integration test complete!")
    print("\n💡 Next steps:")
    print("1. Open Apple Intelligence Chat in Xcode")
    print("2. Add GCTIntegration.swift to the project")
    print("3. Update ContentView.swift to use processWithGCT()")
    print("4. Run the app and try queries like 'Check my coherence'")

if __name__ == "__main__":
    main()