---
name: hermes-academic-research
description: "Use Hermes Agent for academic research, literature reviews, and training material development"
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, research, academic, training, literature-review, ai-agents]
    related_skills: [hermes-agent, zotero-integration, arxiv, llm-wiki, blogwatcher]
---

# Hermes Agent for Academic Research

Leverage Hermes Agent's capabilities to enhance academic research workflows, literature reviews, and training material development. This skill builds on the core Hermes Agent functionality to provide specialized guidance for academic use cases.

## Why This Matters

Hermes Agent is particularly valuable for academic work because it combines:
- **Persistent context** across research sessions
- **Tool integration** for accessing databases, libraries, and APIs
- **Multi-agent coordination** for complex research tasks
- **Customizable workflows** through skills and configuration
- **Cross-platform availability** for seamless work across devices

## Core Academic Workflows

### 1. Literature Review Assistance
Hermes can help streamline the literature review process:

```markdown
## Literature Review Workflow with Hermes

1. **Discovery Phase**
   - Use arXiv search to find recent papers
   - Search academic databases via available MCP servers
   - Browse your Zotero library for relevant sources
   - Monitor blogs and RSS feeds for emerging research

2. **Organization Phase**
   - Tag and categorize papers in Zotero
   - Create collections for different subtopics
   - Add notes and annotations to key papers
   - Build relationship maps between related works

3. **Analysis Phase**
   - Extract key findings, methodologies, and limitations
   - Identify research gaps and contradictions
   - Track citation networks and influence patterns
   - Summarize trends over time

4. **Synthesis Phase**
   - Generate literature review outlines
   - Create comparative tables of methodologies
   - Develop conceptual frameworks from the literature
   - Write annotated bibliographies
```

### 2. Training Material Development
For creating educational content about AI agents and related topics:

```markdown
## Training Material Development Process

1. **Needs Assessment**
   - Research current training gaps and requirements
   - Survey target audience (faculty, students, staff)
   - Review existing training materials and best practices
   - Define learning objectives and outcomes

2. **Content Creation**
   - Develop slide decks and presentation materials
   - Create hands-on exercises and labs
   - Build demonstration scripts and examples
   - Generate assessment questions and rubrics

3. **Iteration & Refinement**
   - Test materials with pilot groups
   - Incorporate feedback and improve clarity
   - Update examples to reflect latest developments
   - Ensure accessibility and inclusivity

4. **Deployment & Tracking**
   - Publish materials to appropriate platforms
   - Track usage and effectiveness metrics
   - Maintain version control and update schedules
   - Collect and analyze learner feedback
```

### 3. Research Project Management
Coordinate complex research projects using Hermes' multi-agent capabilities:

```markdown
## Research Project Coordination

1. **Planning Phase**
   - Define research questions and hypotheses
   - Design methodology and experimental approach
   - Create timeline and milestone plan
   - Assign roles and responsibilities

2. **Execution Phase**
   - Spawn specialized agents for different tasks:
     * Literature search agent
     * Data collection agent
     * Analysis agent
     * Writing agent
   - Use Kanban board for task tracking
   - Set up regular check-ins and progress reviews
   - Manage data and version control

3. **Validation Phase**
   - Cross-check results between agents
   - Verify methodology implementation
   - Ensure reproducibility of experiments
   - Prepare results for dissemination

4. **Dissemination Phase**
   - Write papers and conference submissions
   - Create presentation materials
   - Develop data visualizations
   - Prepare supplementary materials
```

## Recommended Skills & Tools

### Essential Skills for Academic Work
- **`zotero-integration`**: Access and manage your reference library
- **`arxiv`**: Search and retrieve pre-print papers
- **`llm-wiki`**: Build personal knowledge bases from research
- **`blogwatcher`**: Monitor academic blogs and RSS feeds
- **`plan`**: Structure research projects and training modules
- **`test-driven-development`**: Ensure quality in code-based research
- **`requesting-code-review`**: Validate research code and implementations

