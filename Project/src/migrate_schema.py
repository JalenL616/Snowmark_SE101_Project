#!/usr/bin/env python3
"""
One-time migration script to update existing tables to new schema
Run this ONCE to add the Category column to existing grades table
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

from db import _connect, TABLE_NAME, CATEGORIES_TABLE

def migrate_schema():
    """Add Category column to existing grades table"""
    print("=" * 60)
    print("Schema Migration: Adding Category Column")
    print("=" * 60)

    conn = _connect()
    try:
        cur = conn.cursor()

        # Check if Category column exists
        cur.execute(f"DESCRIBE {TABLE_NAME}")
        columns = [row[0] for row in cur.fetchall()]

        if 'Category' in columns:
            print(f"\n✓ Column 'Category' already exists in {TABLE_NAME}")
            print("  No migration needed!")
            return True

        print(f"\n[1/2] Adding 'Category' column to {TABLE_NAME}...")

        # Add Category column after Subject
        alter_query = f"""
            ALTER TABLE {TABLE_NAME}
            ADD COLUMN Category varchar(255) NOT NULL DEFAULT 'Uncategorized'
            AFTER Subject
        """

        cur.execute(alter_query)
        conn.commit()
        print("  ✓ Category column added successfully")

        # Add index for performance
        print(f"\n[2/2] Adding index on (Subject, Category)...")
        try:
            cur.execute(f"""
                ALTER TABLE {TABLE_NAME}
                ADD INDEX idx_subject_category (Subject, Category)
            """)
            conn.commit()
            print("  ✓ Index added successfully")
        except Exception as e:
            if "Duplicate key name" in str(e):
                print("  ✓ Index already exists")
            else:
                print(f"  ! Warning: Could not add index: {e}")

        print("\n" + "=" * 60)
        print("✓ Migration Complete!")
        print("=" * 60)
        print("\nNext steps:")
        print("  1. Run test_db_setup.py to verify")
        print("  2. Manually set categories for existing data if needed")

        return True

    except Exception as e:
        conn.rollback()
        print(f"\n✗ Migration failed: {e}")
        return False
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    success = migrate_schema()
    sys.exit(0 if success else 1)
