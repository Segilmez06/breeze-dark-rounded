#!/usr/bin/env python3
import os
import sys
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
THEME_DIR = os.path.join(REPO_ROOT, 'Breeze-Dark-Rounded')
INDEX_THEME = os.path.join(THEME_DIR, 'index.theme')

VALID_CONTEXTS = {
    'Actions', 'Animations', 'Applications', 'Categories', 'Devices',
    'Emblems', 'Emotes', 'MimeTypes', 'Places', 'Status', 'Stock', 'International'
}
VALID_TYPES = {'Fixed', 'Scalable', 'Threshold'}

print("=================================================================")
print("          BREEZE DARK ROUNDED - FULL THEME SCAN REPORT           ")
print("=================================================================")
print(f"Theme Path: {THEME_DIR}\n")

total_files = 0
total_regular_files = 0
total_symlinks = 0
broken_symlinks = []
absolute_symlinks = []
circular_symlinks = []
zero_byte_files = []
unexpected_files = []
corrupted_svgs = []
corrupted_pngs = []

for root, dirs, files in os.walk(THEME_DIR, followlinks=False):
    for f in files:
        total_files += 1
        path = os.path.join(root, f)
        rel_path = os.path.relpath(path, THEME_DIR)
        
        if f.startswith('.') or f.endswith('~') or f.endswith('.bak') or f.endswith('.old') or f.endswith('.orig'):
            unexpected_files.append(rel_path)

        if os.path.islink(path):
            total_symlinks += 1
            target = os.readlink(path)
            if os.path.isabs(target):
                absolute_symlinks.append((rel_path, target))
            if not os.path.exists(path):
                broken_symlinks.append((rel_path, target))
            else:
                try:
                    os.stat(path)
                except OSError as e:
                    if 'Too many levels of symbolic links' in str(e):
                        circular_symlinks.append((rel_path, target))
        else:
            total_regular_files += 1
            if os.path.getsize(path) == 0:
                zero_byte_files.append(rel_path)
            if f.endswith('.svg'):
                try:
                    with open(path, 'rb') as fp:
                        header = fp.read(1024).strip()
                        if not (b'<svg' in header or b'<?xml' in header):
                            corrupted_svgs.append((rel_path, "No svg/xml tag in header"))
                except Exception as e:
                    corrupted_svgs.append((rel_path, str(e)))
            elif f.endswith('.png'):
                try:
                    with open(path, 'rb') as fp:
                        sig = fp.read(8)
                        if sig != b'\x89PNG\r\n\x1a\n':
                            corrupted_pngs.append((rel_path, "Invalid PNG signature"))
                except Exception as e:
                    corrupted_pngs.append((rel_path, str(e)))

print("--- 1. File & Symlink Audit ---")
print(f"Total entries:       {total_files}")
print(f"Regular files:       {total_regular_files}")
print(f"Symlinks:            {total_symlinks}")
print(f"Broken symlinks:     {len(broken_symlinks)}")
print(f"Absolute symlinks:   {len(absolute_symlinks)}")
print(f"Circular symlinks:   {len(circular_symlinks)}")
print(f"0-byte files:        {len(zero_byte_files)}")
print(f"Unexpected files:    {len(unexpected_files)}")
print(f"Corrupted SVGs:      {len(corrupted_svgs)}")
print(f"Corrupted PNGs:      {len(corrupted_pngs)}")

# Scaled Directory Symlinks Audit
scaled_dir_symlinks = []
broken_dir_symlinks = []
for root, dirs, files in os.walk(THEME_DIR, followlinks=False):
    for d in dirs:
        if '@' in d:
            dpath = os.path.join(root, d)
            rel_dpath = os.path.relpath(dpath, THEME_DIR)
            if os.path.islink(dpath):
                tgt = os.readlink(dpath)
                if not os.path.exists(dpath):
                    broken_dir_symlinks.append((rel_dpath, tgt))
                else:
                    scaled_dir_symlinks.append((rel_dpath, tgt))

print("\n--- 2. Scaled Directory Symlinks Audit (@2x, @3x) ---")
print(f"Total scaled directory symlinks: {len(scaled_dir_symlinks)}")
print(f"Broken scaled directory symlinks: {len(broken_dir_symlinks)}")

# index.theme Audit
print("\n--- 3. index.theme Specification & Directory Sync ---")
with open(INDEX_THEME, 'r') as f:
    content = f.read()

dirs_m = re.search(r'^Directories=(.*)$', content, re.MULTILINE)
scaled_dirs_m = re.search(r'^ScaledDirectories=(.*)$', content, re.MULTILINE)

declared_dirs = set(dirs_m.group(1).split(',')) if dirs_m and dirs_m.group(1) else set()
declared_scaled_dirs = set(scaled_dirs_m.group(1).split(',')) if scaled_dirs_m and scaled_dirs_m.group(1) else set()

actual_dirs = set()
for root, dirs, files in os.walk(THEME_DIR, followlinks=False):
    rel = os.path.relpath(root, THEME_DIR)
    if rel == '.' or '@' in os.path.basename(rel):
        continue
    if any(f.endswith('.svg') or f.endswith('.png') for f in files) or os.path.islink(root):
        actual_dirs.add(rel)

actual_scaled_dirs = set(d[0] for d in scaled_dir_symlinks)

print(f"Declared Directories:        {len(declared_dirs)}")
print(f"Actual Directories with Icons: {len(actual_dirs)}")
print(f"  Missing from Directories=:   {len(actual_dirs - declared_dirs)}")
print(f"  Ghost in Directories=:       {len(declared_dirs - actual_dirs)}")

print(f"Declared ScaledDirectories:  {len(declared_scaled_dirs)}")
print(f"Actual Scaled Symlinks:      {len(actual_scaled_dirs)}")
print(f"  Missing from ScaledDirs=:    {len(actual_scaled_dirs - declared_scaled_dirs)}")
print(f"  Ghost in ScaledDirs=:        {len(declared_scaled_dirs - actual_scaled_dirs)}")

# Section Audit
section_dict = {}
for sec_match in re.finditer(r'\[([^\]]+)\](.*?)(?=\n\[|\Z)', content, re.DOTALL):
    sname = sec_match.group(1)
    sbody = sec_match.group(2)
    sdict = {}
    for l in sbody.strip().split('\n'):
        if '=' in l:
            k, v = l.strip().split('=', 1)
            sdict[k] = v
    section_dict[sname] = sdict

invalid_context_sections = []
invalid_type_sections = []
for sname, sdict in section_dict.items():
    if sname == 'Icon Theme':
        continue
    ctx = sdict.get('Context')
    if not ctx or ctx not in VALID_CONTEXTS:
        invalid_context_sections.append((sname, ctx))
    dtype = sdict.get('Type')
    if not dtype or dtype not in VALID_TYPES:
        invalid_type_sections.append((sname, dtype))

print("\n--- 4. Section Declarations Validation ---")
print(f"Total directory sections:    {len(section_dict) - 1}")
print(f"Invalid Context sections:    {len(invalid_context_sections)}")
print(f"Invalid Type sections:       {len(invalid_type_sections)}")

print("\n=================================================================")
print("                      SCAN COMPLETED                             ")
print("=================================================================")
