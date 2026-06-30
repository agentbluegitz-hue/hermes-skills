# Zensical Configuration Reference

Based on the zensical.toml file in the Hermes Agent website repository.

## Key Configuration Sections

### Project Metadata
- `site_name`: "Hermes Agent Website"
- `site_description`: "Showcasing the capabilities, skills, and activities of the Hermes Agent AI assistant"
- `site_author`: "Agent Blue"
- `site_url`: "https://agent-blue.gitz.us/"
- `copyright`: Copyright notice for Hermes Agent Project

### Theme Configuration
- Uses Zensical theme with slate and default color schemes
- Font: Inter (text), Jetbrains Mono (code)
- Language: en (English)
- Features enabled: announce.dismiss, content.code.annotate, content.code.copy, content.code.select, content.footnote.tooltips, content.tabs.link, content.tooltips, navigation.path, navigation.top, navigation.tracking, search.highlight

### Markdown Extensions
- Enabled extensions: abbr, admonition, attr_list, def_list, footnotes, md_in_html, toc (with permalink)
- pymdownx extensions: arithmatex, betterem, caret, details, emoji, highlight, inlinehilite, keys, magiclink, mark, smartsymbols, superfences (with mermaid support), tabbed, tasklist, tilde

## Build Process
The site is built using the `zensical build` command which:
1. Reads configuration from zensical.toml
2. Processes Markdown files in the docs/ directory
3. Applies the selected theme and extensions
4. Outputs static HTML, CSS, and JavaScript files to the site/ directory

## Customization Options
- Additional CSS can be added via extra_css setting
- Additional JavaScript can be added via extra_javascript setting
- Custom templates can be placed in an overrides/ directory
- Favicon can be set via favicon setting