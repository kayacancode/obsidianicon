import os
import yaml
import re

def process_obsidian_vault(vault_path):
    """
    Scan all .md files in the vault and:
    - Add icon: LiBookmark if there's a non-empty 'Quality Score' and no icon
    - Remove icon: LiBookmark if 'Quality Score' is empty or 0
    """
    updated_count = 0
    removed_count = 0
    
    for root, dirs, files in os.walk(vault_path):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Check if file has frontmatter
                    if content.startswith('---\n'):
                        parts = content.split('---\n', 2)
                        if len(parts) >= 3:
                            frontmatter_raw = parts[1]
                            body = parts[2]
                            
                            try:
                                frontmatter = yaml.safe_load(frontmatter_raw) or {}
                            except yaml.YAMLError:
                                print(f"Skipping {file_path} - invalid YAML")
                                continue
                            
                            has_qs = 'Quality Score' in frontmatter
                            qs_value = frontmatter.get('Quality Score')
                            has_icon = 'icon' in frontmatter
                            icon_value = frontmatter.get('icon')

                            changed = False

                            # Remove icon if QS is empty or 0
                            if has_qs and qs_value in [None, '', 0] and icon_value == 'LiBookmark':
                                del frontmatter['icon']
                                removed_count += 1
                                changed = True
                                print(f"✗ Removed bookmark icon from: {file}")

                            # Add icon if QS has value and no icon
                            elif has_qs and qs_value not in [None, '', 0] and not has_icon:
                                frontmatter['icon'] = 'LiBookmark'
                                updated_count += 1
                                changed = True
                                print(f"✓ Added bookmark icon to: {file}")

                            if changed:
                                new_frontmatter = yaml.dump(
                                    frontmatter,
                                    default_flow_style=False,
                                    allow_unicode=True
                                ).strip()
                                new_content = f"---\n{new_frontmatter}\n---\n{body}"

                                with open(file_path, 'w', encoding='utf-8') as f:
                                    f.write(new_content)
                                
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
    
    print(f"\n✅ Added icon to {updated_count} files")
    print(f"🧹 Removed icon from {removed_count} files")

# Usage
vault_path = r"/Users/kayajones/Library/Mobile Documents/iCloud~md~obsidian/Documents/Locked in"  # Change this to your vault path
process_obsidian_vault(vault_path)
