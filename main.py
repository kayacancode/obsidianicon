import os
import yaml
import re

def process_obsidian_vault(vault_path):
    """
    Scan all .md files in vault and add icon: TiBookmark 
    to notes that have 'quality score' but no 'icon' property
    """
    updated_count = 0
    
    for root, dirs, files in os.walk(vault_path):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Check if file has frontmatter
                    if content.startswith('---\n'):
                        # Split frontmatter and body
                        parts = content.split('---\n', 2)
                        if len(parts) >= 3:
                            frontmatter_raw = parts[1]
                            body = parts[2]
                            
                            # Parse frontmatter
                            try:
                                frontmatter = yaml.safe_load(frontmatter_raw) or {}
                            except yaml.YAMLError:
                                print(f"Skipping {file_path} - invalid YAML")
                                continue
                            
                            # Check conditions: has quality score, no icon
                            if 'Quality Score' in frontmatter and 'icon' not in frontmatter:
                                frontmatter['icon'] = 'LiBookmark'
                                
                                # Rebuild file content
                                new_frontmatter = yaml.dump(frontmatter, 
                                                           default_flow_style=False, 
                                                           allow_unicode=True).strip()
                                new_content = f"---\n{new_frontmatter}\n---\n{body}"
                                
                                # Write back to file
                                with open(file_path, 'w', encoding='utf-8') as f:
                                    f.write(new_content)
                                
                                print(f"✓ Added bookmark icon to: {file}")
                                updated_count += 1
                                
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
    
    print(f"\n🎉 Successfully updated {updated_count} files!")

# Usage
vault_path = r"/Users/kayajones/Library/Mobile Documents/iCloud~md~obsidian/Documents/brain"  # Change this to your vault path
process_obsidian_vault(vault_path)
