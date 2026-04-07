#!/usr/bin/env python3
import os,shutil,sys
conf_files=[]
for root,dirs,files in os.walk('.'):
    if root.startswith('./.git') or '/.git/' in root or root.startswith('./venv'):
        continue
    for f in files:
        path=os.path.join(root,f)
        if path.startswith('./.git'):
            continue
        try:
            with open(path,'r',encoding='utf-8',errors='replace') as fh:
                data=fh.read()
        except Exception:
            continue
        if '<<<<<<< ' in data and '=======' in data and '>>>>>>> ' in data:
            conf_files.append(path)

if not conf_files:
    print('No conflicted files found')
    sys.exit(0)

print('Conflicted files:')
for f in conf_files:
    print(' -', f)

for file in conf_files:
    bak = file + '.orig'
    try:
        shutil.copy(file, bak)
    except Exception as e:
        print(f'Failed to backup {file}: {e}')
        continue
    try:
        with open(file, 'r', encoding='utf-8', errors='replace') as fh:
            lines = fh.readlines()
    except Exception as e:
        print(f'Failed to read {file}: {e}')
        continue
    out = []
    i = 0
    changed = False
    while i < len(lines):
        line = lines[i]
        if line.startswith('<<<<<<<'):
            changed = True
            # keep ours (the lines after <<<<<<< up to =======)
            i += 1
            while i < len(lines) and not lines[i].startswith('======='):
                out.append(lines[i])
                i += 1
            # skip =======
            while i < len(lines) and not lines[i].startswith('>>>>>>>'):
                i += 1
            # skip the >>>>>>> line
            if i < len(lines) and lines[i].startswith('>>>>>>>'):
                i += 1
        else:
            out.append(line)
            i += 1
    if changed:
        try:
            with open(file, 'w', encoding='utf-8') as fh:
                fh.writelines(out)
            print(f'Fixed: {file} (backup at {bak})')
        except Exception as e:
            print(f'Failed to write {file}: {e}')

print('Done')
