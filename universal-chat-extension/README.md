# Universal Chat Coherence Analyzer

A Chrome extension that analyzes the quality and coherence of human-to-human conversations across any chat platform.

## Features

- **Universal Detection**: Automatically detects chat interfaces on any website
- **Real-time Analysis**: Monitors conversation quality as messages are exchanged
- **Privacy-Focused**: All analysis happens locally in your browser
- **Comprehensive Metrics**: Evaluates conversations on multiple dimensions
- **Platform Support**: Works with WhatsApp Web, Facebook Messenger, Slack, Discord, Teams, and more

## Metrics Explained

### Core GCT Dimensions (Adapted for Human Conversation)

1. **Consistency (Ψ)**: Logical flow and internal coherence
   - Checks for contradictions or backtracking
   - Rewards logical connectors and structure

2. **Contextual Relevance (ρ)**: Staying on topic
   - Analyzes topic overlap with recent messages
   - Measures how well responses relate to the conversation

3. **Engagement (q)**: Active participation
   - Detects questions and active listening phrases
   - Considers message length and effort

4. **Empathy (f)**: Emotional intelligence
   - Identifies empathetic language
   - Recognizes emotional support and understanding

### Additional Human Conversation Metrics

- **Clarity**: How clearly ideas are expressed
- **Sentiment**: Positive, negative, or neutral tone
- **Turn Balance**: Equality of participation
- **Response Time**: Appropriateness of response latency

## How It Works

1. **Automatic Detection**: The extension scans for common chat UI patterns
2. **Message Extraction**: Identifies sender, text, and timing information
3. **Real-time Analysis**: Each message is analyzed as it appears
4. **Visual Feedback**: A floating widget shows current conversation quality
5. **Data Export**: Export analysis for deeper insights

## Privacy

- **100% Local Processing**: No data leaves your browser
- **No Storage**: Conversations are not saved
- **No Tracking**: No analytics or user tracking
- **User Control**: Enable/disable at any time

## Installation

1. Clone this repository
2. Open Chrome and go to `chrome://extensions/`
3. Enable "Developer mode"
4. Click "Load unpacked" and select the extension directory

## Usage

1. Navigate to any chat platform
2. Click the extension icon
3. Click "Start Analyzing" when a chat interface is detected
4. View real-time coherence metrics in the floating widget
5. Export data for further analysis when needed

## Supported Platforms

The extension uses intelligent pattern matching to work with:
- WhatsApp Web
- Facebook Messenger
- Slack
- Discord
- Microsoft Teams
- Generic chat interfaces

## Technical Details

### Message Detection Patterns

The extension uses multiple strategies:
1. **URL-based detection**: Identifies known platforms
2. **Class name patterns**: Looks for common naming conventions
3. **Structure analysis**: Detects chat-like DOM structures

### Analysis Algorithm

- **Sliding window**: Analyzes messages in context
- **Weighted scoring**: Different metrics have different importance
- **Adaptive detection**: Learns from message patterns

## Development

### File Structure
```
universal-chat-extension/
├── manifest.json          # Extension configuration
├── content.js            # Main content script
├── background.js         # Background service worker
├── popup.html/js         # Extension popup UI
├── content.css          # Widget styles
└── icons/               # Extension icons
```

### Building

No build process required - load directly as unpacked extension.

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Future Enhancements

- [ ] Machine learning-based pattern detection
- [ ] More sophisticated topic modeling
- [ ] Conversation summary generation
- [ ] Multi-language support
- [ ] Custom metric configuration
- [ ] Integration with communication training tools

## License

MIT License - feel free to use and modify

## Acknowledgments

Based on Grounded Coherence Theory (GCT) adapted for human conversation analysis.