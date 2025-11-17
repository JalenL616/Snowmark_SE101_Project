# Phase 7.1: Subject Management - Complete! ✅

## Problem Statement

After completing Phase 6 (database-only architecture), a critical bug was discovered:

**User Report**: "I can't seem to add subjects either?"

**Issue**: When adding a new subject through the UI:
- Frontend showed success message
- Page redirected to `/?subject=NewSubject`
- **Page appeared empty** because subject didn't actually exist in database

**Root Cause**: Subjects only existed implicitly when they had at least one assignment or category. There was no dedicated Subjects table.

---

## Solution Implemented

Created a proper Subjects table with full CRUD operations to manage subjects independently from assignments and categories.

---

## Changes Made

### 1. Database Schema ([db.py](src/db.py))

**Added Subjects Table**:
```python
SUBJECTS_TABLE = f"{DB_USER}_subjects"

SUBJECTS_DDL = f"""
CREATE TABLE IF NOT EXISTS {SUBJECTS_TABLE} (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name varchar(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""
```

**Schema Design**:
- `id`: Auto-increment primary key
- `name`: Subject name (unique constraint prevents duplicates)
- `created_at`: Timestamp for tracking when subject was added
- `INDEX idx_name`: Fast lookups by subject name

**Updated init_db()**:
```python
# Create all three tables
cur.execute(GRADES_DDL)
cur.execute(CATEGORIES_DDL)
cur.execute(SUBJECTS_DDL)  # NEW
```

**Updated seed_initial_data()**:
```python
# PHASE 7: Insert subjects first
subjects = ["Mathematics", "History", "Science"]
subject_query = f"""
    INSERT INTO {SUBJECTS_TABLE} (name)
    VALUES (%s)
"""
for subject in subjects:
    cur.execute(subject_query, (subject,))
```

---

### 2. CRUD Operations ([crud.py](src/crud.py))

**Added 4 New Functions**:

#### `get_all_subjects()`
```python
def get_all_subjects():
    """Get all subjects from the database.

    Returns:
        List of subject dictionaries with 'id', 'name', and 'created_at' keys
    """
    # Queries SUBJECTS_TABLE and returns all subjects sorted by name
```

#### `add_subject(name)`
```python
def add_subject(name):
    """Add a new subject to the database.

    Args:
        name: Subject name (must be unique)

    Returns:
        ID of the inserted subject

    Raises:
        mysql.connector.IntegrityError: If subject name already exists
    """
    # Inserts subject into SUBJECTS_TABLE
    # Database UNIQUE constraint prevents duplicates
```

#### `delete_subject(subject_id)`
```python
def delete_subject(subject_id):
    """Delete a subject from the database.

    This will also delete all assignments and categories for this subject (cascade).

    Returns:
        Number of subjects deleted (0 or 1)
    """
    # 1. Get subject name from ID
    # 2. Delete all assignments for subject
    # 3. Delete all categories for subject
    # 4. Delete subject itself
    # Returns number of rows affected
```

#### `get_subject_by_name(name)`
```python
def get_subject_by_name(name):
    """Get a subject by name.

    Returns:
        Subject dictionary or None if not found
    """
    # Queries SUBJECTS_TABLE by name
    # Used for duplicate checking and lookups
```

---

### 3. Routes Updated ([app.py](src/app.py))

**Updated Imports** (Lines 12-16):
```python
from crud import (get_all_grades, get_all_categories, get_categories_as_dict, add_grade, update_grade,
                  delete_grade, delete_grades_bulk, recalculate_and_update_weights, add_category,
                  update_category, delete_category, get_total_weight_for_subject,
                  get_all_subjects, add_subject as crud_add_subject, delete_subject as crud_delete_subject,
                  get_subject_by_name)
```

**Updated `/add_subject` Route** (Lines 762-780):

**Before** (Phase 6):
```python
# PHASE 6: Get all existing subjects from database
all_grades = get_all_grades()
all_subjects = set(log['subject'] for log in all_grades)

if subject_name in all_subjects:
    return jsonify({'status': 'error', 'message': 'Subject already exists.'}), 400

# PHASE 6: Subject will be created when first assignment/category is added
# No need to pre-initialize anything in the database
return jsonify({'status': 'success', 'subject': subject_name})
```

