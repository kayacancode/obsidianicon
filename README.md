# Obsidian Icon Automation Script

## Note as of Jun 23rd, 2025:

The core dilemma is that Obsidian's Iconize plugin only supports assigning icons based on file paths or names using regex, as shown in your screenshots, but it cannot detect internal frontmatter properties like "quality score." This means you can't use Iconize's current features to automatically add a bookmark icon to notes based solely on their metadata content, regardless of folder or filename. As a result, you're forced to rely on external scripts or manual frontmatter edits to achieve the automation you want.

To fully automate icon assignment for all future notes based on frontmatter, enable Iconize's frontmatter support and run a file watcher script that automatically adds the icon property when the quality score property is present. This ensures every new note will display the correct icon without manual intervention.

## Current Solution

**Update:** Created the script that batch reads all your files and adds the `LiBookmark` icon to notes with a "Quality Score" property.

### What the Script Does

The `main.py` script:
- Scans all `.md` files in your Obsidian vault
- Identifies notes that have a "Quality Score" frontmatter property
- Adds `icon: LiBookmark` to those notes (if they don't already have an icon)
- Preserves all existing frontmatter and content
- Provides progress feedback during execution

### Usage

1. Update the `vault_path` variable in `main.py` to point to your Obsidian vault:
   ```python
   vault_path = r"/path/to/your/obsidian/vault"
   ```

2. Run the script:
   ```bash
   python main.py
   ```

### Requirements

- Python 3.x
- PyYAML library (`pip install pyyaml`)

## Still To Do

- **Add file watcher capability**: Implement real-time monitoring to automatically add icons to new notes as they're created with quality scores
- Consider integration with Obsidian's plugin system for seamless automation

## How It Works

The script processes frontmatter in this format:
```yaml
---
Quality Score: 8
# After processing:
icon: LiBookmark
Quality Score: 8
---
```

Files with existing `icon` properties are left unchanged to preserve manual customizations. 