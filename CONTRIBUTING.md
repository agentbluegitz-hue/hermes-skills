# Contributing to Hermes Skills

Thank you for considering contributing to the Hermes Agent skills repository! This document outlines the process and guidelines for contributing.

## 🤝 How to Contribute

### 1. Fork the Repository
- Fork this repository to your own GitHub account
- Clone your fork locally:
  ```bash
  git clone https://github.com/your-username/hermes-skills.git
  cd hermes-skills
  ```

### 2. Create a Branch
- Create a new branch for your changes:
  ```bash
  git checkout -b feature/your-feature-name
  ```
  or
  ```bash
  git checkout -b fix/issue-description
  ```

### 3. Make Your Changes
- Follow the skill authoring guidelines below
- Ensure your changes are focused and well-documented
- Test your changes if they include executable components

### 4. Commit Your Changes
- Write clear, descriptive commit messages:
  ```bash
  git commit -m "Add: new skill for X"
  ```
  or
  ```bash
  git commit -m "Fix: resolve issue with Y in Z skill"
  ```

### 5. Push and Create Pull Request
- Push your branch to your fork:
  ```bash
  git push origin feature/your-feature-name
  ```
- Go to the original repository and click "New Pull Request"
- Provide a clear description of what your changes accomplish

## 📝 Skill Authoring Guidelines

When creating or updating skills, please follow these guidelines:

### Skill Structure
Each skill should have:
- **SKILL.md**: Main skill documentation with YAML frontmatter and markdown body
- **Optional**: references/, templates/, scripts/ directories for supporting files

### SKILL.md Format
```yaml
---
name: skill-name
description: Brief description of what the skill enables
category: optional-category-for-organization
---
```

### Content Requirements
1. **Trigger Conditions**: Clearly state when this skill should be used
2. **Numbered Steps**: Provide exact commands and procedures
3. **Pitfalls Section**: Document common issues and how to avoid them
4. **Verification Steps**: How to confirm the skill worked correctly
5. **Examples**: Concrete examples of usage when helpful

### Best Practices
- **Focus**: One skill per distinct, recurring task type
- **Clarity**: Use clear, action-oriented language
- **Conciseness**: Be thorough but avoid unnecessary verbosity
- **Tool Usage**: Prefer Hermes built-in tools over raw shell commands when possible
- **Safety**: Never store credentials or sensitive information in skills
- **Atomic Operations**: Make skills idempotent when possible

## 🔍 Review Process

All contributions will be reviewed based on:
- Relevance to Hermes Agent use cases
- Clarity and completeness of documentation
- Adherence to best practices
- Potential usefulness to the Hermes community

## 📄 License

By contributing to this repository, you agree that your contributions will be licensed under the same terms as the existing skills.

## ❓ Questions?

If you have questions about contributing, please open an issue or reach out through the Hermes community channels.

Thank you for helping improve Hermes Agent for everyone!