### Useful Toolsets
- **`web`**: For general research and information gathering
- **`file`**: For working with papers, notes, and data files
- **`terminal`**: For running analysis scripts and commands
- **`vision`**: For analyzing figures, charts, and diagrams in papers
- **`delegation`**: For spawning specialized research agents
- **`cronjob`**: For scheduled literature searches and updates
- **`session_search`**: For finding previous research conversations

## Configuration Recommendations

### Optimal Settings for Research
```yaml
# In ~/.hermes/config.yaml
agent:
  max_turns: 150          # Allow for deep research conversations
  tool_use_enforcement: auto  # Encourage tool use when helpful
  task_completion_guidance: true  # Get help completing tasks

memory:
  memory_enabled: true    # Remember research context across sessions
  user_profile_enabled: true
  provider: ""            # Use default

delegation:
  max_concurrent_children: 3  # Run multiple research agents in parallel
  max_spawn_depth: 2        # Allow agents to spawn specialists
  reasoning_effort: medium  # Balanced reasoning for research tasks

# For working with large PDFs and documents
compression:
  enabled: true
  threshold: 0.50
  target_ratio: 0.20

# Enable useful auxiliary models
auxiliary:
  vision:
    provider: auto        # For analyzing paper figures
    model: ""
  session_search:
    provider: auto        # For finding past research discussions
    model: ""
```

### Example Research-Focused Profiles
Consider creating specialized profiles for different research activities:

1. **`research-literature`**: Optimized for paper reading and note-taking
2. **`research-writing`**: Configured for drafting and editing manuscripts
3. **`research-analysis`**: Set up for data analysis and statistical work
4. **`training-development`**: Tailored for creating educational materials

## Practical Examples

### Example 1: Literature Search Assistant
```python
# Goal: Find recent papers on AI agents in education
from hermes_tools import web_search, web_extract

def search_ai_agents_education():
    # Search arXiv for recent papers
    arxiv_results = web_search(query="AI agent education training", limit=10)
    
    # Get abstracts for promising papers
    papers = []
    for result in arxiv_results['data']['web'][:5]:
        if 'arxiv.org' in result['url']:
            abstract = web_extract(urls=[result['url']])
            papers.append({
                'title': result['title'],
                'url': result['url'],
                'abstract': abstract['results'][0]['content'] if abstract['results'] else "No abstract"
            })
    
    return papers

# Use in delegation
delegate_task(
    goal="Find and summarize recent papers on AI agents in education",
    context="Focus on papers from 2023-2024 that discuss practical implementations",
    toolsets=["web", "file"]
)
```

### Example 2: Training Material Generator
```python
# Goal: Create a training module on prompt engineering
def create_prompt_engineering_module():
    # Research current best practices
    research = web_search(query="prompt engineering best practices 2024", limit=8)
    
    # Extract key techniques
    techniques = []
    for result in research['data']['web']:
        content = web_extract(urls=[result['url']])
        # Process content to extract key points
        # (implementation depends on specific sources)
    
    # Create module structure
    module = {
        'title': 'Prompt Engineering for AI Agents',
        'learning_objectives': [
            'Understand principles of effective prompt design',
            'Learn techniques for improving agent reliability',
            'Practice creating prompts for specific use cases',
            'Evaluate and iterate on prompt effectiveness'
        ],
        'sections': [
            'Introduction to Prompt Engineering',
            'Core Principles and Techniques',
            'Advanced Strategies (Chain-of-Thought, Few-Shot)',
            'Testing and Evaluation Methods',
            'Common Pitfalls and How to Avoid Them',
            'Hands-on Practice Exercises'
        ],
        'references': research['data']['web']
    }
    
    return module
```

