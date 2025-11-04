Project Charter — Study Time Tracker/Planner​
Executive Summary
Build a Flask + MySQL web app that logs study time and grades, captures desired targets, and computes recommended weekly study hours per course; deliver a tagged v1.0 with automated tests and a short demo showing all user stories.​
Manage scope through groomed GitLab Issue Boards and a four‑week schedule, emphasizing quality gates and release tagging for reproducibility.​
Purpose and Objectives
Purpose: Help students optimize limited study time by converting inputs (time spent, grades, weights, targets) into clear study‑hour recommendations per course.​
SMART objectives: ship v1.0 in 4 weeks; achieve ≥70% automated test coverage; provide per‑course recommendations and a weekly summary dashboard; publish a 2–4 minute demo.​
Scope
In scope: account and course setup; weight and assessment inputs; study time logging; recommendation algorithm; CRUD on grades/time; weekly summary and charts; issue boards for backlog/sprints; pytest and coverage reports; reproducible setup.​
Out of scope (v1.0): native mobile apps, LMS integrations, and advanced ML personalization beyond heuristics.​
Quality boundaries: Definition of Done requires acceptance criteria met, tests passing in CI, documentation updated, and board status to Done.​
Key Deliverables
docs/charter.md; docs/user_stories.md; docs/domain_model.md; docs/use_cases.md.​
src/ with Flask app; MySQL schema/migrations; tests/ with pytest; docs/test_plan.md and docs/test_report.md with coverage ≥70%.​
Dashboard with weekly summary and charts; docs/user_manual.md; docs/demo.mp4 (2–4 min).​
Tagged v1.0 release (semantic tag) and review presentation (docs/review_presentation.pdf).​
Success Criteria
Minimum: core features working; reproducible setup; groomed issue boards; v1.0 tag; demo showing all user stories.​
Ideal: weekly suggestions with time windows, chart exports, background timer with persistence, and positive stakeholder review.​
Stakeholders and Roles
Teams: A and B (2–3 members each). Each sprint, one feature + associated tests per team; cross‑team Monday review/merge.​
Schedule and Milestones (4 Weeks)
Week 1: Charter/design finalized; backlog groomed; Flask skeleton and DB schema created.​
Week 2: CRUD for courses, assessments, and time logs; initial recommendation algorithm; unit tests and coverage configured.​
Week 3: Weekly summary dashboard and charts; study‑time suggestion logic; broader tests and doc updates.​
Week 4: Hardening; README/setup; test report ≥70% coverage; demo and review deck; v1.0 tag.​
Backlog and Sprint Management
Boards: Lists for Backlog, Selected, In Progress, In Review, Done; maintain manual priority order during grooming.​
Refinement: ensure stories are clear, estimated, and prioritized for upcoming sprints.​
Communication Plan
Channel: WhatsApp for daily coordination; Monday AM status with blockers; help requests ASAP.​
Cadence: Wednesday-Friday feature building and testing; Monday strictly for code review/merging; Tuesday assigns new reviews; keep board items current.​
Architecture and Tech Stack
Frontend: React with JavaScript.
Backend: Python 3 + Flask; MySQL; pytest + coverage; semantic tagging for releases; optional containerization for reproducible runs.​
Visualization: Matplotlib for charts in v1.0; consider swapping to a JS chart lib later.​
Testing and Quality
Strategy: unit and integration tests via pytest; coverage report linked from README and included in docs/test_report.md; threshold ≥70%.​
DoD: tests pass in CI; documentation updated; stakeholder acceptance per story; merged via review gate.​
Risks and Mitigations
Limited hours: prioritize core scope; park extras behind flags; keep sprints small and vertical.​
Grade/weight complexity: start with a minimal normalized schema; evolve via migrations as cases appear.​
Release reliability: require tag‑based builds and a scripted demo checklist before v1.0.​
Release and Versioning
Use semantic Git tag (v1.0.0) to mark release point; CI builds artifacts on tag; only tagged commits are treated as releases.​


