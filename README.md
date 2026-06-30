# Hermes Agent Skills Repository

This repository contains the skills for the [Hermes Agent](https://hermes-agent.nousresearch.com/) AI assistant. Skills are reusable procedural knowledge that extend Hermes' capabilities for specific task types.

## 📁 Repository Structure

Each skill is organized in its own directory under the respective category:

```
├── autonomous-ai-agents/     # AI agent orchestration skills
│   ├── claude-code/          # Delegate to Claude Code CLI
│   ├── codex/                # Delegate to OpenAI Codex CLI  
│   ├── hermes-agent/         # Configure Hermes itself
│   └── opencode/             # Delegate to OpenCode CLI
├── computer-use/             # Desktop automation skills
├── creative/                 # Content generation (ASCII art, diagrams, etc.)
├── data-science/             # Data analysis and visualization
├── email/                    # Email management
├── github/                   # GitHub workflow automation
├── media/                    # Media processing (GIFs, audio, video)
├── mlops/                    # Machine Learning Operations
├── note-taking/              # Note taking tools (Obsidian)
├── productivity/             # Productivity apps (Airtable, Google Workspace, etc.)
├── research/                 # Academic research tools
├── smart-home/               # Smart home device control
├── social-media/             # Social media platforms
└── software-development/     # Software development practices
```

## 🔧 How Skills Work

Skills are loaded automatically when relevant to a task. They contain:
- **YAML frontmatter**: Metadata about the skill
- **Markdown body**: Detailed instructions, workflows, and best practices
- **Linked files**: Optional references, templates, and scripts

When you ask Hermes to perform a task, it will:
1. Check if any loaded skills are relevant
2. Load the most appropriate skill(s)
3. Follow the guidance provided in the skill(s)
4. Execute the task using the recommended approach

## 📖 Using This Repository

### For Users
- Skills are automatically managed by Hermes - no manual intervention needed
- To view a skill: Ask Hermes to `skill_view(name="skill-name")`
- Skills are version controlled here for backup and collaboration

### For Developers/Contributors
1. **Adding New Skills**: Create a new directory with an SKILL.md file
2. **Updating Skills**: Modify existing SKILL.md files
3. **Best Practices**:
   - Keep skills focused on specific, recurring task types
   - Include clear trigger conditions (when to use the skill)
   - Provide numbered steps with exact commands
   - Add a "pitfalls" section with common issues and solutions
   - Include verification steps to confirm success
   - Keep language clear and action-oriented

### Skill Format
See [hermes-agent-skill-authoring](./software-development/hermes-agent-skill-authoring/) for detailed guidelines on creating skills.

## 🔄 Automation

This repository is automatically updated via a cron job that:
- Runs hourly
- Commits any changes to skills
- Pushes to GitHub

Manual updates can be made with:
```bash
cd /home/agent-blue/.hermes/skills
git add .
git commit -m "Description of changes"
git push origin main
```

## 🛡️ Safety & Best Practices

- **Never store credentials** in skills - use Hermes' secure credential storage
- **Prefer built-in tools** over shell commands when possible
- **Batch independent operations** for efficiency
- **Verify results** before reporting success
- **Keep skills focused** - one skill per distinct task type
- **Update skills** when you discover better approaches or fix issues

## 🤝 Contributing

If you'd like to contribute improvements to skills:
1. Fork this repository
2. Make your changes following the skill authoring guidelines
3. Submit a pull request with a clear description of what problem your changes solve

## 📄 License

This repository contains skills for personal use with Hermes Agent. See individual skill files for any specific licensing information.

---

*Last updated: $(date)*
*Automatically maintained by Hermes Agent*