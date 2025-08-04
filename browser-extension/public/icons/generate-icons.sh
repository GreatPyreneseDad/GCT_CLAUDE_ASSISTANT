#!/bin/bash

# This script generates placeholder icons for the extension
# In production, replace with actual icon designs

# Create a simple SVG icon
cat > icon.svg << 'EOF'
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <rect width="128" height="128" rx="24" fill="#667eea"/>
  <path d="M64 32 L80 48 L64 64 L48 48 Z" fill="white" opacity="0.9"/>
  <path d="M64 64 L80 80 L64 96 L48 80 Z" fill="white" opacity="0.7"/>
  <circle cx="64" cy="64" r="4" fill="white"/>
</svg>
EOF

echo "Placeholder SVG icon created. Use an image editor to convert to PNG at different sizes:"
echo "- 16x16 -> icon16.png"
echo "- 32x32 -> icon32.png"  
echo "- 48x48 -> icon48.png"
echo "- 128x128 -> icon128.png"