import re
import os
import glob
import json
import argparse
import sys
from pathlib import Path

def add_index_tags(file_path, terms_data):
    """Add index tags to a Quarto markdown file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Create a backup of the original file
    with open(file_path + '.bak', 'w', encoding='utf-8') as backup:
        backup.write(content)
    
    # Split the content to separate YAML front matter
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            yaml_header = parts[0] + '---' + parts[1] + '---'
            main_content = parts[2]
        else:
            yaml_header = ''
            main_content = content
    else:
        yaml_header = ''
        main_content = content
    
    # Track changes for reporting
    terms_added = 0
    
    # Process each term in the main content only
    for term, category in terms_data.items():
        # Create escape pattern for regex
        pattern = r'\b' + re.escape(term) + r'\b'
        
        # Prepare index tag based on category
        if category:
            index_tag = f"\\\\index{{{category}!{term}}}"
        else:
            index_tag = f"\\\\index{{{term}}}"
        
        # Check if content already has index tag for this term
        # Use double backslash in the string to search for \index
        if f"\\index{{{term}}}" not in main_content and (not category or f"\\index{{{category}!{term}}}" not in main_content):
            # Find first occurrence and add the tag using a function for replacement
            def add_tag(match):
                return match.group(0) + index_tag.replace("\\\\", "\\")
                
            new_content = re.sub(pattern, add_tag, main_content, count=1, flags=re.IGNORECASE)
            if new_content != main_content:
                main_content = new_content
                terms_added += 1
    
    # Reassemble the document
    modified_content = yaml_header + main_content
    
    # Write the modified content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(modified_content)
    
    return terms_added

def load_terms(terms_file):
    """Load terms and their categories from a JSON file."""
    try:
        with open(terms_file, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: Terms file '{terms_file}' not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Terms file '{terms_file}' is not valid JSON.")
        return {}

def create_sample_terms_file(terms_file):
    """Create a sample terms file if none exists."""
    sample_terms = {
        "artificial intelligence": "AI concepts",
        "large language models": "AI concepts",
        "enhancement": "human-AI relationship",
        "human judgment": "human-AI relationship",
        "Heidegger": "philosophy",
        "being-in-the-world": "philosophy!Heidegger",
        "healthcare": "",
        "investment management": "",
        "Beethoven's Tenth Symphony": ""
    }
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(terms_file), exist_ok=True)
    
    with open(terms_file, 'w', encoding='utf-8') as file:
        json.dump(sample_terms, file, indent=2)
    
    print(f"Created sample terms file '{terms_file}'. Please edit it and run the script again.")

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Add index tags to Quarto markdown files.')
    parser.add_argument('--terms', '-t', default='index_terms.json',
                        help='Path to the JSON file containing index terms (default: index_terms.json)')
    parser.add_argument('--dir', '-d', default='.',
                        help='Directory containing Quarto files to process (default: current directory)')
    parser.add_argument('--create-sample', '-c', action='store_true',
                        help='Create a sample terms file if none exists')
    parser.add_argument('--recursive', '-r', action='store_true',
                        help='Process Quarto files in subdirectories recursively')
    
    args = parser.parse_args()
    
    # Make paths absolute
    terms_file = os.path.abspath(args.terms)
    qmd_dir = os.path.abspath(args.dir)
    
    # Check if terms file exists, create sample if requested
    if not os.path.exists(terms_file):
        if args.create_sample:
            create_sample_terms_file(terms_file)
            return
        else:
            print(f"Error: Terms file '{terms_file}' not found. Use --create-sample to create one.")
            return
    
    # Load terms
    terms_data = load_terms(terms_file)
    if not terms_data:
        return
    
    # Determine which files to process
    if args.recursive:
        file_pattern = os.path.join(qmd_dir, '**', '*.qmd')
        qmd_files = glob.glob(file_pattern, recursive=True)
    else:
        file_pattern = os.path.join(qmd_dir, '*.qmd')
        qmd_files = glob.glob(file_pattern)
    
    # Process the files
    processed_count = 0
    terms_added_total = 0
    
    for file_path in qmd_files:
        print(f"Processing {os.path.relpath(file_path, qmd_dir)}...")
        terms_added = add_index_tags(file_path, terms_data)
        if terms_added > 0:
            processed_count += 1
            terms_added_total += terms_added
            print(f"  Added {terms_added} index tags")
        else:
            print("  No new tags added")
    
    print(f"\nDone! Added {terms_added_total} index tags to {processed_count} files.")
    print(f"Processed {len(qmd_files)} total files using {len(terms_data)} terms.")

if __name__ == "__main__":
    main()