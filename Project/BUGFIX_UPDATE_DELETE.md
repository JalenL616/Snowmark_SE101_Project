# Bug Fix: Assignment Not Found on Update/Delete

## Problem Description

After adding a new assignment, attempting to **update** or **delete** it would fail with the error:
```
Assignment not found.
```

This happened even though the assignment clearly existed in the database and was visible in the UI.

## Root Cause

The issue was in the `/update/<id>` and `/delete/<id>` routes in [app.py](src/app.py):

### Before Fix (Lines 346, 391):
```python
# UPDATE route (line 346)
update_index = next((i for i, log in enumerate(study_data) if log['id'] == log_id), -1)
if update_index == -1:
    return jsonify({'status': 'error', 'message': 'Assignment not found.'}), 404

# DELETE route (line 391)
log_to_delete = next((log for log in study_data if log['id'] == log_id), None)
if log_to_delete:
    # ... delete logic
else:
    return jsonify({'status': 'error', 'message': 'Assignment not found.'}), 404
```

**The Problem**: Both routes were checking the **in-memory `study_data` dictionary** to see if the assignment exists.

### Why This Failed:

1. **Initial State**: When the Flask app starts, `study_data` is initialized with a hardcoded list of assignments:
   ```python
   study_data = [
       {"id": 1, "subject": "Mathematics", ...},
       {"id": 2, "subject": "History", ...},
       # ... only pre-existing assignments
   ]
   ```

2. **Adding New Assignment**: When a user adds a new assignment:
   - ✅ Assignment is saved to the **database** (correct!)
   - ✅ Assignment is appended to in-memory `study_data` (for backwards compatibility)
   - ✅ ID returned is the database's auto-increment ID (e.g., ID 22)

3. **The Bug**: However, if the app was restarted or there was any issue with the in-memory dict sync:
   - ❌ New assignment exists in **database** with ID 22
   - ❌ In-memory dict might not have ID 22
   - ❌ Update/delete routes check in-memory dict → "not found"

## The Fix

Changed both routes to **check the database** instead of the in-memory dictionary:

### After Fix:

#### UPDATE Route (Lines 346-351):
```python
@app.route('/update/<int:log_id>', methods=['POST'])
@login_required
def update_log(log_id):
    # PHASE 5 FIX: Check database instead of in-memory dict
    all_assignments = get_all_grades()  # Query database
    old_log = next((log for log in all_assignments if log['id'] == log_id), None)

    if not old_log:
        return jsonify({'status': 'error', 'message': 'Assignment not found.'}), 404

    # ... rest of update logic
```

#### DELETE Route (Lines 398-403):
```python
@app.route('/delete/<int:log_id>', methods=['POST'])
@login_required
def delete_log(log_id):
    current_filter = request.args.get('current_filter')

    # PHASE 5 FIX: Check database instead of in-memory dict
    all_assignments = get_all_grades()  # Query database
    log_to_delete = next((log for log in all_assignments if log['id'] == log_id), None)

    if not log_to_delete:
        return jsonify({'status': 'error', 'message': 'Assignment not found.'}), 404

    # ... rest of delete logic
```

### Backwards Compatibility

The fix still maintains backwards compatibility with the in-memory dictionary:

```python
# In UPDATE route (lines 374-376):
update_index = next((i for i, log in enumerate(study_data) if log['id'] == log_id), -1)
if update_index != -1:
    study_data[update_index] = updated_data  # Update if exists

# In DELETE route (lines 413-415):
in_memory_log = next((log for log in study_data if log['id'] == log_id), None)
if in_memory_log:
    study_data.remove(in_memory_log)  # Delete if exists
```

This ensures the in-memory dict stays in sync **if** the assignment exists there, but doesn't fail if it doesn't.

## Testing

### Automated Test
**File**: [test_update_delete_fix.py](src/test_update_delete_fix.py)

The test verifies:
1. ✅ Adding a new assignment to database
2. ✅ Updating the newly added assignment (would fail before fix)
3. ✅ Deleting the newly added assignment (would fail before fix)

### Test Results
```
[4/5] Testing UPDATE on newly added assignment...
  (This would fail with 'Assignment not found' before the fix)
  ✓ Updated 1 assignment successfully!
  ✓ Update verified in database

[5/5] Testing DELETE on newly added assignment...
  (This would fail with 'Assignment not found' before the fix)
  ✓ Deleted 1 assignment successfully!
  ✓ Deletion verified - assignment no longer in database
```

## Files Modified

### [app.py](src/app.py)
**Lines Changed**:
- **Lines 343-378**: UPDATE route - now queries database first
- **Lines 393-427**: DELETE route - now queries database first

**Key Changes**:
1. Added `all_assignments = get_all_grades()` to fetch from database
2. Check database for assignment existence instead of in-memory dict
3. Made in-memory dict updates conditional (only if assignment exists there)

## Impact

### Before Fix:
- ❌ Updating newly added assignments failed
- ❌ Deleting newly added assignments failed
- ❌ User had to refresh page to sync in-memory dict
- ❌ Poor user experience

### After Fix:
- ✅ All assignments can be updated regardless of when added
- ✅ All assignments can be deleted regardless of when added
- ✅ Database is the source of truth (as it should be)
- ✅ Seamless user experience

## Related Issues Fixed

This fix also resolves the issue mentioned earlier where:
> "When I add a new assignment it hides all the previous ones until I refresh"

That was a separate but related issue where the ADD route was returning in-memory data instead of database data. Both issues stemmed from **over-reliance on the in-memory dictionary**.

## Why This Matters

This bug fix is crucial for the transition from in-memory to database-driven architecture:

### Phase 2-3 (Previous):
- **Read** from database ✅
- **Write** to both database AND in-memory dict (dual-write) ✅
- **Check existence** via in-memory dict ❌ (This was the bug!)

### Phase 5 (Now):
- **Read** from database ✅
- **Write** to database ✅
- **Check existence** via database ✅
- **In-memory dict** updated optionally for backwards compatibility

## Next Steps

### Phase 6: Remove In-Memory Dictionary Completely
Now that all operations properly use the database, we can:
1. Remove the hardcoded `study_data` initialization
2. Remove dual-write code
3. Simplify all routes to only use database
4. Clean up backwards compatibility code

This will make the codebase cleaner and prevent similar bugs in the future.

## Conclusion

**Bug Status**: ✅ **FIXED**

The update and delete functionality now works correctly for all assignments, regardless of when they were added. The database is properly treated as the source of truth, and the application is one step closer to full database integration.
