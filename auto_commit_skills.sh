#!/bin/bash
# Auto-commit script for Hermes skills

# Navigate to the skills directory
cd /home/agent-blue/.hermes/skills || exit

# Check if there are any changes (excluding untracked files? we want to track new files too)
# We'll add all changes (including new and modified) and commit if there are changes to commit.

# Update the index to include all changes (including new files, deletions, modifications)
git add -A

# Check if there are any changes staged for commit
if ! git diff-index --quiet HEAD --; then
    # There are changes, so commit
    TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
    git commit -m "Auto-commit: Update skills at $TIMESTAMP"
    echo "Auto-committed skills at $TIMESTAMP"
else
    echo "No changes in skills to commit at $(date)"
fi
