# Phases 7-10: Completion Plan

## Current Status
- ✅ **Phases 1-6 Complete**: Database-only architecture with category management
- ❌ **Add Subject Not Working**: Subject only exists when assignment/category added
- 📋 **Remaining Work**: Based on charter requirements

## Phase 7: Subject Management + Recommendations (Week 2 Charter Goal)

### 7.1 Fix Subject Management
**Problem**: Subjects don't persist without assignments
**Solution**: Create Subjects table in database

#### Changes Needed:
1. **Database Schema** (`db.py`):
   - Add `SUBJECTS_TABLE` DDL
   - Create subjects table with: `id`, `name`, `user_id`, `created_at`

2. **CRUD Operations** (`crud.py`):
   - `add_subject(name)` - Insert into subjects table
   - `get_all_subjects()` - Query subjects table
   - `delete_subject(subject_id)` - Delete subject and cascade

3. **Routes** (`app.py`):
   - Update `/add_subject` to insert into database
   - Update `/delete_subject` to use subject ID
   - Update `display_table` to query subjects table

4. **Testing**:
   - Test subject CRUD operations
   - Verify subjects persist without assignments

### 7.2 Study Time Recommendations Algorithm
**Charter Goal**: "Initial recommendation algorithm" (Week 2)

#### Algorithm Design:
```python
def calculate_recommendations(subject):
    """
    Calculate recommended weekly study hours based on:
    1. Current grade vs target grade gap
    2. Category weights
    3. Historical study time effectiveness
    """
    # Get target grade for subject (if set)
    # Get current weighted grade
    # Calculate gap
    # Recommend hours based on:
    #   - Gap size (larger gap = more hours)
    #   - Category weights (focus on high-weight categories)
    #   - Historical k-value (efficiency factor)
```

#### Implementation:
1. Add target grade field to subjects table
2. Create recommendation calculation function
3. Add `/get_recommendations` route
4. Display recommendations in UI

**Estimated Complexity**: Medium (3-4 hours)

---

## Phase 8: Weekly Dashboard & Charts (Week 3 Charter Goal)

### 8.1 Weekly Summary Dashboard
**Charter Goal**: "Weekly summary dashboard"

#### Features:
1. **Weekly Totals**:
   - Total hours studied this week
   - Hours per subject
   - Average grade per subject

2. **Week Navigation**:
   - Current week (default)
   - Previous/Next week buttons
   - Week date range display

3. **Comparison**:
   - Recommended vs actual hours
   - Color-coded progress bars
   - Gap indicators

#### Implementation:
1. Add week calculation helpers
2. Create `/api/weekly_summary` endpoint
3. Build weekly dashboard UI component
4. Add week navigation controls

**Estimated Complexity**: Medium (4-5 hours)

### 8.2 Charts and Visualizations
**Charter Goal**: "Charts"

#### Chart Types:
1. **Hours Pie Chart** (Already exists):
   - Improve with better colors
   - Add tooltips

2. **Weekly Trend Line Chart** (New):
   - Study hours over last 4 weeks
   - Multiple subjects on same chart
   - Legend and axis labels

3. **Grade Progress Chart** (New):
   - Current vs target grade
   - Progress bars
   - Visual indicators (on track/behind)

#### Implementation:
1. Use existing Chart.js library
2. Create chart components
3. Add data endpoints
4. Integrate into dashboard

**Estimated Complexity**: Medium-High (5-6 hours)

---

## Phase 9: Testing & Documentation (Week 4 Charter Goal)

### 9.1 Achieve 70% Test Coverage
**Charter Requirement**: "≥70% automated test coverage"

#### Current Test Files:
- `test_phase2.py` - Read-only integration
- `test_phase3.py` - Dual-write
- `test_phase4.py` - Weight recalculation
- `test_phase5.py` - Category UI
- `test_phase6.py` - Database-only
- `test_update_delete_fix.py` - Bug fix verification

#### Additional Tests Needed:
1. **Unit Tests**:
   - `test_crud.py` - All CRUD functions
   - `test_calculations.py` - Summary, predictions, recommendations

2. **Integration Tests**:
   - `test_routes.py` - All Flask routes
   - `test_auth.py` - Login/logout

3. **Coverage Report**:
   ```bash
   pytest --cov=. --cov-report=html
   ```

**Estimated Complexity**: High (6-8 hours)

