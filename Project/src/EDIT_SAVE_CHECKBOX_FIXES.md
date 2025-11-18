# Edit/Save Button and Checkbox Alignment Fixes

## Date: 2025-11-17
## Branch: 27-Sprint-2

## Overview
Fixed two critical issues with the multi-select delete feature:
1. Edit and Save buttons were not working due to event propagation conflicts
2. New and edited assignment rows were missing checkboxes, causing table alignment issues

---

## Issue 1: Edit/Save Buttons Not Working

### Problem
When clicking the Edit or Save buttons in the assignment table, nothing happened. The buttons were completely non-functional.

### Root Cause
The row click handler (added for checkbox toggling) was preventing button clicks from reaching the button event listener due to how event delegation and propagation work in JavaScript.

**Problematic code (lines 1248-1284):**
- The row click handler checked `if (e.target.matches('button, input, select, .action-btn'))` and returned early
- However, this didn't properly handle nested button clicks
- The `stopPropagation` on checkbox clicks was interfering with normal event flow

### Solution
Enhanced the row click handler with multiple checks to properly handle different interaction scenarios:

```javascript
// Click anywhere on row to toggle checkbox (except buttons and inputs)
if (assignmentTableBody) {
    assignmentTableBody.addEventListener('click', function(e) {
        // Don't toggle if clicking on buttons, inputs, selects, or the checkbox itself
        if (e.target.matches('button, input, select, .action-btn')) {
            return;
        }

        // Don't toggle if clicking within an SVG (category tag icon)
        if (e.target.closest('svg')) {
            return;
        }

        // Don't toggle if the click is on an action button or its parent
        if (e.target.closest('button')) {
            return;
        }

        // Find the closest row
        const row = e.target.closest('tr[data-id]');
        if (!row) return;

        // Don't toggle for summary row
        if (row.classList.contains('summary-row')) return;

        // Don't toggle if row is in edit mode (has input/select elements)
        if (row.querySelector('input[name="study_time"], select[name="subject"]')) {
            return;
        }

        // Find and toggle the checkbox
        const checkbox = row.querySelector('.select-assignment');
        if (checkbox) {
            checkbox.checked = !checkbox.checked;
            updateDeleteButton();
        }
    });

    // Stop propagation on checkbox clicks to prevent double-toggling
    assignmentTableBody.addEventListener('click', function(e) {
        if (e.target.classList.contains('select-assignment')) {
            e.stopPropagation();
        }
    }, true);
}
```

### Key Improvements
1. **Added `e.target.closest('button')` check**: Prevents row clicks when clicking on or near buttons
2. **Added edit mode check**: Prevents checkbox toggling when row is being edited (has input/select elements)
3. **Preserved existing checks**: SVG check for category icons, summary row check, etc.

---

## Issue 2: Missing Checkboxes in New/Edit Rows

### Problem
When adding a new assignment or editing an existing one, the checkbox column was missing, causing:
- Table columns to be misaligned
- Content shifting to the left
- Visual inconsistency

### Root Cause
The code was written before checkboxes were added to the table. When the checkbox column was added at index 0, the JavaScript code wasn't updated to:
1. Include the checkbox column in new rows
2. Account for the shifted cell indices (everything moved +1)

### Solution

#### Part 1: Add Checkbox to New Rows
**File: main.js, Line 567**

**Before:**
```javascript
newRow.innerHTML = `${subjectTd.outerHTML}${categoryTd.outerHTML}<td><input type="number" name="study_time"...`;
```

**After:**
```javascript
newRow.innerHTML = `<td></td>${subjectTd.outerHTML}${categoryTd.outerHTML}<td><input type="number" name="study_time"...`;
```

Added empty `<td></td>` at the beginning to maintain checkbox column alignment.

#### Part 2: Fix Cell Indices Throughout

With checkbox at index 0, the table structure is now:
- **Index 0**: Checkbox
- **Index 1**: Subject
- **Index 2**: Category
- **Index 3**: Study Time
- **Index 4**: Assignment Name
- **Index 5**: Grade
- **Index 6**: Weight
- **Index 7**: Actions

**Updated all cell index references:**

1. **Edit button handler (lines 596-657):**
```javascript
const cells = row.querySelectorAll('td');
// Adjust indices: cells[0] is checkbox, cells[1] is subject, cells[2] is category, etc.
const subjectText = cells[1].textContent.trim();
const categoryText = cells[2].querySelector('.category-tag').lastChild.textContent.trim();
const gradeText = cells[5].textContent.trim();
// ...
cells[1].innerHTML = '';
cells[1].appendChild(subjectSelect);
cells[2].innerHTML = '';
cells[2].appendChild(categorySelect);
cells[3].innerHTML = `<input type="number" name="study_time"...`;
cells[4].innerHTML = `<input type="text" name="assignment_name"...`;
cells[5].innerHTML = `<input type="number" name="grade"...`;
cells[6].innerHTML = `<input type="number" name="weight"...`;
```

