import os

file_path = 'index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
in_target_function = False

for line in lines:
    if 'function markMasechet(seder, masechet) {' in line:
        if not line.startswith('        '): # Check if already indented
            in_target_function = True
            
    if 'function editMishnaCount' in line:
        in_target_function = False
        
    if in_target_function:
        # Add 8 spaces if it doesn't look like it has them (heuristic)
        # Actually, the file view showed 0 indentation for the first line.
        # So we should just add 8 spaces to everything that is part of this function.
        # But wait, the inner lines had 4 spaces in the view.
        # So we need to add 8 spaces to everything?
        # Let's just prepend 8 spaces to every line in the function.
        # But we need to be careful not to double indent if I run this twice.
        # The condition `if not line.startswith('        ')` protects the start.
        # But inner lines?
        # If line 891 has 4 spaces, and I add 8, it becomes 12. Correct.
        # If line 890 has 0 spaces, and I add 8, it becomes 8. Correct.
        new_lines.append('        ' + line)
    else:
        new_lines.append(line)

    # Check for end of function to stop indenting
    # The function ends with '}' and then a newline before editMishnaCount
    # But my loop logic sets in_target_function = False AT editMishnaCount.
    # So the lines BEFORE editMishnaCount (including the closing brace) will be indented.
    # This seems correct.

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Indentation fixed.")
