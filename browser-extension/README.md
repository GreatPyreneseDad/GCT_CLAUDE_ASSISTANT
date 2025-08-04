# GCT Coherence Monitor - Browser Extension

Real-time coherence evaluation for LLM outputs using Grounded Coherence Theory (GCT).

## Features

- **Real-time Analysis**: Monitors LLM responses as they appear on the page
- **Multi-dimensional Scoring**: Evaluates coherence across 4 GCT dimensions:
  - Ψ (Psi) - Internal Consistency
  - ρ (Rho) - Wisdom Integration
  - q - Actionability/Practical Value
  - f - Social/Relational Awareness
- **Floating Widget**: Non-intrusive display with coherence metrics
- **Platform Support**: Works with ChatGPT, Claude, Gemini, Bard, Poe, and Perplexity
- **History Tracking**: Visualizes coherence trends over conversation
- **API Integration**: Optional connection to backend for advanced analysis

## Installation

### Development Setup

1. Install dependencies:
```bash
cd browser-extension
npm install
```

2. Build the extension:
```bash
npm run build
```

3. Load in Chrome/Edge:
   - Navigate to `chrome://extensions/`
   - Enable "Developer mode"
   - Click "Load unpacked"
   - Select the `dist` folder

4. Load in Firefox:
   - Navigate to `about:debugging`
   - Click "This Firefox"
   - Click "Load Temporary Add-on"
   - Select the `manifest.json` file in `dist`

### Production Build

```bash
npm run pack
```

This creates a `gct-monitor.zip` file ready for submission to browser stores.

## Usage

1. **Enable Monitoring**: Click the extension icon and ensure monitoring is enabled
2. **Visit LLM Platform**: Navigate to any supported LLM website
3. **Start Chatting**: The extension automatically analyzes LLM responses
4. **View Metrics**: A floating widget shows real-time coherence scores
5. **Check History**: Click the extension icon to see conversation trends

## Architecture

```
browser-extension/
├── src/
│   ├── background/        # Service worker
│   ├── content/          # Content scripts and widget
│   ├── popup/            # Extension popup UI
│   └── utils/            # Coherence analyzer
├── public/               # Static assets
└── dist/                 # Built extension
```

## API Integration

The extension can optionally connect to your local GCT backend for enhanced analysis:

1. Start the backend server:
```bash
cd ../backend
python gct_backend.py
```

2. The extension will automatically use the API when available at `http://localhost:5001`

## Coherence Metrics

### Overall Score (0-100%)
Composite score using the GCT formula: `C = ψ + (ρ × ψ) + q + (f × ψ)`

### Dimension Scores
- **Consistency (Ψ)**: Logical flow, contradiction detection, structural coherence
- **Wisdom (ρ)**: Learning references, nuanced thinking, experience integration
- **Action (q)**: Practical advice, concrete steps, solution-oriented
- **Social (f)**: Empathy, relational awareness, inclusive language

### Trajectory Analysis
- **Improving**: Coherence trending upward
- **Stable**: Consistent coherence level
- **Declining**: Coherence trending downward

## Privacy

- All analysis happens locally in your browser
- No data is sent to external servers unless API integration is enabled
- History is stored locally and can be cleared anytime

## Development

### Watch Mode
```bash
npm run watch
```

### Testing
The extension includes test scenarios for each supported platform. Enable developer mode to access the test panel.

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details