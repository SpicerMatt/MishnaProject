import os

file_path = 'index.html'
new_content_path = 'new_mark_masechet.js'

with open(new_content_path, 'r', encoding='utf-8') as f:
    new_func_content = f.read()

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
in_function = False
replaced = False

for line in lines:
    if 'function markMasechet(seder, masechet) {' in line:
        in_function = True
        new_lines.append(new_func_content + '\n')
        replaced = True
        continue
    
    if in_function:
        # We assume the function ends with a line that has only indentation and '}'
        # or we can count braces. But looking at the file, the function ends before 'function editMishnaCount'
        if 'function editMishnaCount' in line:
            in_function = False
            new_lines.append(line)
        elif line.strip() == '}' and lines[lines.index(line)+1].strip() == '':
             # This is risky. Let's just skip until we hit the next function or a known end point.
             pass
        # Better approach: Count braces? No, too complex for regex-ish replacement.
        # Let's rely on the fact that the next function starts with 'function editMishnaCount'
        # But wait, there might be empty lines between them.
        
        # Let's look at the previous view_file.
        # 904:         }
        # 905: 
        # 906:         function editMishnaCount(chapterId, currentCount) {
        
        # So if we see 'function editMishnaCount', we are definitely out.
        # But we need to make sure we don't duplicate the closing brace if we inserted the whole function.
        # The new content HAS the closing brace.
        pass
    else:
        new_lines.append(line)

# Wait, the above logic is slightly flawed because I need to know when to STOP skipping.
# I should skip until I see the next function definition, OR until I see the closing brace of THIS function.
# But since I'm replacing the WHOLE function including the closing brace, I should skip everything from the start line
# until the line BEFORE the next function? Or until the closing brace?

# Let's try a different approach.
# Find start index.
# Find end index (line with '}' before 'function editMishnaCount').

start_idx = -1
end_idx = -1

for i, line in enumerate(lines):
    if 'function markMasechet(seder, masechet) {' in line:
        start_idx = i
    if start_idx != -1 and 'function editMishnaCount' in line:
        end_idx = i - 1 # The line before is likely empty or the closing brace
        break

# Refine end_idx: backtrack from editMishnaCount to find the closing brace of markMasechet
if end_idx != -1:
    # Check lines[end_idx]
    while end_idx > start_idx and '}' not in lines[end_idx]:
        end_idx -= 1
    # Now end_idx points to the line with '}'
    
    # Construct new lines
    final_lines = lines[:start_idx] + [new_func_content + '\n'] + lines[end_idx+1:]
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(final_lines)
    print("Successfully replaced function.")
else:
    print("Could not find function boundaries.")

