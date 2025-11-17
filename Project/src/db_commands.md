# Database Testing Commands

## Quick SQL Commands (if you have mysql client)

Connect to database:
```bash
mysql -h riku.shoshin.uwaterloo.ca -u <your_userid> -p SE101_Team_21
```

Then run these queries:

```sql
-- Show all tables
SHOW TABLES;

-- View table structure
DESCRIBE l48cai_grades;
DESCRIBE l48cai_categories;

-- Count rows
SELECT COUNT(*) FROM l48cai_grades;
SELECT COUNT(*) FROM l48cai_categories;

-- View all data
SELECT * FROM l48cai_categories;
SELECT * FROM l48cai_grades;

-- View assignments by subject
SELECT Subject, Category, AssignmentName, Grade, Weight
FROM l48cai_grades
ORDER BY Subject, Category;

-- Check category weights
SELECT Subject, CategoryName, TotalWeight, DefaultName
FROM l48cai_categories
ORDER BY Subject, CategoryName;
```

## Python Testing Scripts

### 1. Full test suite
```bash
cd /Users/jalenlocke/project_team_21/Project/src
python3 test_db_setup.py
```

### 2. View database contents
```bash
python3 query_db.py
```

### 3. Test in Python interactive shell
```bash
python3
```

Then:
```python
import os
from dotenv import load_dotenv
load_dotenv('.env')

from db import init_db, _connect, TABLE_NAME, CATEGORIES_TABLE
from crud import get_all_grades

# Initialize if needed
init_db()

# Fetch all assignments
grades = get_all_grades()
print(f"Found {len(grades)} assignments")
for g in grades[:3]:
    print(g)

# Query categories directly
conn = _connect()
cur = conn.cursor(dictionary=True)
cur.execute(f"SELECT * FROM {CATEGORIES_TABLE}")
cats = cur.fetchall()
print(f"\nFound {len(cats)} categories")
for c in cats:
    print(c)
cur.close()
conn.close()
```

## What to Look For

✅ **Both tables exist:**
- `{username}_grades` - has 7 columns including Category
- `{username}_categories` - has 5 columns

✅ **Seed data present:**
- 5 categories (Math: Homework & Quizzes, History: Essays, Science: Labs & Projects)
- 6 sample assignments

✅ **Schema correct:**
- Category column exists in grades table
- Unique constraint on (Subject, CategoryName) in categories table

## Common Issues

**Issue:** "Unknown column 'Category'"
**Fix:** Run `python3 migrate_schema.py` to add the column

**Issue:** "Table doesn't exist"
**Fix:** Run `python3 -c "from db import init_db; init_db()"`

**Issue:** Empty tables
**Fix:** Tables auto-seed on first run. Run `init_db()` again.

## Next Steps After Testing

Once you verify the database is working:
1. ✅ Phase 1 Complete - Database schema ready
2. ⏭️ Phase 2 - Start reading data from database in the app
3. ⏭️ Phase 3 - Add write operations (dual-write mode)
