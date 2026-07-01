---
name: obsidian
description: Read, search, create, and edit notes in the Obsidian vault.
platforms: [linux, macos, windows]
---

# Obsidian Vault

Use this skill for **filesystem‑first** Obsidian vault work: reading notes, listing notes, searching note files, creating notes, appending content, and adding wikilinks.

---

## Vault path

1. Resolve the vault location **before** calling any file‑tool.  
2. The conventional environment variable is `OBSIDIAN_VAULT_PATH`.  
   *Example:* `${HERMES_HOME:-~/.hermes}/.env` may export it.  
3. If the variable is **unset**, fall back to `~/Documents/Obsidian Vault`.

> **Important** – File tools (`read_file`, `write_file`, `patch`, `search_files`) **do not expand shell variables**.  
> Pass a **concrete absolute path** (no `$` or `~`).

If you need to discover the path, you may temporarily use the `terminal` tool (e.g., `echo $OBSIDIAN_VAULT_PATH` or `ls "$HOME/Documents/Obsidian Vault"`). Once you have the absolute path, switch back to file tools.

---

## Read a note

```json
{
  "tool": "read_file",
  "path": "/absolute/path/to/Obsidian Vault/Notes/Meeting.md",
  "page": 1,
  "lines_per_page": 40
}
```

`read_file` returns the file contents with line numbers and pagination, which is safer than a raw `cat`.

---

## List notes

```json
{
  "tool": "search_files",
  "target": "files",
  "path": "/absolute/path/to/Obsidian Vault",
  "pattern": "*.md"
}
```

* Use `target: "files"` to list filenames.  
* Change `pattern` to narrow the list (e.g., `"Projects/*.md"` to list only notes inside *Projects*).

---

## Search

### By filename

```json
{
  "tool": "search_files",
  "target": "files",
  "path": "/absolute/path/to/Obsidian Vault",
  "pattern": "*project*"
}
```

### By content

```json
{
  "tool": "search_files",
  "target": "content",
  "path": "/absolute/path/to/Obsidian Vault",
  "file_glob": "*.md",
  "pattern": "TODO|FIXME"
}
```

*`pattern`* is a regular expression applied to file contents.  
Add `file_glob` to restrict the search to markdown files.

---

## Create a note

```json
{
  "tool": "write_file",
  "path": "/absolute/path/to/Obsidian Vault/Notes/New Idea.md",
  "content": "# New Idea\n\n- description: ...\n- links: [[Related Note]]\n"
}
```

`write_file` creates the file (or overwrites it) and returns a structured result, avoiding shell‑quoting pitfalls.

---

## Append to a note

### Preferred (stable anchor)

1. **Read** the note to locate an anchor (e.g., a heading).  
2. **Patch** the file, inserting new content after the anchor.

```json
{
  "tool": "patch",
  "path": "/absolute/path/to/Obsidian Vault/Notes/Journal.md",
  "anchor": "## 2024‑06‑30",
  "content": "\n- Added reflection on the meeting.\n"
}
```

### Simple append (no reliable anchor)

If there is no stable context, a quick `terminal` command is acceptable:

```json
{
  "tool": "terminal",
  "cmd": "echo '\\n- New bullet' >> '/absolute/path/to/Obsidian Vault/Notes/Journal.md'"
}
```

When the note is short, you may also **read → modify → write** the whole file.

---

## Targeted edits

Use `patch` when you have a clear surrounding context (a heading, a list item, a code block, etc.):

```json
{
  "tool": "patch",
  "path": "/absolute/path/to/Obsidian Vault/Notes/Project Plan.md",
  "anchor": "### Milestones",
  "content": "\n- Phase 2: Prototype (due 2024‑07‑15)\n"
}
```

Avoid generic `sed`‑style rewrites; `patch` is less fragile and returns a concise diff.

---

## Wikilinks

Obsidian uses `[[Note Name]]` syntax for internal links. When creating or editing notes, embed wikilinks to connect related content:

```markdown
See also: [[Project Overview]], [[Meeting Notes/2024‑06‑30]]
```

The `write_file` or `patch` examples above already demonstrate how to insert such links.

---