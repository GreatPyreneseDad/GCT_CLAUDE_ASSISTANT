// Simple script to create placeholder icons for the extension
const fs = require('fs');
const path = require('path');

// Create icons directory
const iconsDir = path.join(__dirname, 'icons');
if (!fs.existsSync(iconsDir)) {
  fs.mkdirSync(iconsDir);
}

// SVG icon with GCT theme
const svgIcon = `
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="128" height="128" rx="24" fill="url(#grad)"/>
  <text x="64" y="64" text-anchor="middle" dominant-baseline="middle" 
        fill="white" font-family="Arial, sans-serif" font-size="48" font-weight="bold">GCT</text>
  <circle cx="64" cy="90" r="4" fill="white" opacity="0.8"/>
  <circle cx="50" cy="90" r="4" fill="white" opacity="0.6"/>
  <circle cx="78" cy="90" r="4" fill="white" opacity="0.9"/>
</svg>
`;

// Save SVG
fs.writeFileSync(path.join(iconsDir, 'icon.svg'), svgIcon);

console.log('Icon created successfully!');
console.log('Note: For Chrome Web Store, you\'ll need PNG versions.');
console.log('You can convert the SVG to PNG using online tools or image editors.');
console.log('\nRequired sizes:');
console.log('- icon16.png (16x16)');
console.log('- icon32.png (32x32)');
console.log('- icon48.png (48x48)');
console.log('- icon128.png (128x128)');