import os
import yaml
import re

def is_empty_quality_score(value):
    """
    Comprehensive check for empty/meaningless quality score values
    """
    if value is None:
        return True
    if value == '':
        return True
    if value == 0:
        return True
    if value == '0':
        return True
    if isinstance(value, str) and value.strip() == '':
        return True
    if value is False:
        return True
    return False

def process_obsidian_vault(vault_path, max_changes=50):
    """
    Scan all .md files in the vault and:
    - Add icon: LiBookmark if there's a non-empty 'Quality Score' and no icon
    - Remove icon: LiBookmark if 'Quality Score' is empty or 0
    - Limit to max_changes per run to prevent Obsidian freezing
    """
    updated_count = 0
    removed_count = 0
    processed_count = 0
    total_changes = 0
    skipped_files = []
    
    print(f"🎯 Processing up to {max_changes} file changes to prevent Obsidian freezing...")
    
    for root, dirs, files in os.walk(vault_path):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                
                # Stop if we've reached the maximum changes limit
                if total_changes >= max_changes:
                    skipped_files.append(file)
                    continue
                
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

                            # Debug output for files with Quality Score OR icons
                            if has_qs or has_icon:
                                processed_count += 1
                                qs_display = f"'{qs_value}'" if qs_value is not None else "None"
                                icon_display = f"'{icon_value}'" if icon_value is not None else "None"
                                print(f"📄 {file}: QS={qs_display} (type: {type(qs_value)}), icon={icon_display}")

                            changed = False

                            # Remove icon if QS is empty using comprehensive check
                            if has_qs and is_empty_quality_score(qs_value) and icon_value == 'LiBookmark':
                                del frontmatter['icon']
                                removed_count += 1
                                total_changes += 1
                                changed = True
                                print(f"  ✗ Removed bookmark icon from: {file} (QS was: '{qs_value}') [{total_changes}/{max_changes}]")

                            # Add icon if QS has value and no icon
                            elif has_qs and not is_empty_quality_score(qs_value) and not has_icon:
                                frontmatter['icon'] = 'LiBookmark'
                                updated_count += 1
                                total_changes += 1
                                changed = True
                                print(f"  ✓ Added bookmark icon to: {file} (QS: '{qs_value}') [{total_changes}/{max_changes}]")
                            
                            # Also check for orphaned LiBookmark icons (icon exists but no Quality Score)
                            elif not has_qs and icon_value == 'LiBookmark':
                                print(f"  ⚠️  WARNING: {file} has LiBookmark icon but no Quality Score property!")

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
    
    # Summary
    print(f"\n📊 SUMMARY:")
    print(f"   Processed {processed_count} files with Quality Score or icons")
    print(f"   ✅ Added icon to {updated_count} files")
    print(f"   🧹 Removed icon from {removed_count} files")
    print(f"   🎯 Total changes: {total_changes}/{max_changes}")
    
    if skipped_files:
        print(f"\n⏭️  SKIPPED {len(skipped_files)} files to stay under {max_changes} change limit")
        print(f"   Run the script again to process remaining files:")
        for i, file in enumerate(skipped_files[:5]):  # Show first 5
            print(f"   - {file}")
        if len(skipped_files) > 5:
            print(f"   ... and {len(skipped_files) - 5} more")
        print(f"\n💡 TIP: Increase max_changes if you want to process more files per run")
    else:
        print(f"\n🎉 All files processed! No more changes needed.")

# Usage
vault_path = r"/Users/kayajones/Library/Mobile Documents/iCloud~md~obsidian/Documents/Locked in"  # Change this to your vault path
process_obsidian_vault(vault_path, max_changes=50)  # Limit to 50 changes per run
