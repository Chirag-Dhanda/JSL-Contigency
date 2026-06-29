import os, re
files = ['modules/governance/models.py', 'modules/knowledge_intake/models.py', 'modules/media_platform/models.py']
for f in files:
    path = os.path.join(r'd:\JSL Contigency\backend', f)
    with open(path, 'r', encoding='utf-8') as f_in:
        content = f_in.read()
    content = re.sub(r'from datetime import datetime\b', r'from datetime import datetime, timezone', content)
    content = content.replace('datetime.utcnow()', 'datetime.now(timezone.utc)')
    with open(path, 'w', encoding='utf-8') as f_out:
        f_out.write(content)
