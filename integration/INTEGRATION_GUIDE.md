# GCT-Apple Intelligence Integration Guide

This guide explains how to integrate the GCT Assistant with the Apple Intelligence Chat application.

## Overview

The integration enables Apple Intelligence Chat to:
- Access GCT coherence analysis
- Provide personalized wellness insights
- Generate recovery plans
- Analyze communication patterns
- Track temporal coherence patterns

## Architecture

```
┌─────────────────────────┐     ┌─────────────────────────┐
│  Apple Intelligence     │     │     GCT Assistant       │
│      Chat (Swift)       │────▶│   Backend (Python)      │
│                         │     │                         │
│  - SwiftUI Interface    │     │  - Flask API           │
│  - Foundation Models    │     │  - SQLite DB           │
│  - GCTIntegration.swift│     │  - GPU Acceleration    │
└─────────────────────────┘     └─────────────────────────┘
                │                           │
                └───────────────────────────┘
                    HTTP REST API
```

## Setup Instructions

### 1. Backend Setup

First, ensure the GCT backend is running:

```bash
cd /Users/chris/GCT_CLAUDE_ASSISTANT/backend
source venv/bin/activate
PORT=5001 python gct_backend.py
```

### 2. Add Bridge Endpoints

The bridge endpoints are already integrated into the backend through the `gct_apple_intelligence_bridge.py` module.

### 3. Swift Integration

1. Copy `GCTIntegration.swift` to your Apple Intelligence Chat Xcode project
2. Add it to your project target
3. Modify `ContentView.swift` to use GCT integration:

```swift
// In ContentView.swift, modify the sendMessage function:

private func sendMessage() {
    isResponding = true
    let userMessage = ChatMessage(role: .user, text: inputText)
    messages.append(userMessage)
    let prompt = inputText
    inputText = ""
    
    messages.append(ChatMessage(role: .assistant, text: ""))
    
    streamingTask = Task {
        // Check if this is a GCT query
        if let gctResponse = await processWithGCT(prompt) {
            updateLastMessage(with: gctResponse)
            isResponding = false
            return
        }
        
        // Continue with normal Apple Intelligence processing
        do {
            if session == nil { 
                session = LanguageModelSession.createGCTEnhancedSession() 
            }
            // ... rest of the existing code
        }
    }
}
```

## API Endpoints

### Query Processing
`POST /api/apple-intelligence/query`
```json
{
  "query": "Check my coherence",
  "user_id": "apple_user"
}
```

Response:
```json
{
  "success": true,
  "response": "Your current coherence is good (2.87/4.0)...",
  "type": "coherence_check",
  "data": { /* coherence profile */ }
}
```

### System Prompt
`GET /api/apple-intelligence/system-prompt`

Returns the system prompt for Apple Intelligence to understand GCT concepts.

## Supported Query Types

1. **Coherence Check**
   - "Check my coherence"
   - "How's my wellness balance?"
   - "Analyze my current state"

2. **Recovery Plans**
   - "Help me improve my coherence"
   - "I need a recovery plan"
   - "How can I boost my wellness?"

3. **Communication Analysis**
   - "Analyze this message: [text]"
   - "Check my communication style"
   - "Review my text coherence"

4. **Temporal Patterns**
   - "What are my daily patterns?"
   - "When am I most coherent?"
   - "Show my weekly trends"

5. **Group Analysis**
   - "Check our team coherence"
   - "Analyze family dynamics"
   - "Group wellness assessment"

## Example Integration Flow

1. User asks: "How's my coherence today?"
2. Apple Intelligence Chat detects GCT-related query
3. Swift app calls GCT backend API
4. Backend returns coherence analysis
5. Response formatted and shown in chat

## SwiftUI Components

The integration includes custom SwiftUI components:

- `GCTCoherenceView`: Displays coherence profile
- `VariableRow`: Shows individual GCT variables
- `GCTIntegrationManager`: Handles API communication

## Best Practices

1. **Caching**: Cache coherence profiles locally for offline access
2. **Error Handling**: Gracefully handle backend unavailability
3. **Privacy**: Store user IDs securely in Keychain
4. **Performance**: Use GPU-accelerated endpoints for batch operations

## Testing

Test the integration with these queries:
```
"Check my coherence"
"I'm feeling unbalanced, help me"
"Analyze my communication patterns"
"What time of day am I most coherent?"
"Create a recovery plan for me"
```

## Troubleshooting

- **Connection Failed**: Ensure backend is running on port 5001
- **No Profile Found**: User needs to complete initial assessment
- **Slow Response**: Check if GPU acceleration is enabled

## Future Enhancements

- Widget support for coherence tracking
- Siri Shortcuts integration
- Watch app companion
- Live Activities for coherence monitoring