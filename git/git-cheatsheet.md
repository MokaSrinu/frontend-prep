# 🚀 Git Commands Cheat Sheet

> **A comprehensive guide to essential Git commands for developers**

*Reference: [10 Best git commands to know and use](https://appwrite.io/blog/post/10-git-commands-you-should-start-using?ref=dailydev)*

---

## 📋 Table of Contents

1. [Creating Snapshots](#creating-snapshots)
2. [Browsing History](#browsing-history)
3. [Branching & Merging](#branching--merging)
4. [Collaboration](#collaboration)
5. [Rewriting History](#rewriting-history)

---

## Creating Snapshots

### 🔧 Initializing a Repository
```bash
git init
```

### 📁 Staging Files
```bash
git add file1.js                    # Stages a single file
git add file1.js file2.js           # Stages multiple files
git add *.js                        # Stages with a pattern
git add .                           # Stages the current directory and all its content
```

### 📊 Viewing the Status
```bash
git status                          # Full status
git status -s                       # Short status
```

### 💾 Committing the Staged Files
```bash
git commit -m "Message"             # Commits with a one-line message
git commit                          # Opens the default editor to type a long message
```

### ⚡ Skipping the Staging Area
```bash
git commit -am "Message"            # Add and commit in one command
```

### 🗑️ Removing Files
```bash
git rm file1.js                     # Removes from working directory and staging area
git rm --cached file1.js            # Removes from staging area only
```

### 📝 Renaming or Moving Files
```bash
git mv file1.js file1.txt           # Rename/move files
```

### 👁️ Viewing the Staged/Unstaged Changes
```bash
git diff                            # Shows unstaged changes
git diff --staged                   # Shows staged changes
git diff --cached                   # Same as the above
```

### 📜 Viewing the History
```bash
git log                             # Full history
git log --oneline                   # Summary
git log --reverse                   # Lists commits from oldest to newest
```

### 🔍 Viewing a Commit
```bash
git show 921a2ff                    # Shows the given commit
git show HEAD                       # Shows the last commit
git show HEAD~2                     # Two steps before the last commit
git show HEAD:file.js               # Shows the version of file.js stored in the last commit
```

### ↩️ Unstaging Files (Undoing git add)
```bash
git restore --staged file.js        # Copies the last version of file.js from repo to index
```

### 🔄 Discarding Local Changes
```bash
git restore file.js                 # Copies file.js from index to working directory
git restore file1.js file2.js       # Restores multiple files in working directory
git restore .                       # Discards all local changes (except untracked files)
git clean -fd                       # Removes all untracked files
```

### ⏮️ Restoring an Earlier Version of a File
```bash
git restore --source=HEAD~2 file.js # Restore file from 2 commits ago
```

---

## Browsing History

### 📊 Viewing the History
```bash
git log --stat                      # Shows the list of modified files
git log --patch                     # Shows the actual changes (patches)
```

### 🔍 Filtering the History
```bash
git log -3                          # Shows the last 3 entries
git log --author="Mosh"             # Filter by author
git log --before="2020-08-17"       # Filter by date (before)
git log --after="one week ago"      # Filter by date (after)
git log --grep="GUI"                # Commits with "GUI" in their message
git log -S"GUI"                     # Commits with "GUI" in their patches
git log hash1..hash2                # Range of commits
git log file.txt                    # Commits that touched file.txt
```

### 🎨 Formatting the Log Output
```bash
git log --pretty=format:"%an committed %H"
```

### 🔗 Creating an Alias
```bash
git config --global alias.lg "log --oneline"
```

### 👀 Viewing a Commit
```bash
git show HEAD~2                     # Show commit details
git show HEAD~2:file1.txt           # Shows the version of file stored in this commit
```

### ⚖️ Comparing Commits
```bash
git diff HEAD~2 HEAD                # Shows changes between two commits
git diff HEAD~2 HEAD file.txt       # Changes to file.txt only
```

### 🚪 Checking Out a Commit
```bash
git checkout dad47ed                # Checks out the given commit
git checkout master                 # Checks out the master branch
```

### 🐛 Finding a Bad Commit
```bash
git bisect start                    # Start bisect session
git bisect bad                      # Marks the current commit as bad
git bisect good ca49180             # Marks the given commit as good
git bisect reset                    # Terminates the bisect session
```

### 👥 Finding Contributors
```bash
git shortlog                        # Show contributors summary
```

### 📄 Viewing the History of a File
```bash
git log file.txt                    # Shows commits that touched file.txt
git log --stat file.txt             # Shows statistics for file.txt
git log --patch file.txt            # Shows patches applied to file.txt
```

### 👤 Finding the Author of Lines
```bash
git blame file.txt                  # Shows the author of each line in file.txt
```

### 🏷️ Tagging
```bash
git tag v1.0                        # Tags the last commit as v1.0
git tag v1.0 5e7a828                # Tags an earlier commit
git tag                             # Lists all tags
git tag -d v1.0                     # Deletes the given tag
```

---

## Branching & Merging

### 🌿 Managing Branches
```bash
git branch bugfix                   # Creates a new branch called bugfix
git checkout bugfix                 # Switches to the bugfix branch
git switch bugfix                   # Same as above (newer syntax)
git switch -C bugfix                # Creates and switches
git branch -d bugfix                # Deletes the bugfix branch
```

### ⚖️ Comparing Branches
```bash
git log master..bugfix              # Lists commits in bugfix branch not in master
git diff master..bugfix             # Shows summary of changes
```

### 📦 Stashing
```bash
git stash push -m "New tax rules"   # Creates a new stash
git stash list                      # Lists all stashes
git stash show stash@{1}            # Shows the given stash
git stash show 1                    # Shortcut for stash@{1}
git stash apply 1                   # Applies the given stash to working dir
git stash drop 1                    # Deletes the given stash
git stash clear                     # Deletes all stashes
```

### 🔀 Merging
```bash
git merge bugfix                    # Merges bugfix branch into current branch
git merge --no-ff bugfix            # Creates a merge commit even if FF is possible
git merge --squash bugfix           # Performs a squash merge
git merge --abort                   # Aborts the merge
```

### 👁️ Viewing the Merged Branches
```bash
git branch --merged                 # Shows merged branches
git branch --no-merged              # Shows unmerged branches
```

### 🔄 Rebasing
```bash
git rebase master                   # Changes the base of the current branch
```

### 🍒 Cherry Picking
```bash
git cherry-pick dad47ed             # Applies the given commit on current branch
```

---

## Collaboration

### 📥 Cloning a Repository
```bash
git clone url                       # Clone a remote repository
```

### 🔄 Syncing with Remotes
```bash
git fetch origin master             # Fetches master from origin
git fetch origin                    # Fetches all objects from origin
git fetch                           # Shortcut for "git fetch origin"
git pull                            # Fetch + merge
git push origin master              # Pushes master to origin
git push                            # Shortcut for "git push origin master"
```

### 🏷️ Sharing Tags
```bash
git push origin v1.0                # Pushes tag v1.0 to origin
git push origin --delete v1.0       # Removes tag from origin
```

### 🌿 Sharing Branches
```bash
git branch -r                       # Shows remote tracking branches
git branch -vv                      # Shows local & remote tracking branches
git push -u origin bugfix           # Pushes bugfix to origin
git push -d origin bugfix           # Removes bugfix from origin
```

### 🔗 Managing Remotes
```bash
git remote                          # Shows remote repos
git remote add upstream url         # Adds a new remote called upstream
git remote rm upstream              # Removes upstream remote
```

---

## Rewriting History

### ↩️ Undoing Commits
```bash
git reset --soft HEAD^              # Removes last commit, keeps changes staged
git reset --mixed HEAD^             # Unstages the changes as well
git reset --hard HEAD^              # Discards local changes
```

### 🔄 Reverting Commits
```bash
git revert 72856ea                  # Reverts the given commit
git revert HEAD~3..                 # Reverts the last three commits
git revert --no-commit HEAD~3..     # Reverts without auto-committing
```

### 🔍 Recovering Lost Commits
```bash
git reflog                          # Shows the history of HEAD
git reflog show bugfix              # Shows the history of bugfix pointer
```

### ✏️ Amending the Last Commit
```bash
git commit --amend                  # Modify the last commit
```

### 🛠️ Interactive Rebasing
```bash
git rebase -i HEAD~5                # Interactive rebase for last 5 commits
```

---

## 💡 Pro Tips

### 🎯 Best Practices
- **Commit often** with meaningful messages
- **Use branches** for features and bug fixes
- **Pull before push** to avoid conflicts
- **Review changes** before committing with `git diff`
- **Use `.gitignore`** for files you don't want to track

### ⚡ Useful Aliases
```bash
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.lg "log --oneline --graph --all"
```

### 🔧 Configuration
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
git config --global core.editor "code --wait"  # Use VS Code as editor
```

### 🚨 Emergency Commands
```bash
git stash                           # Quickly save work in progress
git checkout -- .                  # Discard all local changes
git clean -fd                       # Remove untracked files and directories
git reset --hard HEAD               # Reset to last commit (destructive!)
```

---

## 🎯 Quick Reference Summary

| Command | Description |
|---------|-------------|
| `git status` | Check working directory status |
| `git add .` | Stage all changes |
| `git commit -m "message"` | Commit staged changes |
| `git push` | Push to remote repository |
| `git pull` | Pull from remote repository |
| `git branch` | List branches |
| `git checkout -b branch-name` | Create and switch to new branch |
| `git merge branch-name` | Merge branch into current branch |
| `git log --oneline` | View commit history (compact) |
| `git diff` | Show unstaged changes |

---

**Remember**: Git is powerful but can be dangerous. Always make sure you understand what a command does before running it, especially destructive commands like `reset --hard` or `clean -fd`.

**Happy coding! 🚀**
