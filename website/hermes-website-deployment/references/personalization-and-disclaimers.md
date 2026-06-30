# Personalization and Disclaimer Guidelines for Hermes Agent Website

Based on session updates where user requested:
1. Clear disclaimer stating the site is not an official Hermes site
2. Integration of personal avatar image
3. Visual enhancements to "jazz up" the site

## Disclaimer Requirements

Add a prominent disclaimer at the top of all main pages stating:
> **Disclaimer**: This website showcases my personal experience with the Hermes Agent AI assistant based on our interactions and my growing skill set. It is not an official Hermes Agent website or documentation.

This disclaimer should:
- Be visually distinct (using blockquote or alert styling)
- Appear before the main content
- Be present on index.html and other primary pages

## Avatar Integration

To include a personal avatar:
1. Place the avatar image in `docs/assets/images/` directory
2. Reference it in markdown using: `![Agent Blue Avatar](/assets/images/agent-blue-avatar.png)`
3. Recommended dimensions: square image, minimum 400x400px
4. The avatar from `~/Pictures/AgentBlue.png` was successfully used in this implementation

## Visual Enhancement Guidelines

When "jazzing up" the site as requested:
1. Use thematic placeholder images to illustrate concepts
2. Suggested image sources:
   - Feature icons: Multi-tool Integration, Skill System, Automation
   - Skills Categories visualization
   - Activity timeline
   - Getting started guide
   - Contribution workflow
   - Documentation standards
3. All placeholder images can be replaced with custom graphics later
4. Use descriptive alt text for all images

## Implementation Example

From the updated index.md:
```markdown
# Hermes Agent Website

> **Disclaimer**: This website showcases my personal experience with the Hermes Agent AI assistant based on our interactions and my growing skill set. It is not an official Hermes Agent website or documentation.

![Agent Blue Avatar](/assets/images/agent-blue-avatar.png)

[Rest of content...]
```

## Verification

After updates, verify that:
1. The disclaimer is visible and properly formatted
2. The avatar image loads correctly
3. Placeholder images enhance visual appeal without distracting from content
4. All images have appropriate alt text for accessibility