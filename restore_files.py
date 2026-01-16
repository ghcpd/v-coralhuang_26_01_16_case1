# Generator script to recreate Python files with proper encoding

# Read the original files from backup if they exist
import os
import shutil

# Restore from backup
backup_dir = r"C:\Bug_Bash\26_01_16\Claude-sonnet-4.5-backup"
target_dir = r"C:\Bug_Bash\26_01_16\Claude-sonnet-4.5"

files_to_restore = ['errors.py', 'log.py', 'data/__init__.py', 'data/browsers.json']

for file in files_to_restore:
    src = os.path.join(backup_dir, file)
    dst = os.path.join(target_dir, file)
    if os.path.exists(src):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        print(f"Restored {file}")

print("Files restored from backup")
