# Chrome Web Store Submission Guide

## Prerequisites

1. **Google Developer Account**
   - Go to https://chrome.google.com/webstore/devconsole
   - Pay one-time $5 registration fee
   - Verify your account

## Required Assets

### 1. Icons (PNG format)
- [ ] icon16.png (16x16px)
- [ ] icon32.png (32x32px) 
- [ ] icon48.png (48x48px)
- [ ] icon128.png (128x128px)

Convert the SVG icon at `icons/icon.svg` to PNG using:
- Online tool: https://cloudconvert.com/svg-to-png
- Or Photoshop/GIMP/Preview

### 2. Screenshots (Required: 1-5 screenshots)
- Size: 1280x800 or 640x400 pixels
- Format: PNG or JPG
- Suggestions:
  - Widget showing on Claude.ai
  - Graph visualization
  - Different coherence states
  - Export functionality

### 3. Promotional Images (Optional but recommended)
- Small tile: 440x280px
- Large tile: 920x680px
- Marquee: 1400x560px

## Package the Extension

1. Create production build:
```bash
npm run build
```

2. Package for upload:
```bash
# In browser-extension directory
zip -r gct-coherence-monitor.zip dist/ icons/ manifest.json PRIVACY_POLICY.md
```

Or manually:
- Select `dist/`, `icons/`, `manifest.json`
- Create ZIP file

## Chrome Web Store Listing

### Basic Information
- **Name**: GCT Coherence Monitor
- **Short Description**: Real-time coherence analysis for AI conversations using Grounded Coherence Theory
- **Category**: Productivity or Developer Tools
- **Language**: English

### Detailed Description
Use content from `store-assets/description.md`

### Privacy Practices
- [ ] Single Purpose: "Analyze coherence of AI responses"
- [ ] Host Permissions Justification: "Required to analyze content on AI chat platforms"
- [ ] No remote code
- [ ] Data handling: "No user data is collected or transmitted"

### Additional Fields
- **Website**: Your GitHub repo URL
- **Support Email**: Your email
- **Privacy Policy URL**: Link to hosted PRIVACY_POLICY.md

## Submission Steps

1. Go to https://chrome.google.com/webstore/devconsole
2. Click "New Item"
3. Upload the ZIP file
4. Fill in all required fields
5. Upload screenshots and icons
6. Complete privacy questionnaire
7. Submit for review

## Review Process
- Initial review: 1-3 business days
- May take longer for first submission
- Check email for any requested changes

## Post-Submission

1. **Version Updates**:
   - Update version in `manifest.json`
   - Rebuild and repackage
   - Upload new ZIP in developer console

2. **Monitor Reviews**:
   - Respond to user feedback
   - Fix reported issues promptly

3. **Analytics**:
   - Track installs and usage in developer console
   - Consider adding opt-in analytics for improvement

## Tips for Approval

1. **Clear Description**: Explain what the extension does
2. **Minimal Permissions**: Only request necessary permissions
3. **Privacy Focus**: Emphasize local processing
4. **Quality Screenshots**: Show the extension in action
5. **Responsive Support**: Provide valid support email

## Marketing

After approval:
1. Share on social media
2. Post in relevant AI/developer communities
3. Create a simple landing page
4. Consider ProductHunt launch