### Example 3: Research Project Coordinator
```python
# Goal: Coordinate a multi-agent research project on AI agent evaluation
research_plan = {
    'project_title': 'Evaluating AI Agent Effectiveness in Educational Settings',
    'research_questions': [
        'How do different AI agent architectures impact learning outcomes?',
        'What prompt strategies maximize educational effectiveness?',
        'How do students and faculty perceive and interact with AI agents?'
    ],
    'methodology': 'Mixed-methods study with quasi-experimental design',
    'phases': [
        {
            'name': 'Literature Review',
            'duration': '4 weeks',
            'deliverables': ['Annotated bibliography', 'Theoretical framework'],
            'agents': ['literature_search_agent', 'synthesis_agent']
        },
        {
            'name': 'Instrument Development',
            'duration': '3 weeks',
            'deliverables': ['Survey instruments', 'Observation protocols', 'Interview guides'],
            'agents': ['instrument_design_agent', 'validation_agent']
        },
        {
            'name': 'Data Collection',
            'duration': '6 weeks',
            'deliverables': ['Quantitative dataset', 'Qualitative transcripts', 'Interaction logs'],
            'agents': ['data_collection_agent', 'ethics_compliance_agent']
        },
        {
            'name': 'Analysis & Reporting',
            'duration': '5 weeks',
            'deliverables': ['Statistical analysis report', 'Qualitative themes paper', 'Policy recommendations'],
            'agents': ['quantitative_analysis_agent', 'qualitative_analysis_agent', 'writing_agent']
        }
    ]
}

# This could be fed into delegation to spawn appropriate agents for each phase
```

## Best Practices for Academic Use

### 1. Context Management
- Use `/goal` to set long-term research objectives
- Leverage `/compress` to manage context during long literature reviews
- Save important findings with `/save` or session export
- Use project context files (`.hermes.md`, `AGENTS.md`) for domain-specific guidance

### 2. Quality Assurance
- Implement `/requesting-code-review` for research code
- Use systematic verification approaches for findings
- Cross-check information from multiple sources
- Document your research process and decisions

### 3. Collaboration Features
- Share sessions with colleagues via `/handoff`
- Use Kanban boards for task tracking in group projects
- Set up scheduled checks with cron jobs for long-running monitoring
- Export sessions for sharing with team members

### 4. Ethical Considerations
- Be mindful of data privacy when working with sensitive research data
- Consider bias in AI-generated content and analyses
- Follow institutional guidelines for AI use in research
- Acknowledge AI assistance appropriately in publications

