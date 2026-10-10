import os
import re

skills_dir = '.agents/skills'
skills = sorted(os.listdir(skills_dir))

total_desc_chars = 0
total_desc_words = 0
total_body_chars = 0
total_body_words = 0
total_body_lines = 0

print(f"| Skill | Lines | Words (Full) | Chars (Full) | Desc Chars | Desc Words | Body Words | Body Lines |")
print(f"|---|---|---|---|---|---|---|---|")

for s in skills:
    p = os.path.join(skills_dir, s, 'SKILL.md')
    if not os.path.isfile(p):
        continue
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()
    
    parts = content.split('---', 2)
    fm = parts[1] if len(parts) >= 3 else ''
    body = parts[2] if len(parts) >= 3 else content
    
    # parse description
    lines = fm.splitlines()
    desc_lines = []
    in_desc = False
    for line in lines:
        if line.startswith('description:'):
            in_desc = True
            val = line.split('description:', 1)[1].strip()
            if val and val not in ('>-', '|-', '>', '|'):
                desc_lines.append(val)
        elif in_desc:
            if re.match(r'^[a-zA-Z0-9_-]+:', line):
                in_desc = False
            else:
                desc_lines.append(line.strip())
    desc = ' '.join(' '.join(desc_lines).split())
    
    lines_full = len(content.splitlines())
    words_full = len(content.split())
    chars_full = len(content)
    
    desc_chars = len(desc)
    desc_words = len(desc.split())
    
    body_lines = len(body.splitlines())
    body_words = len(body.split())
    body_chars = len(body)
    
    total_desc_chars += desc_chars
    total_desc_words += desc_words
    total_body_chars += body_chars
    total_body_words += body_words
    total_body_lines += body_lines
    
    print(f"| {s:22} | {lines_full:5} | {words_full:12} | {chars_full:12} | {desc_chars:10} | {desc_words:10} | {body_words:10} | {body_lines:10} |")

print(f"| **TOTAL** | - | - | - | {total_desc_chars:10} | {total_desc_words:10} | {total_body_words:10} | {total_body_lines:10} |")
