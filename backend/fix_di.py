import os, re
d = r'd:\JSL Contigency\backend\modules'
for r, dirs, files in os.walk(d):
    for f in files:
        if f.endswith('.py'):
            path = os.path.join(r, f)
            with open(path, 'r', encoding='utf-8') as f_in:
                content = f_in.read()
            # Replace container.resolve("ClassName") with container.resolve(ClassName)
            content = re.sub(r'container\.resolve\(\"([A-Za-z0-9_]+)\"\)', r'container.resolve(\1)', content)
            content = re.sub(r"container\.resolve\(\'([A-Za-z0-9_]+)\'\)", r"container.resolve(\1)", content)
            with open(path, 'w', encoding='utf-8') as f_out:
                f_out.write(content)
