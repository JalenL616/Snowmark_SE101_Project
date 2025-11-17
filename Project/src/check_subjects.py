#!/usr/bin/env python3
import sys
import os
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from crud import get_all_subjects, add_subject, get_subject_by_name
from db import init_db

# Initialize database
print("Initializing database...")
init_db()

# Check current subjects
print("\nCurrent subjects in database:")
subjects = get_all_subjects()
for s in subjects:
    print(f"  - {s['name']} (ID: {s['id']})")

print(f"\nTotal: {len(subjects)} subjects")

# Ensure original subjects exist
original_subjects = ["Mathematics", "History", "Science"]
print(f"\nEnsuring original subjects exist...")

for subj_name in original_subjects:
    existing = get_subject_by_name(subj_name)
    if not existing:
        print(f"  Adding missing subject: {subj_name}")
        subj_id = add_subject(subj_name)
        print(f"    ✓ Added {subj_name} (ID: {subj_id})")
    else:
        print(f"  ✓ {subj_name} already exists (ID: {existing['id']})")

print("\n✓ All original subjects are in database!")