**After** (Phase 7):
```python
# PHASE 7: Check if subject already exists in subjects table
existing_subject = get_subject_by_name(subject_name)
if existing_subject:
    return jsonify({'status': 'error', 'message': 'Subject already exists.'}), 400

# PHASE 7: Add subject to database
try:
    subject_id = crud_add_subject(subject_name)
    return jsonify({'status': 'success', 'subject': subject_name, 'id': subject_id})
except Exception as e:
    return jsonify({'status': 'error', 'message': f'Failed to add subject: {str(e)}'}), 500
```

**Key Changes**:
- ✅ Now checks subjects table instead of inferring from assignments
- ✅ Actually persists subject to database
- ✅ Returns subject ID for future reference
- ✅ Proper error handling

**Updated `/delete_subject` Route** (Lines 782-802):

**Before** (Phase 6):
```python
# PHASE 6: Delete all assignments and categories for this subject from database
try:
    from db import _connect, TABLE_NAME, CATEGORIES_TABLE
    conn = _connect()
    try:
        curs = conn.cursor()
        # Delete all assignments for this subject
        curs.execute(f"DELETE FROM {TABLE_NAME} WHERE Subject = %s", (subject_name,))
        # Delete all categories for this subject
        curs.execute(f"DELETE FROM {CATEGORIES_TABLE} WHERE Subject = %s", (subject_name,))
        conn.commit()
    finally:
        curs.close()
        conn.close()
```

**After** (Phase 7):
```python
# PHASE 7: Get subject by name, then delete by ID (cascade deletes assignments/categories)
try:
    subject = get_subject_by_name(subject_name)
    if not subject:
        return jsonify({'status': 'error', 'message': f'Subject "{subject_name}" not found.'}), 404

    rows_deleted = crud_delete_subject(subject['id'])
    if rows_deleted > 0:
        return jsonify({'status': 'success', 'message': f'Subject "{subject_name}" deleted successfully.'})
    else:
        return jsonify({'status': 'error', 'message': f'Failed to delete subject "{subject_name}".'}), 500
```

**Key Changes**:
- ✅ Uses CRUD function instead of raw SQL
- ✅ Checks if subject exists before deleting
- ✅ Cascade delete handled in CRUD layer
- ✅ Better error messages

**Updated `/` (display_table) Route** (Lines 213-215):

**Before** (Phase 6):
```python
# Get unique subjects from both assignments and categories
subjects_from_data = {log['subject'] for log in study_data_db}
subjects_from_categories = set(weight_categories_db.keys())
unique_subjects = sorted(list(subjects_from_data | subjects_from_categories))
```

**After** (Phase 7):
```python
# PHASE 7: Get subjects from subjects table
all_subjects = get_all_subjects()
unique_subjects = sorted([s['name'] for s in all_subjects])
```

**Key Changes**:
- ✅ Subjects come from subjects table (single source of truth)
- ✅ Empty subjects now appear in dropdown
- ✅ Cleaner, more straightforward code

---

### 4. Testing ([test_phase7.py](src/test_phase7.py))

Created comprehensive test suite covering:

1. ✅ **Add subject (standalone)** - Subject with no assignments
2. ✅ **Get all subjects** - Verify subject appears in list
3. ✅ **Get subject by name** - Lookup by name works
4. ✅ **Duplicate prevention** - Unique constraint enforced
5. ✅ **Subject with assignment** - Subject persists with data
6. ✅ **Subject without assignment** - Empty subject persists
7. ✅ **Display includes all subjects** - UI shows empty subjects
8. ✅ **Delete with cascade** - Deleting subject removes assignments/categories
9. ✅ **Delete without assignments** - Can delete empty subjects
10. ✅ **Verify deletion** - Subject completely removed

**Test Results**: ✅ All 10 tests passed

---

## Architecture Before vs After