2. **Weight preview functions (lines 147-150, 166, 174, 182, 223):**
```javascript
// Check if it's in view mode (not being edited)
// cells[0] is checkbox, cells[1] is subject, cells[2] is category
if (cells.length > 1 && cells[2].querySelector('.category-tag')) {
    return cells[1].textContent.trim() === subject &&
           cells[2].querySelector('.category-tag').lastChild.textContent.trim() === category;
}

// Weight cell references
const weightCell = row.querySelectorAll('td')[6]; // Weight is now at index 6
```

3. **Predictor weight preview (lines 207-210, 223):**
```javascript
const cells = row.querySelectorAll('td');
// cells[0] is checkbox, cells[1] is subject, cells[2] is category
return cells.length > 1 &&
       cells[1].textContent.trim() === subject &&
       cells[2].querySelector('.category-tag')?.lastChild.textContent.trim() === category;
```

4. **Category table updates (lines 251-254):**
```javascript
const cells = r.querySelectorAll('td');
// cells[0] is checkbox, cells[1] is subject, cells[2] is category
return cells.length > 1 &&
       cells[1].textContent.trim() === subject &&
       cells[2].querySelector('.category-tag')?.lastChild.textContent.trim() === categoryName;
```

5. **Category name extraction (line 407):**
```javascript
// cells[0] is checkbox, cells[1] is subject, cells[2] is category
const categoryCell = row.querySelectorAll('td')[2];
```

6. **Default name counter (line 739):**
```javascript
// cells[0] is checkbox, cells[1] is subject, cells[2] is category
const existingCount = Array.from(document.querySelectorAll('#study-table-body tr[data-id]'))
    .filter(r => r.querySelectorAll('td')[2].textContent.trim().includes(categoryName)).length;
```

---

## Files Modified

### /Project/src/static/js/main.js

**Changes:**
1. Lines 147-150: Fixed cell indices in weight preview filter (subject: 0→1, category: 1→2)
2. Lines 166, 174, 182, 223: Fixed weight cell index (5→6)
3. Lines 207-210: Fixed cell indices in predictor weight preview filter
4. Lines 251-254: Fixed cell indices in category table update filter
5. Line 407: Fixed category cell index for extraction (1→2)
6. Line 567: Added empty `<td></td>` to new row template
7. Lines 596-657: Fixed all cell indices in edit button handler
8. Line 739: Fixed cell index in default name counter (1→2)
9. Lines 1248-1284: Enhanced row click handler with additional checks

---

## Testing Results

### Before Fixes
- ❌ Edit button does nothing when clicked
- ❌ Save button does nothing when clicked
- ❌ New assignment rows missing checkbox (misaligned)
- ❌ Edit mode rows missing checkbox (misaligned)
- ❌ Table columns shift when adding/editing assignments

### After Fixes
- ✅ Edit button works - converts row to edit mode
- ✅ Save button works - saves changes and exits edit mode
- ✅ New assignment rows have empty checkbox cell (aligned)
- ✅ Edit mode preserves checkbox cell (aligned)
- ✅ Table columns stay consistent across all states
- ✅ Checkbox toggling still works on regular row clicks
- ✅ Buttons don't trigger checkbox toggling

---

## Visual Comparison

### Table Structure - Before (Incorrect)
```
| Subject | Category | Study Time | Assignment | Grade | Weight | Actions |
| Math    | Homework | 2.0        | HW 1       | 85%   | 10%    | E | D   |  ← View mode (missing checkbox)
| [Select]| [Select] | [Input]    | [Input]    | [In]  | [In]   | S | D   |  ← Edit mode (missing checkbox, misaligned)
```

### Table Structure - After (Correct)
```
| ☐ | Subject | Category | Study Time | Assignment | Grade | Weight | Actions |
| ☑ | Math    | Homework | 2.0        | HW 1       | 85%   | 10%    | E | D   |  ← View mode (checkbox present)
|   | [Select]| [Select] | [Input]    | [Input]    | [In]  | [In]   | S | D   |  ← Edit mode (empty cell, aligned)
|   | [Select]| [Select] | [Input]    | [Input]    | [In]  | [In]   | S | D   |  ← New row (empty cell, aligned)
```

---

## Additional Notes

### Why Empty Cell for Edit/New Rows?
The checkbox column in edit/new rows is intentionally left empty (just `<td></td>`) because:
1. **Prevents accidental selection**: User shouldn't select a row that's being edited
2. **Maintains alignment**: Preserves table structure with proper column count
3. **Clear visual state**: Empty cell indicates row is in special mode (edit/new)

### Event Propagation Strategy
The solution uses a multi-layered approach to handle different click scenarios:
1. **Direct button clicks**: Allowed to propagate to button event listener
2. **Edit mode row clicks**: Prevented from toggling checkbox (user is editing)
3. **View mode row clicks**: Allowed to toggle checkbox
4. **SVG/icon clicks**: Prevented from toggling checkbox
5. **Checkbox clicks**: stopPropagation prevents double-toggling

This ensures buttons work while preserving the convenient "click anywhere to select" feature.

---

## Related Documentation
- [MULTISELECT_BUGFIXES.md](MULTISELECT_BUGFIXES.md) - Original multi-select delete implementation
- [MULTISELECT_DELETE_IMPLEMENTATION.md](MULTISELECT_DELETE_IMPLEMENTATION.md) - Multi-select delete feature docs