### Integration with Zotero (as demonstrated in session with Matt)\\n\\nDuring this session, we successfully established direct API access to Matt's Zotero library using pyzotero, demonstrating a working integration approach for academic research workflows.\\n\\n### Successful Connection Established\\n- **Credentials Verified**: User ID 6147 (username: magitz) with provided API key\\n- **Library Access**: Full read access to collections, items, notes, and attachments\\n- **Collections Discovered**: \\n  1. Regulated Data (4 items: CMMC compliance materials)\\n  2. Frontiers In AI 2021 (32 items: AI research including smart cities, AI ethics, computational creativity)\\n  3. Genome Duplication Class (23 items: plant genetics educational materials)\\n  4. Zizphus paper (76 items: microsatellite research with extensive supporting materials)\\n- **Total Items**: Approximately 135 items across all collections\\n\\n### Working Integration Approach\\nThe successful method used during this session was direct pyzotero API access, which works regardless of whether Zotero desktop is running (avoiding database lock issues):\\n\\n```python\\n# Successful connection pattern from this session\\nimport sys\\nsys.path.insert(0, '/home/agent-blue/.local/share/uv/tools/zotero-mcp-server/lib/python3.13/site-packages')\\n\\nfrom pyzotero import zotero\\n\\n# Initialize with verified credentials\\nzot = zotero.Zotero(user_id='6147', library_type='user', api_key='Wzw7Tja95VvSOhpBRwj1pNq4')\\n\\n# Verify connection\\nkey_info = zot.key_info()\\nprint(f\\\"Connected as: {key_info.get('username')} (ID: {key_info.get('userID')})\\\")\\n\\n# Access collections\\ncollections = zot.collections()\\nprint(f\\\"Found {len(collections)} collections\\\")\\n\\n# Search and retrieve items\\nsearch_results = zot.items(q='AI', limit=5)\\nfor item in search_results:\\n    data = item.get('data', {})\\n    print(f\\\"- [{data.get('itemType')}] {data.get('title', 'No title')}\\\")\\n```\\n\\n### Practical Applications Demonstrated\\n\\n#### 1. Literature Search & Discovery\\n```python\\n# Search across entire library\\npapers_on_topic = zot.items(q='machine learning education', limit=15)\\n\\n# Search within specific collection\\ncollection_items = zot.collection_items('COLLECTION_KEY')\\nfiltered_items = [item for item in collection_items if 'assessment' in item.get('data', {}).get('title', '').lower()]\\n\\n# Get recent items\\nrecent_items = zot.items(limit=10, sort='dateAdded', direction='desc')\\n```\\n\\n#### 2. Data Extraction for Analysis\\n```python\\n# Extract structured data for analysis\\ndef extract_item_data(item):\\n    data = item.get('data', {})\\n    creators = data.get('creators', [])\\n    author_str = ', '.join([\\n        f\\\"{c.get('lastName', '')}, {c.get('firstName', '')}\\\" \\n        for c in creators if c.get('lastName')\\n    ]) or 'No authors'\\n    \\n    return {\\n        'title': data.get('title', 'No title'),\\n        'authors': author_str,\\n        'publication_title': data.get('publicationTitle', ''),\\n        'date': data.get('date', ''),\\n        'item_type': data.get('itemType', 'unknown'),\\n        'tags': [tag.get('tag', '') for tag in data.get('tags', [])],\\n        'note': data.get('note', ''),\\n        'url': data.get('url', '')\\n    }\\n\\n# Process search results\\nprocessed_papers = [extract_item_data(item) for item in zot.items(q='prompt engineering', limit=10)]\\n```\\n\\n#### 3. Collection-Specific Analysis\\n```python\\n# Analyze the Frontiers In AI 2021 collection (as demonstrated)\\nai_collection_key = 'FPWTGJKS'  # From Matt's library\\nai_papers = zot.collection_items(ai_collection_key)\\n\\n# Categorize by content\\ncategories = {\\n    'AI Ethics': [],\\n    'Smart Systems': [],\\n    'Creative AI': [],\\n    'Other': []\\n}\\n\\nfor paper in ai_papers:\\n    title = paper.get('data', {}).get('title', '').lower()\\n    abstract = paper.get('data', {}).get('abstractNote', '').lower()\\n    combined_text = f\\\"{title} {abstract}\\\"\\n    \\n    if any(term in combined_text for term in ['ethic', 'bias', 'discriminat', 'fair']):\\n        categories['AI Ethics'].append(paper)\\n    elif any(term in combined_text for term in ['smart', 'iot', 'sensor', 'city', 'agriculture']):\\n        categories['Smart Systems'].append(paper)\\n    elif any(term in combined_text for term in ['creat', 'art', 'music', 'generat']):\\n        categories['Creative AI'].append(paper)\\n    else:\\n        categories['Other'].append(paper)\\n```\\n\\n### Integration with Research Workflows\\nThis working Zotero integration enables several academic research patterns:\\n\\n**Literature Review Automation**:\\n- Automatically gather and summarize papers on specific topics\\n- Extract key findings, methodologies, and limitations\\n- Generate comparative analyses across your library\\n\\n**Training Material Development**:\\n- Create reading lists from your actual research collections\\n- Generate bibliographies in multiple formats (APA, MLA, Chicago)\\n- Develop exercises based on real papers from your library\\n- Extract examples of good research practices for instructional use\\n\\n**Research Project Support**:\\n- Quickly find relevant background literature for new projects\\n- Identify gaps in your current collection\\n- Track evolution of research interests over time\\n- Build knowledge maps connecting related works\\n\\n### Advantages of This Approach\\n1. **No Database Lock Issues**: Works even when Zotero desktop is running\\n2. **Real-Time Access**: Always accesses current library state\\n3. **Full Functionality**: Access to all metadata, notes, tags, and attachments\\n4. **Programmatic Control**: Enables automated workflows and analysis\\n5. **Cross-Platform**: Works on Linux, macOS, and Windows\\n\\n### Important Lessons from Library Analysis\\n\\nDuring our analysis, we discovered an important lesson about analyzing personal research libraries that should inform future work:\\n\\n**Lesson: Initial topic modeling from small samples can miss significant domain-specific content**\\n\\nWhen we first analyzed a sample of 100 items from Matt's library using topic modeling based on titles, abstracts, and tags, we missed a substantial collection of plant phylogeny and evolution research. Subsequent targeted searches revealed:\\n\\n- **858 items** (~16.2% of the 5,292 item library) related to plant phylogeny, evolution, and botany\\n- **Core phylogenetics work** including APG classifications, plastid phylogenomics, and multigene analyses\\n- **Content spanning multiple plant groups** (bryophytes, gymnosperms, angiosperms) and methodologies (DNA barcoding, phylogenomics, molecular dating)\\n\\n### Why This Was Missed Initially\\n\\n1. **Format issues**: Many items were attachments/PDFs with generic titles like \"Full Text PDF\"\\n2. **Annotation limitations**: Numerous annotations lacked meaningful titles\\n3. **Keyword bias**: Initial topic modeling emphasized frequent terms from dominant topics (AI/ML, genomics)\\n4. **Specialized terminology**: Plant systematics uses domain-specific terms that didn't surface in top keyword lists\\n\\n### Corrected Approach: Multi-strategy Verification\\n\\nTo avoid missing significant content when analyzing research libraries:\\n\\n1. **Broad domain-specific searches**: Use targeted search terms for suspected missing domains\\n   - Example plant biology terms: ['plant phylogeny', 'plant evolution', 'phylogeny', 'evolution', 'botany', 'flora', 'vegetation', 'clade', 'cladistic', 'monophyletic', 'polyploidy', 'genome duplication', 'karyotype', 'chromosome', 'species tree', 'molecular evolution', 'adaptive evolution', 'natural selection', 'speciation', 'phylogenetic']\\n\\n2. **Collection verification**: Check existing collections for domain-relevant content to validate search strategies\\n\\n3. **Iterative refinement**: Start with broad searches, refine based on results, deduplicate across search terms\\n\\n4. **Format-aware analysis**: Distinguish between substantive items (journal articles, books, preprints) and less substantive ones (annotations, attachments)\\n\\n### Next Steps for Enhancement\\nBased on this successful demonstration, consider:\\n1. **Building Custom Research Agents**: Create specialized agents for your specific collections\\n2. **Automated Literature Monitoring**: Set up scheduled checks for new papers in your interests\\n3. **Knowledge Base Integration**: Connect Zotero extracts to personal wiki or note-taking system\\n4. **Citation Automation**: Integrate with writing tools for automatic bibliography generation\\n5. **Library Organization Assistance**: Use Hermes to help organize unfiled items into topical collections based on content analysis\\n\\nThis integration pattern provides a solid foundation for using Hermes Agent as a research assistant that learns from and enhances your personal knowledge base over time.
## Troubleshooting Common Issues

### "Database is locked" Error
- **Cause**: Zotero desktop is running and has the database open
- **Solutions**:
  1. Close Zotero desktop temporarily for direct access
  2. Use API approach instead (requires credentials)
  3. Make a read-only copy of the database for analysis
  4. Schedule database access for when Zotero is not running

### Missing Dependencies
- **pyzotero not found**: Install with `pip install pyzotero` or `uv pip install pyzotero`
- **MCP issues**: Ensure `mcp` package is installed: `pip install mcp`
- **Web search problems**: Check API keys for search providers in config

### Performance Optimization
- Limit search results when browsing large libraries
- Use specific, targeted queries rather than broad searches
- Consider exporting subsets of your library for frequent analysis
- Use caching strategies for repeated queries to the same data

## Next Steps for Implementation

1. **Start with Exploration**: Use the skills to browse your research environment
2. **Build a Small Project**: Try a focused literature search on a narrow topic
3. **Develop a Template**: Create reusable templates for common academic tasks
4. **Establish Routines**: Set up regular practices for literature monitoring and organization
5. **Share and Collaborate**: Work with colleagues to refine approaches and share best practices

This skill provides a foundation for using Hermes Agent as a research assistant that learns and adapts to your specific academic needs over time.