### 9.2 Documentation
**Charter Requirements**:
- `docs/test_plan.md` ✅ (Likely exists)
- `docs/test_report.md` (Generate from coverage)
- `docs/user_manual.md` (Create)
- `README.md` (Update with setup instructions)

#### Documentation Tasks:
1. **User Manual**:
   - Getting started
   - Adding subjects/categories
   - Logging study time
   - Understanding recommendations
   - Screenshots

2. **Test Report**:
   - Coverage statistics
   - Test results
   - Known issues

3. **README**:
   - Setup instructions
   - Environment variables
   - Running the app
   - Running tests

**Estimated Complexity**: Medium (3-4 hours)

---

## Phase 10: Polish & v1.0 Release (Week 4 Charter Goal)

### 10.1 Bug Fixes & Polish
**Charter Goal**: "Hardening"

#### Tasks:
1. **UI/UX Improvements**:
   - Consistent styling
   - Loading indicators
   - Better error messages
   - Form validation

2. **Bug Fixes**:
   - Test all user workflows
   - Fix any edge cases
   - Handle empty states gracefully

3. **Performance**:
   - Optimize database queries
   - Add indexes if needed
   - Minimize page reloads

**Estimated Complexity**: Medium (4-5 hours)

### 10.2 Demo & Review
**Charter Requirements**:
- `docs/demo.mp4` (2-4 minute demo)
- `docs/review_presentation.pdf`

#### Demo Script:
1. Login
2. Add subject
3. Add categories with weights
4. Add assignments
5. View recommendations
6. Check weekly dashboard
7. View charts
8. Show grade predictions

**Estimated Complexity**: Low-Medium (2-3 hours)

### 10.3 v1.0 Release
**Charter Requirement**: "Tagged v1.0 release"

#### Release Checklist:
- [ ] All tests passing
- [ ] Coverage ≥70%
- [ ] Documentation complete
- [ ] Demo recorded
- [ ] No critical bugs
- [ ] Clean git history

#### Release Steps:
```bash
git tag -a v1.0.0 -m "Release v1.0.0: Study Time Tracker MVP"
git push origin v1.0.0
```

**Estimated Complexity**: Low (1 hour)

---

## Time Estimates

| Phase | Tasks | Estimated Hours |
|-------|-------|----------------|
| **Phase 7** | Subject table + Recommendations | 6-8 hours |
| **Phase 8** | Weekly dashboard + Charts | 9-11 hours |
| **Phase 9** | Testing + Documentation | 9-12 hours |
| **Phase 10** | Polish + Release | 7-9 hours |
| **Total** | | **31-40 hours** |

## Priority Order (Recommended)

### High Priority (Must Have for v1.0):
1. ✅ Fix add subject (Phase 7.1)
2. ⚠️ Basic recommendations (Phase 7.2 - simplified)
3. ⚠️ Weekly summary (Phase 8.1 - basic version)
4. ✅ Testing ≥70% coverage (Phase 9.1)
5. ✅ Documentation (Phase 9.2)
6. ✅ v1.0 Release (Phase 10.3)

### Medium Priority (Nice to Have):
1. Advanced charts (Phase 8.2)
2. UI polish (Phase 10.1)
3. Demo video (Phase 10.2)

### Low Priority (Future):
1. Advanced recommendation algorithm
2. Export functionality
3. Mobile responsive design

## Next Immediate Steps

1. **Fix Add Subject** (30 min):
   - Create subjects table
   - Update routes
   - Test functionality

2. **Basic Recommendations** (2 hours):
   - Simple algorithm: gap × category weight
   - Add to UI
   - Basic testing

3. **Testing Sprint** (4 hours):
   - Write comprehensive tests
   - Run coverage report
   - Fix to ≥70%

4. **Documentation** (2 hours):
   - Update README
   - Create test report
   - Quick user guide

5. **Release** (1 hour):
   - Final testing
   - Tag v1.0.0
   - Celebrate! 🎉

## Success Criteria

✅ **Minimum Viable Product (MVP)**:
- Subjects/categories/assignments CRUD working
- Basic grade tracking
- Simple study recommendations
- 70% test coverage
- Basic documentation
- Tagged v1.0.0 release

🎯 **Ideal v1.0**:
- All above +
- Weekly dashboard
- Charts
- User manual
- Demo video
- Polish UI

---

## Current Focus: Phase 7.1 - Fix Add Subject

Let's start by implementing the subjects table and fixing the add subject functionality. This is blocking users from properly using the app.