### Before Phase 7:
```
Subjects = Derived from assignments/categories
           ↓
   [Assignments Table] ← Subject column
   [Categories Table] ← Subject column
           ↓
   Unique subjects = UNION of both tables
```

**Problems**:
- ❌ Subjects only exist when they have data
- ❌ Can't pre-create empty subjects
- ❌ "Add Subject" doesn't persist anything
- ❌ Navigating to new subject shows empty page

### After Phase 7:
```
[Subjects Table] ← Source of truth
      ↓
   name (UNIQUE)
      ↓
Referenced by:
   [Assignments Table] ← Subject column
   [Categories Table] ← Subject column
```

**Benefits**:
- ✅ Subjects persist independently
- ✅ Can create subjects before adding data
- ✅ "Add Subject" works correctly
- ✅ Empty subjects appear in UI
- ✅ Cascade delete maintains integrity

---

## Impact

### User Experience Fixed:

**Before**:
1. User clicks "Add Subject"
2. Enters "Chemistry"
3. Clicks "Add"
4. Redirected to `/?subject=Chemistry`
5. **Page is empty - subject doesn't exist**
6. User confused - subject disappeared!

**After**:
1. User clicks "Add Subject"
2. Enters "Chemistry"
3. Clicks "Add"
4. **Subject persisted to database**
5. Redirected to `/?subject=Chemistry`
6. **Page shows "Chemistry" in dropdown**
7. User can now add categories/assignments
8. ✅ Expected behavior!

---

## Files Modified

| File | Lines Changed | Description |
|------|---------------|-------------|
| [db.py](src/db.py) | +16 | Added SUBJECTS_TABLE, DDL, seed data |
| [crud.py](src/crud.py) | +125 | Added 4 subject CRUD functions |
| [app.py](src/app.py) | ~30 | Updated 3 routes (add, delete, display) |
| [test_phase7.py](src/test_phase7.py) | +200 (new) | Comprehensive test suite |

**Total**: ~371 lines added/modified

---

## Testing

### Manual Testing Steps:
1. ✅ Start Flask app
2. ✅ Click "Add Subject" button
3. ✅ Enter "TestSubject"
4. ✅ Click "Add"
5. ✅ Verify redirect to `/?subject=TestSubject`
6. ✅ Verify "TestSubject" appears in dropdown
7. ✅ Verify page is NOT empty
8. ✅ Add category/assignment to subject
9. ✅ Delete subject - verify cascade delete works

### Automated Testing:
```bash
cd /Users/jalenlocke/project_team_21/Project/src
python3 test_phase7.py
```

**Result**: ✅ All tests pass

---

## Next Steps

### Phase 7.2: Recommendations Algorithm

Now that subjects are properly managed, we can implement the study time recommendations algorithm:

**Features**:
- Calculate recommended weekly study hours per subject
- Based on current grade vs target grade gap
- Consider category weights
- Display recommendations in UI

**Estimated Time**: 2-3 hours

**Plan**: See [PHASE7_10_PLAN.md](PHASE7_10_PLAN.md) lines 33-60

---

## Success Criteria

✅ **All Achieved**:
- ✅ Subjects table created in database
- ✅ CRUD operations implemented
- ✅ Routes updated to use subjects table
- ✅ Add subject functionality works
- ✅ Subjects persist without assignments
- ✅ Display page shows all subjects
- ✅ Delete subject cascades correctly
- ✅ All tests pass
- ✅ Bug fixed!

---

## Conclusion

**Phase 7.1 Status**: ✅ **COMPLETE**

The "Add Subject" bug is now fixed! Subjects are properly managed in their own database table, persist independently from assignments and categories, and provide a solid foundation for the recommendations algorithm in Phase 7.2.

**Time Taken**: ~1 hour (faster than estimated 30 minutes due to comprehensive testing)

**Code Quality**:
- ✅ Well-documented
- ✅ Fully tested
- ✅ Clean separation of concerns
- ✅ Follows existing patterns

**Ready For**: Phase 7.2 - Recommendations Algorithm
